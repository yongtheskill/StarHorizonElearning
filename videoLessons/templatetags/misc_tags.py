from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines
import base64

register = template.Library()

def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ''))
remove_newlines.is_safe = True
remove_newlines = stringfilter(remove_newlines)
register.filter(remove_newlines)


def b64encode(text):
    normalized_text = normalize_newlines(text)
    normalized_text = normalized_text.replace('\n', '').encode('utf-8')
    return mark_safe(base64.b64encode(normalized_text).decode('ascii'))
b64encode.is_safe = True
b64encode = stringfilter(b64encode)
register.filter(b64encode)