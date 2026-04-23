"""
Setup script for creating sample data.
Run this after migrations to populate the database with initial data.

Usage:
    python manage.py shell < setup_sample_data.py
"""

from core.models import Profile, Home, About, Project

def create_sample_data():
    """Create sample portfolio data."""
    
    # Create Profile
    if not Profile.objects.exists():
        Profile.objects.create(
            name="Your Name",
            title="Full Stack Developer",
            bio="Passionate developer with expertise in building scalable web applications. "
                "I love creating elegant solutions to complex problems.",
            github="https://github.com/yourusername",
            linkedin="https://linkedin.com/in/yourusername",
            twitter="https://twitter.com/yourusername",
        )
        print("✓ Created Profile")
    else:
        print("○ Profile already exists")
    
    # Create Home
    if not Home.objects.exists():
        Home.objects.create(
            headline="Hello, I'm Your Name",
            subheadline="Building digital experiences that matter",
            resume_link="https://example.com/resume.pdf",
        )
        print("✓ Created Home")
    else:
        print("○ Home already exists")
    
    # Create About
    if not About.objects.exists():
        About.objects.create(
            title="About Me",
            description="I'm a passionate developer with X years of experience in building "
                       "web applications. I specialize in Python, Django, and modern JavaScript frameworks.",
            experience="5+ years of professional experience\n"
                      "Worked with startups and enterprises\n"
                      "Led teams of 5+ developers",
            skills="Python, Django, Django REST Framework, PostgreSQL, React, TypeScript, "
                  "Node.js, Docker, AWS, Git, CI/CD, Agile",
        )
        print("✓ Created About")
    else:
        print("○ About already exists")
    
    # Create Sample Projects
    sample_projects = [
        {
            "title": "E-Commerce Platform",
            "description": "A full-featured e-commerce platform with cart, checkout, and payment integration. "
                          "Built with Django and React.",
            "live_link": "https://example.com",
            "github_link": "https://github.com/yourusername/ecommerce",
            "is_featured": True,
            "order": 1,
        },
        {
            "title": "Task Management App",
            "description": "A collaborative task management application with real-time updates and team features.",
            "live_link": "https://example.com",
            "github_link": "https://github.com/yourusername/taskapp",
            "is_featured": True,
            "order": 2,
        },
        {
            "title": "API Gateway Service",
            "description": "A microservices API gateway with rate limiting, authentication, and request routing.",
            "github_link": "https://github.com/yourusername/api-gateway",
            "is_featured": False,
            "order": 3,
        },
    ]
    
    for project_data in sample_projects:
        project, created = Project.objects.get_or_create(
            title=project_data["title"],
            defaults=project_data
        )
        if created:
            print(f"✓ Created Project: {project.title}")
        else:
            print(f"○ Project exists: {project.title}")
    
    print("\n✓ Sample data setup complete!")
    print("\nNext steps:")
    print("1. Upload images via the admin panel")
    print("2. Update the sample data with your actual information")
    print("3. Access the admin panel at /admin/")

if __name__ == "__main__":
    create_sample_data()
