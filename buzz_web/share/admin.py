from django.contrib import admin

from models import Role, Person, Config, Alarm


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Role, RoleAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')

admin.site.register(Person, PersonAdmin)


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('stat_name', 'number_op', 'number_value', 'slope_op', 'slope_value')
    list_filter = ['stat_name']

admin.site.register(Config, ConfigAdmin)


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('config', 'create_time', 'number_value', 'slope_value', 'notified')
    list_filter = ['config__stat_name']
    ordering = ['-id']

admin.site.register(Alarm, AlarmAdmin)
