from django.contrib.admin import AdminSite
from django.db.models import Count, Sum
from django.utils import timezone


class BTCAdminSite(AdminSite):
    site_header = "BTC — Big Terms & Conditions"
    site_title = "BTC Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["btc_stats"] = self._collect_stats()
        return super().index(request, extra_context)

    def _collect_stats(self):
        from tasks.models import Task, UserTaskCompletion
        from users.models import User

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = now - timezone.timedelta(days=7)

        total_users = User.objects.count()
        total_btc = User.objects.aggregate(total=Sum("btc_balance"))["total"] or 0
        total_referrals = User.objects.filter(referred_by__isnull=False).count()
        new_today = User.objects.filter(date_joined__gte=today_start).count()
        new_this_week = User.objects.filter(date_joined__gte=week_ago).count()

        total_task_completions = UserTaskCompletion.objects.count()
        btc_from_tasks = UserTaskCompletion.objects.aggregate(
            total=Sum("btc_earned")
        )["total"] or 0
        tasks_today = UserTaskCompletion.objects.filter(completed_at__gte=today_start).count()

        top_referrers = (
            User.objects.annotate(ref_count=Count("referrals"))
            .filter(ref_count__gt=0)
            .order_by("-ref_count")
            .values("email", "ref_count", "btc_balance")[:5]
        )

        top_earners = (
            User.objects.filter(btc_balance__gt=0)
            .order_by("-btc_balance")
            .values("email", "btc_balance", "referral_code")[:5]
        )

        active_tasks = Task.objects.filter(is_active=True).count()

        recent_users = (
            User.objects.order_by("-date_joined")
            .values("email", "phone_number", "date_joined", "btc_balance")[:10]
        )

        return {
            # headline numbers
            "total_users": total_users,
            "total_btc_distributed": total_btc,
            "total_referrals": total_referrals,
            "new_users_today": new_today,
            "new_users_this_week": new_this_week,
            # tasks
            "total_task_completions": total_task_completions,
            "btc_from_tasks": btc_from_tasks,
            "tasks_today": tasks_today,
            "active_tasks": active_tasks,
            # tables
            "top_referrers": list(top_referrers),
            "top_earners": list(top_earners),
            "recent_users": list(recent_users),
        }


btc_admin = BTCAdminSite(name="btc_admin")
