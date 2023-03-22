from django.db import models
import datetime
import django


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

    def get_duration(self) -> datetime.timedelta:

        leaved_time = django.utils.timezone.localtime(self.leaved_at)
        time_in_storage = leaved_time - self.entered_at

        return time_in_storage

    def is_long(self, minutes: int = 60) -> bool:
        result = False

        visit_duration = self.get_duration()
        visit_minutes = visit_duration.total_seconds() // 60
        if visit_minutes > minutes:
            result = True

        return result


def format_duration(duration: datetime.timedelta) -> str:
    days = duration.days
    seconds = duration.seconds

    minutes = seconds // 60

    hours = minutes // 60
    minutes = minutes % 60

    dur_string = f'{hours} ч {minutes} мин'
    if days:
        dur_string = f'{days} день - ' + dur_string

    return dur_string
