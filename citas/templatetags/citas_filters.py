from django import template

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    """Divide el valor dado por 100 y retorna el resultado."""
    try:
        return float(value) / 100
    except (ValueError, TypeError):
        return value  # Si ocurre un error, retorna el valor original
