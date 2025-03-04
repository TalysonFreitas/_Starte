from django import template
from rolepermissions.roles import get_user_roles

register = template.Library()

@register.filter
def has_role(user, role_name):
    """Verifica se o usuário tem um papel específico"""
    return role_name in [role.get_name() for role in get_user_roles(user)]
