from django import template
import datetime

register = template.Library()


@register.filter
def addDays(days):
    newDate = datetime.date.today() + datetime.timedelta(days=days)
    return newDate
