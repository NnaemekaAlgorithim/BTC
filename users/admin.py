from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from btc_backend.admin_site import btc_admin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "phone_number", "btc_balance", "referral_code", "referral_count", "date_joined", "is_staff")
    list_filter = ("is_staff", "is_active", "agreed_to_terms")
    search_fields = ("email", "phone_number", "referral_code")
    ordering = ("-date_joined",)
    readonly_fields = ("id", "referral_code", "date_joined", "btc_balance", "referral_count")

    fieldsets = (
        (None, {"fields": ("id", "email", "phone_number", "password")}),
        ("BTC & Referral", {"fields": ("btc_balance", "referral_code", "referred_by")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "agreed_to_terms", "groups", "user_permissions")}),
        ("Dates", {"fields": ("date_joined", "last_login")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number", "password1", "password2", "agreed_to_terms"),
        }),
    )

    def referral_count(self, obj):
        return obj.referrals.count()
    referral_count.short_description = "Referrals"


btc_admin.register(User, UserAdmin)
