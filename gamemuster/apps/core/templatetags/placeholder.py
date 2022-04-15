from django.template.defaultfilters import register


@register.filter
def placeholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value
