from django import template

register = template.Library()

wrong_words = ['утбол', 'чемп', 'ext']


@register.filter()
def censor(value):
    for _ in range(len(wrong_words)):
        value = value.lower().replace(wrong_words[_].lower(), len(wrong_words[_]) * "*")
    return f'{value}'