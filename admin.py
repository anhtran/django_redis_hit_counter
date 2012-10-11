from django.contrib import admin
from redis_hit_counter.models import HitCount, BlacklistIP, BlacklistUserAgent

class HitCountAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'hits')
admin.site.register(HitCount, HitCountAdmin)


class BlacklistIPAdmin(admin.ModelAdmin):
    list_display = ('ip', 'disable')
    list_editable = ('disable', )
admin.site.register(BlacklistIP, BlacklistIPAdmin)


class BlacklistUserAgentAdmin(admin.ModelAdmin):
    list_display = ('user_agent', 'disable')
    list_editable = ('disable', )
admin.site.register(BlacklistUserAgent, BlacklistUserAgentAdmin)