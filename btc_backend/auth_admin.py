from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from btc_backend.admin_site import btc_admin

btc_admin.register(Group, GroupAdmin)
