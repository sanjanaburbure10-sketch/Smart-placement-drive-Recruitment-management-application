from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


    degree = models.CharField(max_length=50, null=True, blank=True)
    cgpa = models.FloatField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    def __str__(self):
        return self.email


class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    min_cgpa = models.FloatField()

    def __str__(self):
        return self.title


class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Applied")
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return f"{self.student.email} -> {self.job.title}"
    
class SavedJob(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

class SavedJob(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)