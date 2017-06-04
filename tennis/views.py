from django.db import models
from tennis.models import Speler
from django.shortcuts import render_to_response
from django.template import RequestContext

gg = lambda x: (x.punten_per_game(), x.score(), x.punten)

def index(request, kinderen=False):
    if kinderen:
        spelers = Speler.objects.filter(~models.Q(speelsterkte__gt=1))
    else:
        spelers = Speler.objects.filter(~models.Q(speelsterkte=1))

    return render_to_response('index.html', {
        'spelers':sorted(spelers, key=gg, reverse=True)
    }, context_instance=RequestContext(request))
