from django import template

register = template.Library()

@register.filter
def get_item(dict, leader):
    return dict[leader]
