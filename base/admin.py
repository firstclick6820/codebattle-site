from django.contrib import admin

from .models import User, Event, Submission

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    
admin.site.register(User, UserAdmin)




class EventAdmin(admin.ModelAdmin):
    search_fields = ['name', 'event_deadline']
    
admin.site.register(Event, EventAdmin)



class SubmissionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['participant', 'event']
admin.site.register(Submission, SubmissionAdmin)