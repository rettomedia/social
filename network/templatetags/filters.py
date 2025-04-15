from django import template
import re

register = template.Library()

@register.filter
def mention_to_link(value):
    pattern = r'@(\w+)'
    
    def replace_mention(match):
        username = match.group(1)
        return f'<a href="/@{username}/">@{username}</a>'
    
    return re.sub(pattern, replace_mention, value)