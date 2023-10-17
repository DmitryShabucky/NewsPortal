from django import template

register = template.Library()

censored_words = [
    'первая', 'часть', 'современная', 'игры', 'жизни', 'масса', 'опыт', 'здесь', 'также', 'информация', 'python', 'обе',
    'многие', 'продажи', 'могут', 'google', 'деньги', 'официально', 'ласточка', 'сайт', 'номер', 'производитель',
    'Jaecoo', 'сочетание',
]
@register.filter()
def censor(text):
    censored_text = []
    try:
        for i in text.split():
            capital = i.capitalize()
            low = i.lower()
            if capital in censored_words or low in censored_words:
                word = i[0] + "*" * (len(i)-1)
                censored_text.append(word)
            else:
                censored_text.append(i)

        return " ".join(censored_text)
    except Exception:
        return f"{ValueError} Censor() filter can be used only with strings!!!"

