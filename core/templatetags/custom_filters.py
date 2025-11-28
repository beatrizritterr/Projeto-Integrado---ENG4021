# Arquivo: core/templatetags/custom_filters.py

from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acessar o valor de um dicionário por chave no template."""
    return dictionary.get(key)