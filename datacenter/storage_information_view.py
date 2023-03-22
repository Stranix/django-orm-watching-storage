import django

from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render


def storage_information_view(request):

    all_active_visits = Visit.objects.filter(leaved_at__isnull=True)
    formatted_non_closed_visits = _get_format_visits_for_storage_view(all_active_visits)

    context = {
        'non_closed_visits': formatted_non_closed_visits,
    }
    return render(request, 'storage_information.html', context)


def _get_format_visits_for_storage_view(visits: list[Visit]):
    formatted_visits = []
    for visit in visits:
        formatted_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': django.utils.timezone.localtime(visit.entered_at),
            'duration': format_duration(visit.get_duration()),
            'is_strange': visit.is_long()
        })
    return formatted_visits
