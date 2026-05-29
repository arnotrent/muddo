from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display  = ['name','username','region','district','status','last_seen']
    list_filter   = ['status','region']
    search_fields = ['user__first_name','user__last_name','user__username']
