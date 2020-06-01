from django import template

register = template.Library()


@register.filter(name="class")
def add_css(field, classname):
    return field.as_widget(attrs={'class': classname})


@register.simple_tag
def verbose_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter
def multiply(arg1, arg2):
    return float(arg1) * float(arg2)


@register.filter
def divide(arg1, arg2):
    if arg2 == 0:
        return 0
    return float(arg1) / float(arg2)


@register.simple_tag
def define(val=None):
    return val
