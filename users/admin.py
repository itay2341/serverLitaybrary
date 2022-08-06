from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.forms import Textarea
from .models import NewUser

class UserAdminConfig(UserAdmin):
    # model = NewUser
    search_fields = ('email','name',)
    list_filter = ('is_active', 'is_staff','groups')
    ordering = ('-start_date',)
    list_display = ('name','email','start_date','last_login','birth_day','phone','gender', 'is_active','email_is_verify', 'is_staff','is_superuser','otp')
    fieldsets = (
        (None,{'fields':('email','name','password')}),
        ('Permissions',{'fields':('is_staff','is_active','email_is_verify','groups')}),
        ('Personal',{'fields':('phone','birth_day','gender')}),
    )
    # formfield_overrides = {
    #     NewUser.about: {'widget':Textarea(attrs={'rows':10,'cols':40})},
    # }
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','password1','password2','is_active','is_staff')
        }),
    )



admin.site.register(NewUser,UserAdminConfig)