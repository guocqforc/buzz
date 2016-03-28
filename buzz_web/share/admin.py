from django.contrib import admin

from models import Role, Config, Alarm


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'flylog_name')

admin.site.register(Role, RoleAdmin)


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('stat_name', 'number_cmp', 'number_value', 'slope_cmp', 'slope_value', 'role_list', 'valid')
    list_filter = ['valid']
    search_fields = ['stat_name']

    def role_list(self, obj):
        return ','.join([role.name for role in obj.roles.all()])

admin.site.register(Config, ConfigAdmin)


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('config', 'create_time', 'number_value', 'slope_value', 'notified')
    list_filter = ['config__stat_name']
    ordering = ['-id']

admin.site.register(Alarm, AlarmAdmin)
