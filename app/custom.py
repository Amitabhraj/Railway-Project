from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]



@register.filter
def convertint(str_w):
    return int(str_w)
    