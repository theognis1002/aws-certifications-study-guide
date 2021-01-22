import pytz
from django import template

register = template.Library()


@register.filter
def question_num(questions):
    res = [question.update({"idx": idx}) for idx, question in enumerate(questions, 1)]
    print(res)
    return [question.update({"idx": idx}) for idx, question in enumerate(questions, 1)]
