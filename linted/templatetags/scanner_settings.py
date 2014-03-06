from django import template

register = template.Library()


@register.simple_tag
def get_property_value(settings, ruleset, rule, property):
    return settings.get_property_value(ruleset, rule, property)

@register.simple_tag
def get_checkbox_checked(settings, ruleset, rule, property):
    return 'checked' if get_property_value(settings, ruleset, rule, property) else ''