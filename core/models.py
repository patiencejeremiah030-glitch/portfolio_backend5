"""
Core models for portfolio data: Profile, Home, About, Project.
"""

from django.db import models


class Profile(models.Model):
    """
    User profile information displayed on the portfolio.
    """
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    about_image = models.ImageField(upload_to='about/', blank=True, null=True)
    
    # Social links
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one profile exists
        if not self.pk and Profile.objects.exists():
            # If trying to create a new one, update the existing instead
            existing = Profile.objects.first()
            if existing:
                # Copy data to existing and save
                for field in ['name', 'title', 'bio', 'profile_image', 'about_image', 'github', 'linkedin', 'twitter']:
                    setattr(existing, field, getattr(self, field))
                existing.save()
                return
        return super().save(*args, **kwargs)


class Home(models.Model):
    """
    Home page hero section content.
    """
    headline = models.CharField(max_length=200)
    subheadline = models.CharField(max_length=500, blank=True, null=True)
    hero_description = models.TextField(blank=True, null=True)
    features_title = models.CharField(max_length=200, blank=True, null=True)
    features_description = models.TextField(blank=True, null=True)
    cta_title = models.CharField(max_length=200, blank=True, null=True)
    cta_description = models.TextField(blank=True, null=True)
    hero_image = models.ImageField(upload_to='home/', blank=True, null=True)
    resume_link = models.URLField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Home'
        verbose_name_plural = 'Home'
    
    def __str__(self):
        return self.headline
    
    def save(self, *args, **kwargs):
        # Ensure only one home entry exists
        if not self.pk and Home.objects.exists():
            # If trying to create a new one, update the existing instead
            existing = Home.objects.first()
            if existing:
                for field in [
                    'headline', 'subheadline', 'hero_description',
                    'features_title', 'features_description', 'cta_title', 'cta_description',
                    'hero_image', 'resume_link',
                ]:
                    setattr(existing, field, getattr(self, field))
                existing.save()
                return
        return super().save(*args, **kwargs)


class About(models.Model):
    """
    About page content.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    experience = models.TextField(blank=True, null=True)
    skills = models.TextField(help_text='Comma-separated list of skills')
    about_image = models.ImageField(upload_to='about/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'
    
    def __str__(self):
        return self.title
    
    def get_skills_list(self):
        """Return skills as a list."""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    def save(self, *args, **kwargs):
        # Ensure only one about entry exists
        if not self.pk and About.objects.exists():
            # If trying to create a new one, update the existing instead
            existing = About.objects.first()
            if existing:
                for field in ['title', 'description', 'experience', 'skills', 'about_image']:
                    setattr(existing, field, getattr(self, field))
                existing.save()
                return
        return super().save(*args, **kwargs)


class Project(models.Model):
    """
    Project showcase items.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    live_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    
    # Ordering
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower first)')
    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    is_active = models.BooleanField(default=True, help_text='Show in listings')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
