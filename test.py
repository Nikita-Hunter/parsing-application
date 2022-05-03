import json

with open("posts_dict.json") as file:
    posts_dict = json.load(file)
search_id = "utochnennaya-massa-w-boasdasda"

if search_id in posts_dict:
    print("Запись уже есть в словаре")
else:
    print("Свежая запись, добавляется в словарь")