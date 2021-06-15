# Проверка введёных значений на тип данных(числа) и соответствие диапазону значений
from telegram.ext import ConversationHandler


def validator(text, min_value, max_value):
    if (text != "I don't know") and (text != ConversationHandler.END):
        try:
            value = int(text)
        except (TypeError, ValueError):
            return None

        if value < min_value or value > max_value:
            return None
        else:
            return value
    return text


# Замена наименований пола на индекс в запросе
def replacing_sex(value):
    if value == 'man':
        value = 2
    if value == 'woman':
        value = 1
    if value == 'any':
        value = 0
    return value


# Замена наименований статуса на индекс в запросе
def replacing_status(value):
    if value == 'not married (not married)':
        value = 1
    if value == 'meets':
        value = 2
    if value == 'engaged':
        value = 3
    if value == 'married':
        value = 4
    if value == "it's complicated":
        value = 5
    if value == 'in active search':
        value = 6
    if value == 'lover':
        value = 7
    if value == 'in civil marriage':
        value = 8
    return value
