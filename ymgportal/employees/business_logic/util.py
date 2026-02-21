from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def get_active_users():
    now = timezone.now()

    # 1. Auto-delete expired sessions (fixes your problem)
    Session.objects.filter(expire_date__lt=now).delete()

    # 2. Fetch only active (non-expired) sessions
    active_sessions = Session.objects.filter(expire_date__gt=now)

    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        uid = data.get("_auth_user_id")
        if uid:
            user_ids.append(uid)

    return User.objects.filter(id__in=user_ids)
