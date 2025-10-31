from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GameSession

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("id","started_at","ended_at","score","duration_ms","client_tag")
    list_filter = ("started_at",)
    search_fields = ("id","client_tag","user_agent")