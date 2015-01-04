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
