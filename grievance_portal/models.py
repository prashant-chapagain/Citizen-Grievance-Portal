from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class GrievanceCategory(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Grievance(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(GrievanceCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='grievance_attachments/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.reference_id} - {self.title}"

class GrievanceResponse(models.Model):
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.grievance.reference_id}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    def __str__(self):
        return self.user.username