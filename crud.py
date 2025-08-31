from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
import json

from app.models import Profile, Skill, Project, WorkExperience
from app.schemas import ProfileCreate, ProfileUpdate, ProjectCreate, ProjectUpdate, WorkExperienceCreate, WorkExperienceUpdate


def get_profile(db: Session, profile_id: int) -> Optional[Profile]:
    return db.query(Profile).options(
        joinedload(Profile.skills),
        joinedload(Profile.projects),
        joinedload(Profile.work_experiences)
    ).filter(Profile.id == profile_id).first()


def get_profile_by_email(db: Session, email: str) -> Optional[Profile]:
    return db.query(Profile).filter(Profile.email == email).first()


def get_profiles(db: Session, skip: int = 0, limit: int = 100) -> List[Profile]:
    return db.query(Profile).options(
        joinedload(Profile.skills),
        joinedload(Profile.projects),
        joinedload(Profile.work_experiences)
    ).offset(skip).limit(limit).all()


def create_profile(db: Session, profile: ProfileCreate) -> Profile:
    # Create profile
    db_profile = Profile(
        name=profile.name,
        email=profile.email,
        description=profile.description,
        github_url=profile.github_url,
        linkedin_url=profile.linkedin_url,
        portfolio_url=profile.portfolio_url
    )
    db.add(db_profile)
    db.flush()  # Get the ID without committing
    
    # Handle skills
    if profile.skills:
        for skill_name in profile.skills:
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.add(skill)
                db.flush()
            db_profile.skills.append(skill)
    
    # Handle projects
    if profile.projects:
        for project_data in profile.projects:
            project = Project(
                title=project_data.title,
                description=project_data.description,
                links=project_data.links,
                profile_id=db_profile.id
            )
            db.add(project)
    
    # Handle work experiences
    if profile.work_experiences:
        for work_data in profile.work_experiences:
            work = WorkExperience(
                company=work_data.company,
                position=work_data.position,
                description=work_data.description,
                start_date=work_data.start_date,
                end_date=work_data.end_date,
                profile_id=db_profile.id
            )
            db.add(work)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: int, profile_update: ProfileUpdate) -> Optional[Profile]:
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return None
    
    # Update basic fields
    for field, value in profile_update.dict(exclude_unset=True, exclude={'skills'}).items():
        setattr(db_profile, field, value)
    
    # Handle skills update
    if profile_update.skills is not None:
        # Clear existing skills
        db_profile.skills.clear()
        
        # Add new skills
        for skill_name in profile_update.skills:
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.add(skill)
                db.flush()
            db_profile.skills.append(skill)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_id: int) -> bool:
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return False
    
    db.delete(db_profile)
    db.commit()
    return True


def get_projects_by_skill(db: Session, skill: str) -> List[Project]:
    return db.query(Project).join(Profile).join(Profile.skills).filter(
        Skill.name.ilike(f"%{skill}%")
    ).all()


def get_top_skills(db: Session, limit: int = 10) -> List[dict]:
    from sqlalchemy import func
    result = db.query(
        Skill.name,
        func.count(Profile.id).label('count')
    ).join(Profile.skills).group_by(Skill.name).order_by(
        func.count(Profile.id).desc()
    ).limit(limit).all()
    
    return [{"skill": name, "count": count} for name, count in result]


def search_profiles(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Profile]:
    search_term = f"%{query}%"
    return db.query(Profile).options(
        joinedload(Profile.skills),
        joinedload(Profile.projects),
        joinedload(Profile.work_experiences)
    ).filter(
        or_(
            Profile.name.ilike(search_term),
            Profile.description.ilike(search_term),
            Profile.skills.any(Skill.name.ilike(search_term))
        )
    ).offset(skip).limit(limit).all()


def create_project(db: Session, profile_id: int, project: ProjectCreate) -> Optional[Project]:
    if not get_profile(db, profile_id):
        return None
    
    db_project = Project(
        title=project.title,
        description=project.description,
        links=project.links,
        profile_id=profile_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return None
    
    for field, value in project_update.dict(exclude_unset=True).items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True


def create_work_experience(db: Session, profile_id: int, work: WorkExperienceCreate) -> Optional[WorkExperience]:
    if not get_profile(db, profile_id):
        return None
    
    db_work = WorkExperience(
        company=work.company,
        position=work.position,
        description=work.description,
        start_date=work.start_date,
        end_date=work.end_date,
        profile_id=profile_id
    )
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def update_work_experience(db: Session, work_id: int, work_update: WorkExperienceUpdate) -> Optional[WorkExperience]:
    db_work = db.query(WorkExperience).filter(WorkExperience.id == work_id).first()
    if not db_work:
        return None
    
    for field, value in work_update.dict(exclude_unset=True).items():
        setattr(db_work, field, value)
    
    db.commit()
    db.refresh(db_work)
    return db_work


def delete_work_experience(db: Session, work_id: int) -> bool:
    db_work = db.query(WorkExperience).filter(WorkExperience.id == work_id).first()
    if not db_work:
        return False
    
    db.delete(db_work)
    db.commit()
    return True