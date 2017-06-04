from django.contrib import admin
from tennis import models

admin.site.register(models.Speler)

# class henkInline(admin.StackedInline):
#     model = models.Team
#
# class HenkAdmin(admin.ModelAdmin):
#     inlines = [henkInline]

#
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'uitslag', 'kindermatch', 'klaar')
    list_editable = ('klaar',)
    list_filter = ('kindermatch', 'klaar')

admin.site.register(models.Team)
admin.site.register(models.Match, MatchAdmin)