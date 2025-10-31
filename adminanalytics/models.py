from django.db import models

import uuid

class GameSession(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_ms = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    shots_fired = models.IntegerField(default=0)
    enemies_destroyed =models.IntegerField(default=0)
    client_tag = models.CharField(max_length=64,blank=True)
    user_agent = models.TextField(blank=True)
    meta = models.JSONField(default=dict,blank = True)
    class Meta:
        indexes = [
                models.Index(fields=["started_at"]),
                models.Index(fields=["ended_at"]),
                models.Index(fields=["score"]),
                models.Index(fields=["client_tag"]),  
            ]
    def __str__(self):
        return f"{self.id} score={self.score}"