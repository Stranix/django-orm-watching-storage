import django

from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render


def storage_information_view(request):

    all_active_visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visit in all_active_visits:
        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': django.utils.timezone.localtime(visit.entered_at),
            'duration': format_duration(visit.get_duration()),
            'is_strange': visit.is_long()
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
