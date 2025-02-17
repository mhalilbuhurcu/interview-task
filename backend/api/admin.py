from django.contrib import admin
from .models import Influencer, SocialMediaAccount

@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['influencer', 'platform', 'username', 'followers_count', 'last_updated']
    list_filter = ['platform']
    search_fields = ['username', 'influencer__full_name']

@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'status', 'created_at', 'get_content_types']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'email']
    
    def get_content_types(self, obj):
        return ", ".join(obj.content_types)
    get_content_types.short_description = 'Content Types'
