from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        duration = get_duration(visit)
        spent_time = format_duration(duration)
        answer = is_visit_long(spent_time)
        personal_data = {
            'entered_at': visit.entered_at,
            'duration': spent_time,
            'is_strange': answer
        }
        this_passcard_visits.append(personal_data)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
