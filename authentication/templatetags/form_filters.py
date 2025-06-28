from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Adds the given CSS class to a form field widget without removing existing ones.
    Handles multiple classes and preserves existing widget attributes.
    """
    if hasattr(field, 'field') and hasattr(field.field.widget, 'attrs'):
        existing_classes = field.field.widget.attrs.get('class', '')
        new_classes = f"{existing_classes} {css_class}".strip()
        return field.as_widget(attrs={"class": new_classes})
    return field
