from django.contrib import admin

from .models import SubscriptionPlan, Support, User

admin.site.register(User)
admin.site.register(SubscriptionPlan)
admin.site.register(Support)
