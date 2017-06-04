from django import template

register = template.Library()

@register.simple_tag
def henk(speler):
    return speler.matches1.get(speler2=arg).spel_nummer

@register.filter(name='is_match')
def is_match(value, arg):
    print value.matches1.filter(speler2=arg)
    return value.matches1.filter(speler2=arg).exists()