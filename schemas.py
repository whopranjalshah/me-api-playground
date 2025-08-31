from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import json


class SkillBase(BaseModel):
    name: str


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str
    description: str
    links: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    links: Optional[str] = None


class Project(ProjectBase):
    id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkExperienceBase(BaseModel):
    company: str
    position: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None


class WorkExperienceCreate(WorkExperienceBase):
    pass


class WorkExperienceUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class WorkExperience(WorkExperienceBase):
    id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProfileBase(BaseModel):
    name: str
    email: EmailStr
    description: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None


class ProfileCreate(ProfileBase):
    skills: List[str] = []
    projects: List[ProjectCreate] = []
    work_experiences: List[WorkExperienceCreate] = []


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    skills: Optional[List[str]] = None


class Profile(ProfileBase):
    id: int
    skills: List[Skill] = []
    projects: List[Project] = []
    work_experiences: List[WorkExperience] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProfileSummary(BaseModel):
    id: int
    name: str
    email: EmailStr
    skills_count: int
    projects_count: int
    work_experiences_count: int