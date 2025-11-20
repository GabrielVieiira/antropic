from django.db import models
from django.utils import timezone

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, user=None):
        return super().update(deleted_at=timezone.now(), deleted_by=user)

    def hard_delete(self):
        return super().delete()

    def alive(self) -> models.QuerySet:
        return self.filter(deleted_at__isnull=True)

    def dead(self) -> models.QuerySet:
        return self.filter(deleted_at__isnull=False)