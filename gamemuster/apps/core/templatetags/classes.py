from django.template.defaultfilters import register


@register.filter
def classes(value, token):
    value.field.widget.attrs["class"] = token
    return value
