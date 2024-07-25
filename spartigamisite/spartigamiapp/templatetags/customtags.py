from django import template

register = template.Library()

@register.filter
def find_score_pair_index(high, low):
    return (high * (high + 1) // 2) + low

@register.filter
def index(data, idx):
    try:
        return data[idx]
    except IndexError:
        return None