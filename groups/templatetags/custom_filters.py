from django import template
import re

register = template.Library()

@register.filter
def limit_linebreaks(value, max_lines=1):
    lines = value.split("\n")
    filtered_lines = []
    
    line_count = 0
    for line in lines:
        if line.strip():
            filtered_lines.append(line)
            line_count = 0 
        else:
            if line_count < max_lines:
                filtered_lines.append(line)
            line_count += 1

    return "\n".join(filtered_lines)


@register.filter
def mention_to_link(value):
    pattern = r'@(\w+)'
    
    def replace_mention(match):
        username = match.group(1)
        return f'<a href="/@{username}/">@{username}</a>'
    
    return re.sub(pattern, replace_mention, value)