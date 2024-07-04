from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Workout)
admin.site.register(Lift)
admin.site.register(Movement)
admin.site.register(Set)
admin.site.register(TrainingZone)
admin.site.register(FollowRequest)
admin.site.register(Plan)