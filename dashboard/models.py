from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class About(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=200)
    years_experience = models.IntegerField(default=0)
    completed_projects = models.IntegerField(default=0)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='about/', blank=True, null=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Skill(models.Model):
    skill = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    years_experience = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.skill

class Qualification(models.Model):
    type = models.CharField(max_length=100)
    diploma = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.diploma

class Service(models.Model):
    service = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service

class Testimonial(models.Model):
    author = models.CharField(max_length=200)
    testimonial = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author
