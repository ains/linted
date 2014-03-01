from django import template

register = template.Library()

@register.simple_tag
def get_property_value(settings, ruleset, rule, property):
    return settings.get_property_value(ruleset, rule, property)