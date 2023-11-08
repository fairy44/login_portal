from django.contrib import admin
from mainApp.models import Users,TimeHistory
from django.contrib.sites.models import Site

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=('Username','First_name','Last_name','Password','Email_Address')

class TimeAdmin(admin.ModelAdmin):
    # list_display=('Username_ID','Email_Address','Login_Time','Logout_Time')
    list_display=('Username','Password','login_time','logout_time','login_method','user','google_id')






admin.site.register(Users,UserAdmin)
admin.site.register(TimeHistory,TimeAdmin)
