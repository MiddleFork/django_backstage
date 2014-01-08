import random
from django import template
register = template.Library()

@register.filter
def random_ad(ads):
    return random.choice(ads)

