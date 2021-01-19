from django.contrib import admin
from .models import Support, User, SubscriptionPlan


admin.site.register(User)
admin.site.register(SubscriptionPlan)
admin.site.register(Support)