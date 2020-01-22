from django.contrib import admin

from .models import Slack, SlackRequest
# Register your models here.
# @admin.register(Slack)
# class InstallationAdmin(admin.ModelAdmin):
#     list_display = ('domain', 'api_app_id', 'is_active')

admin.site.register(Slack)
@admin.register(SlackRequest)
class ScoreRequestAdmin(admin.ModelAdmin):
    list_display = ('installation', 'message', 'is_complete')