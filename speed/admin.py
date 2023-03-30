from django.contrib import admin

from .models import SpeedLimit, UserInfo, Vehicle, Penalty

class ExtraInfoAdmin(admin.ModelAdmin):
    model = UserInfo
    search_fields = ('user__username',)


admin.site.register(SpeedLimit)
admin.site.register(UserInfo, ExtraInfoAdmin)
admin.site.register(Vehicle)
admin.site.register(Penalty)


