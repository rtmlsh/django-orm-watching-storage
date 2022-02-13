import django
import datetime
from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    entered_at, leaved_at = django.utils.timezone.localtime(visit.entered_at), \
                            django.utils.timezone.localtime(visit.leaved_at)
    duration = leaved_at - entered_at
    return duration


def format_duration(duration):
    seconds, minutes = 3600, 60
    spent_hours = duration.total_seconds() // seconds
    spent_minutes = (duration.total_seconds() % seconds) // minutes
    spent_time = datetime.timedelta(hours=spent_hours, minutes=spent_minutes)
    return spent_time