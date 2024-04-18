import re

# Ваша строка
s = "4.2"

# Ваш шаблон регулярного выражения
pattern = r"(\d{1,2})(\.\d{1,2})?(\.?\d{1,2})?"

# Ищем совпадение
match = re.search(pattern, s)

print(match.group(1))
