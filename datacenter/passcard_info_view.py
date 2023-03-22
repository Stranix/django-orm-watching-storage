from django.shortcuts import render
from django.shortcuts import get_object_or_404

from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    all_passcard_visits = Visit.objects.filter(passcard=passcard)
    formatted_passcard_visits = _get_format_visits_for_passcard_view(all_passcard_visits)

    context = {
        'passcard': passcard.owner_name,
        'this_passcard_visits': formatted_passcard_visits
    }
    return render(request, 'passcard_info.html', context)


def _get_format_visits_for_passcard_view(visits: list[Visit]):
    formatted_visits = []
    for visit in visits:
        formatted_visits.append({
            'entered_at': visit.entered_at,
            'duration': format_duration(visit.get_duration()),
            'is_strange': visit.is_long()
        })
    return formatted_visits
