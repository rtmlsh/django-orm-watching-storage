from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []

    for visit in visits:
        duration = get_duration(visit)
        spent_time = format_duration(duration)
        personal_data = {
            'who_entered': visit.passcard,
            'entered_at': visit.entered_at,
            'duration': spent_time

        }
        non_closed_visits.append(personal_data)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
