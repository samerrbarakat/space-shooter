import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import GameSession
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Max, Count
from django.db.models.functions import TruncHour, ExtractHour
from django.shortcuts import render
from .models import GameSession

@csrf_exempt
def session_start(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    data = json.loads(request.body or "{}")
    s = GameSession.objects.create(
        client_tag=data.get("clientTag",""),
        user_agent=request.META.get("HTTP_USER_AGENT",""),
        meta={"ip": request.META.get("REMOTE_ADDR")}
    )
    return JsonResponse({"sessionId": str(s.id)})

@csrf_exempt
def session_end(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    data = json.loads(request.body or "{}")
    sid = data.get("sessionId")
    if not sid:
        return HttpResponseBadRequest("Missing sessionId")
    try:
        s = GameSession.objects.get(pk=sid)
    except GameSession.DoesNotExist:
        return HttpResponseBadRequest("Invalid sessionId")

    s.ended_at = timezone.now()
    s.score = int(data.get("score", 0))
    s.shots_fired = int(data.get("shotsFired", 0))
    s.enemies_destroyed = int(data.get("enemiesDestroyed", 0))
    s.duration_ms = int(data.get("durationMs", max(0, (s.ended_at - s.started_at).total_seconds()*1000)))
    s.save()
    return JsonResponse({"ok": True})


@staff_member_required
def admin_dashboard(request):
    now = timezone.now()
    qs = GameSession.objects.all()

    totals = {
        "sessions": qs.count(),
        "avg_score": round(qs.aggregate(Avg("score"))["score__avg"] or 0, 2),
        "max_score": qs.aggregate(Max("score"))["score__max"] or 0,
        "avg_duration_s": round((qs.aggregate(Avg("duration_ms"))["duration_ms__avg"] or 0)/1000, 1),
    }

    last_hour_cnt = qs.filter(started_at__gte=now - timedelta(hours=1)).count()

    # last 24h, grouped per hour
    ts24 = (qs.filter(started_at__gte=now - timedelta(hours=24))
              .annotate(h=TruncHour("started_at"))
              .values("h").order_by("h")
              .annotate(cnt=Count("id"), avg_score=Avg("score")))

    # peak hours (avg per hour-of-day across last 30 days)
    hod = (qs.filter(started_at__gte=now - timedelta(days=30))
             .annotate(h=ExtractHour("started_at"))
             .values("h").order_by("h")
             .annotate(cnt=Count("id"), avg_score=Avg("score")))

    # top scores (quick leaderboard)
    top_scores = list(qs.order_by("-score").values("score", "started_at")[:5])

    
    unique_players = (qs.exclude(client_tag="")
                        .values("client_tag")
                        .distinct()
                        .count())

    unique_players_24h = (qs.filter(started_at__gte=now - timedelta(hours=24))
                            .exclude(client_tag="")
                            .values("client_tag")
                            .distinct()
                            .count())
    
    ctx = {
        "totals": totals,
        "last_hour_cnt": last_hour_cnt,
        "ts24": list(ts24),
        "hod": list(hod),
        "top_scores": top_scores,
        "unique_players": unique_players,
        "unique_players_24h": unique_players_24h,
    }
    return render(request, "admin/dashboard.html", ctx)