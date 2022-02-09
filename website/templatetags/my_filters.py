# -*- encoding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from tools.utils import change_comma_by_dot


register = template.Library()


def currency(real):
    real = round(float(change_comma_by_dot(real)), 2)

    return "$%s%s" % (intcomma(int(real)), ("%0.2f" % real)[-3:])


register.filter("currency", currency)


def limit_character(words):
    words = words[:20] if words else ""
    return words


register.filter("limit_character", limit_character)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.pop('page', None)
    query.update(kwargs)
    return query.urlencode()
