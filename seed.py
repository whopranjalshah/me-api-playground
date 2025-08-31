from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Profile, Skill, Project, WorkExperience
from app.schemas import ProfileCreate, ProjectCreate, WorkExperienceCreate
from app import crud


def seed_database():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Profile).count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        # Create dummy profile data
        dummy_profile = ProfileCreate(
            name="John Doe",
            email="john.doe@example.com",
            description="Full-stack developer with 5+ years of experience in building web applications. Passionate about clean code, scalable architecture, and modern technologies.",
            github_url="https://github.com/johndoe",
            linkedin_url="https://linkedin.com/in/johndoe",
            portfolio_url="https://johndoe.dev",
            skills=[
                "Python", "FastAPI", "React", "TypeScript", "PostgreSQL",
                "Docker", "AWS", "Git", "REST APIs", "GraphQL",
                "Node.js", "Express.js", "MongoDB", "Redis", "Kubernetes"
            ],
            projects=[
                ProjectCreate(
                    title="E-commerce Platform",
                    description="Full-stack e-commerce application built with React and FastAPI. Features include user authentication, product catalog, shopping cart, and payment integration.",
                    links='{"github": "https://github.com/johndoe/ecommerce", "demo": "https://ecommerce-demo.johndoe.dev"}'
                ),
                ProjectCreate(
                    title="Task Management API",
                    description="RESTful API for task management with FastAPI. Includes features like user management, project organization, task assignment, and real-time notifications.",
                    links='{"github": "https://github.com/johndoe/task-api", "docs": "https://task-api.johndoe.dev/docs"}'
                ),
                ProjectCreate(
                    title="Weather Dashboard",
                    description="React-based weather dashboard that displays current conditions and forecasts. Uses third-party weather APIs and features responsive design.",
                    links='{"github": "https://github.com/johndoe/weather-dashboard", "demo": "https://weather.johndoe.dev"}'
                )
            ],
            work_experiences=[
                WorkExperienceCreate(
                    company="TechCorp Inc.",
                    position="Senior Full-Stack Developer",
                    description="Led development of customer-facing web applications. Mentored junior developers and implemented CI/CD pipelines. Reduced application load time by 40% through optimization.",
                    start_date=datetime(2022, 1, 1),
                    end_date=None  # Current position
                ),
                WorkExperienceCreate(
                    company="StartupXYZ",
                    position="Full-Stack Developer",
                    description="Developed MVP for fintech startup. Built RESTful APIs and React frontend. Implemented user authentication and payment processing systems.",
                    start_date=datetime(2020, 6, 1),
                    end_date=datetime(2021, 12, 31)
                ),
                WorkExperienceCreate(
                    company="WebDev Agency",
                    position="Junior Developer",
                    description="Worked on client projects using various web technologies. Gained experience in responsive design and cross-browser compatibility.",
                    start_date=datetime(2019, 3, 1),
                    end_date=datetime(2020, 5, 31)
                )
            ]
        )
        
        # Create the profile
        profile = crud.create_profile(db=db, profile=dummy_profile)
        print(f"Created profile: {profile.name} (ID: {profile.id})")
        
        # Create a second dummy profile
        dummy_profile_2 = ProfileCreate(
            name="Jane Smith",
            email="jane.smith@example.com",
            description="DevOps engineer and cloud architect specializing in AWS infrastructure and automation. Love building scalable and reliable systems.",
            github_url="https://github.com/janesmith",
            linkedin_url="https://linkedin.com/in/janesmith",
            portfolio_url="https://janesmith.io",
            skills=[
                "AWS", "Kubernetes", "Docker", "Terraform", "Python",
                "Ansible", "Jenkins", "GitLab CI", "Monitoring", "Grafana",
                "Prometheus", "ELK Stack", "Linux", "Bash", "CloudFormation"
            ],
            projects=[
                ProjectCreate(
                    title="Infrastructure as Code",
                    description="Complete AWS infrastructure setup using Terraform. Includes VPC, EKS cluster, RDS, and monitoring stack with automated deployment pipeline.",
                    links='{"github": "https://github.com/janesmith/aws-terraform"}'
                ),
                ProjectCreate(
                    title="CI/CD Pipeline",
                    description="GitLab CI/CD pipeline for microservices deployment. Features automated testing, security scanning, and blue-green deployments to Kubernetes.",
                    links='{"github": "https://github.com/janesmith/cicd-pipeline"}'
                )
            ],
            work_experiences=[
                WorkExperienceCreate(
                    company="Cloud Solutions Ltd.",
                    position="Senior DevOps Engineer",
                    description="Designed and maintained cloud infrastructure for multiple clients. Implemented monitoring and alerting systems. Reduced deployment time by 60%.",
                    start_date=datetime(2021, 8, 1),
                    end_date=None
                ),
                WorkExperienceCreate(
                    company="Infrastructure Co.",
                    position="DevOps Engineer",
                    description="Automated deployment processes and managed Kubernetes clusters. Set up monitoring and logging solutions for production systems.",
                    start_date=datetime(2019, 10, 1),
                    end_date=datetime(2021, 7, 31)
                )
            ]
        )
        
        profile_2 = crud.create_profile(db=db, profile=dummy_profile_2)
        print(f"Created profile: {profile_2.name} (ID: {profile_2.id})")
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()