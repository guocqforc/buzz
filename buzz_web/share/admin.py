from django.contrib import admin

from models import Role, Person, Config, Alarm


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')

admin.site.register(Role, RoleAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'role_list')

    def role_list(self, obj):
        return ','.join([role.name for role in obj.roles.all()])

admin.site.register(Person, PersonAdmin)


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('stat_name', 'number_cmp', 'number_value', 'slope_cmp', 'slope_value', 'role_list', 'person_list', 'valid')
    list_filter = ['stat_name']

    def role_list(self, obj):
        return ','.join([role.name for role in obj.roles.all()])

    def person_list(self, obj):
        return ','.join([person.name for person in obj.persons.all()])

admin.site.register(Config, ConfigAdmin)


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('config', 'create_time', 'number_value', 'slope_value', 'notified')
    list_filter = ['config__stat_name']
    ordering = ['-id']

admin.site.register(Alarm, AlarmAdmin)
