from django.apps import AppConfig

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import *
#
#
# class Employe_Admin(admin.ModelAdmin):
#     list_display = ["city", "is_coming", "is_the_owner"]
#     search_fields = ["name", 'city']
#     list_filter = ["city"]
#     list_per_page = 3
#
#
# class ProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = [ProfileInline]
#
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
# admin.site.register(Event)
# admin.site.register(Evaluation)
# admin.site.register(EventJoin)

class EmployeConfig(AppConfig):
    name = 'employe'
