import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
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
