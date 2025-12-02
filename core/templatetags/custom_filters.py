# Arquivo: core/templatetags/custom_filters.py

from django import template
register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Acessa um item de um dicionário. Ex: {{ meu_dicionario|get_item:chave }}
    """
    return dictionary.get(key)

