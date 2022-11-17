from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)
    bio = models.TextField(null=True, blank=True)
    is_participants = models.BooleanField(default=True, null=True)
    avatar = models.ImageField(default='default.png')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    
    
    def __str__(self):
        return self.email
    
    



class Event(models.Model):
    participants = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    description  = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)
    event_deadline = models.DateTimeField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)



    def __str__(self):
        return self.name 
    
    
    
    
class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    details = models.TextField(null=True, blank=True)
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.event)  + ' --- ' + str(self.participant) 
    
    