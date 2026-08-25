from django.contrib import admin
from mining.models import MiningStage, MinerProfile


@admin.register(MiningStage)
class MiningStageAdmin(admin.ModelAdmin):
    list_display = ["name", "display_order", "published"]
    list_filter = ["published"]
    search_fields = ["name", "description"]


@admin.register(MinerProfile)
class MinerProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "years_active", "featured", "published", "display_order"]
    list_filter = ["published", "featured"]
    search_fields = ["name", "story"]
