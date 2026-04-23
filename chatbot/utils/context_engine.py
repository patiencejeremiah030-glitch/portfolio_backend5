"""
Context Engine for building AI context from portfolio data.

This utility fetches data from Profile, About, and Projects models
and builds a structured context string for the AI chatbot.
"""

import logging
from django.utils import timezone
from core.models import Profile, Home, About, Project

logger = logging.getLogger(__name__)


def build_context_string():
    """
    Build a comprehensive context string from portfolio data.
    
    This function fetches all relevant portfolio information and formats it
    into a structured string that can be injected into AI system prompts.
    
    Returns:
        str: Formatted context string containing portfolio information
    """
    context_parts = []
    
    # Profile Information
    profile = Profile.objects.first()
    if profile:
        profile_context = _format_profile_context(profile)
        context_parts.append(profile_context)
    
    # Home/Hero Information
    home = Home.objects.first()
    if home:
        home_context = _format_home_context(home)
        context_parts.append(home_context)
    
    # About Information
    about = About.objects.first()
    if about:
        about_context = _format_about_context(about)
        context_parts.append(about_context)
    
    # Projects Information
    projects = Project.objects.filter(is_active=True).order_by('order')
    if projects.exists():
        projects_context = _format_projects_context(projects)
        context_parts.append(projects_context)
    
    # Combine all context parts
    if not context_parts:
        full_context = (
            "IMPORTANT: No Profile, Home, About, or active Projects records exist in the database yet. "
            "Politely explain that you do not have published portfolio details to draw from, and suggest "
            "using the site's contact page if available."
        )
    else:
        full_context = "\n\n".join(context_parts)

    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    full_context += f"\n\n[Context generated at: {current_time}]"

    return full_context


def _format_profile_context(profile):
    """Format profile data for context."""
    context = "=== PROFILE INFORMATION ===\n"
    context += f"Name: {profile.name}\n"
    context += f"Title: {profile.title}\n"
    context += f"Bio: {profile.bio}\n"
    
    social_links = []
    if profile.github:
        social_links.append(f"GitHub: {profile.github}")
    if profile.linkedin:
        social_links.append(f"LinkedIn: {profile.linkedin}")
    if profile.twitter:
        social_links.append(f"Twitter: {profile.twitter}")
    
    if social_links:
        context += "Social Links:\n" + "\n".join(f"  - {link}" for link in social_links)
    
    return context


def _format_home_context(home):
    """Format home/hero data for context."""
    context = "=== HOME PAGE (HERO SECTION) ===\n"
    context += f"Headline: {home.headline}\n"
    if home.subheadline:
        context += f"Subheadline: {home.subheadline}\n"
    if home.hero_description:
        context += f"Hero description: {home.hero_description}\n"
    if home.features_title or home.features_description:
        context += "Features section:\n"
        if home.features_title:
            context += f"  Title: {home.features_title}\n"
        if home.features_description:
            context += f"  Description: {home.features_description}\n"
    if home.cta_title or home.cta_description:
        context += "Call to action:\n"
        if home.cta_title:
            context += f"  Title: {home.cta_title}\n"
        if home.cta_description:
            context += f"  Description: {home.cta_description}\n"
    if home.resume_link:
        context += f"Resume Link: {home.resume_link}\n"

    return context


def _format_about_context(about):
    """Format about data for context."""
    context = "=== ABOUT INFORMATION ===\n"
    context += f"Title: {about.title}\n"
    context += f"Description: {about.description}\n"
    
    if about.experience:
        context += f"Experience: {about.experience}\n"
    
    if about.skills:
        skills_list = about.get_skills_list()
        context += f"Skills: {', '.join(skills_list)}\n"
    
    return context


def _format_projects_context(projects):
    """Format projects data for context."""
    context = "=== PROJECTS ===\n"
    
    for i, project in enumerate(projects, 1):
        context += f"\n{i}. {project.title}\n"
        context += f"   Description: {project.description}\n"
        
        if project.is_featured:
            context += "   [Featured Project]\n"
        
        links = []
        if project.live_link:
            links.append(f"Live: {project.live_link}")
        if project.github_link:
            links.append(f"GitHub: {project.github_link}")
        
        if links:
            context += "   Links: " + " | ".join(links)
    
    return context


def get_context_summary():
    """
    Get a brief summary of available context data.
    
    Returns:
        dict: Summary of available portfolio data
    """
    summary = {
        'has_profile': Profile.objects.exists(),
        'has_home': Home.objects.exists(),
        'has_about': About.objects.exists(),
        'project_count': Project.objects.filter(is_active=True).count(),
    }
    
    # Add profile name if available
    profile = Profile.objects.first()
    if profile:
        summary['profile_name'] = profile.name
        summary['profile_title'] = profile.title
    
    return summary
