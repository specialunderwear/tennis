from __future__ import division
from django.db import models


class Speler(models.Model):
    naam = models.CharField(max_length=512)
    speelsterkte = models.IntegerField()

    def score(self):
        return sum(self.matches1.filter(score__isnull=False).values_list('score', flat=True) or [], 0) + \
            sum(self.matches2.filter(score__isnull=False).values_list('score', flat=True) or [], 0)

    def punten_per_game(self):
        try:
            return self.punten / self.games()
        except:
            return 0

    @property
    def punten(self):
        if self.speelsterkte == 1:
            return sum([a.punten1() for a in Match.objects.filter(models.Q(team1__speler1=self)|models.Q(team1__speler2=self), klaar=True).distinct()]) + \
                   sum([a.punten2() for a in Match.objects.filter(models.Q(team2__speler1=self)|models.Q(team2__speler2=self), klaar=True).distinct()])
        else:
            return sum([a.punten1() for a in Match.objects.filter(models.Q(team1__speler1=self)|models.Q(team1__speler2=self), klaar=True, kindermatch=False).distinct()]) + \
                   sum([a.punten2() for a in Match.objects.filter(models.Q(team2__speler1=self)|models.Q(team2__speler2=self), klaar=True, kindermatch=False).distinct()])

    def games(self):
        if self.speelsterkte == 1:
            return Match.objects.filter(models.Q(team1__speler1=self)|models.Q(team1__speler2=self)).distinct().count() + \
            Match.objects.filter(models.Q(team2__speler1=self)|models.Q(team2__speler2=self)).distinct().count()
        else:
            return Match.objects.filter(models.Q(team1__speler1=self)|models.Q(team1__speler2=self), kindermatch=False).distinct().count() + \
            Match.objects.filter(models.Q(team2__speler1=self)|models.Q(team2__speler2=self), kindermatch=False).distinct().count()

    def __unicode__(self):
        return "%s: %s(%s)" % (self.speelsterkte, self.naam, self.games())

    def matches(self):
        if self.speelsterkte == 1:
            return self.matches1.count() + self.matches2.count()
        else:
            return self.matches1.filter(models.Q(teams1__kindermatch=False)|models.Q(teams2__kindermatch=False)).count() + \
                self.matches2.filter(models.Q(teams1__kindermatch=False)|models.Q(teams2__kindermatch=False)).count()


class Team(models.Model):
    speler1 = models.ForeignKey(Speler, related_name='matches1')
    speler2 = models.ForeignKey(Speler, related_name='matches2')

    score = models.IntegerField(blank=True, null=True)

    def speelsterkte(self):
        return (
            self.speler1.speelsterkte + self.speler2.speelsterkte,
            self.speler3.speelsterkte + self.speler4.speelsterkte,
        )

    def __unicode__(self):
        return "%i %s en %s" % (self.id, self.speler1, self.speler2)


class Match(models.Model):
    team1 = models.ForeignKey(Team, related_name='teams1')
    team2 = models.ForeignKey(Team, related_name='teams2')
    klaar = models.BooleanField(default=False)
    kindermatch = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s vs %s [%s]" % (self.team1, self.team2, self.uitslag())

    def punten1(self):
        if self.team1.score > self.team2.score:
            return 3
        elif self.team1.score < self.team2.score:
            return 0
        return 1

    def punten2(self):
        if self.team1.score > self.team2.score:
            return 0
        elif self.team1.score < self.team2.score:
            return 3
        return 1

    def uitslag(self):
        return "%s - %s" % (self.team1.score or 0, self.team2.score or 0)

    class Meta:
        ordering = ('id',)
