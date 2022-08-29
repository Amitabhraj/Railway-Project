from django import template
register = template.Library()


@register.filter
def convertint(str_w):
    return int(str_w)



@register.filter
def index(num, i):
    index_number = i-1
    return num[index_number]



@register.filter
def floatconvert(num):
    return float(num)
    




@register.filter
def length(lis):
    return len(lis)
    





