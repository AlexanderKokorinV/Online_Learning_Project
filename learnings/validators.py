import re

from rest_framework import serializers


class YoutubeOnlyValidator:
    """Валидатор для проверки на отсутствие в материалах ссылок
    на сторонние ресурсы, кроме youtube.com"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        link_to_check = value.get(self.field)  # Получаем значение проверяемого поля из словаря данных

        if not link_to_check:  # Если поле пустое, пропускаем проверку
            return

        url_pattern = re.compile(
            r"https?://[^\s/$.?#].[^\s]*",  # Регулярное выражение для поиска любых URL-ссылок в тексте
            re.IGNORECASE,
        )

        # Находим все ссылки в тексте
        found_urls = url_pattern.findall(str(link_to_check))

        for url in found_urls:

            url_lower = url.lower()

            is_youtube = "youtube.com" in url_lower

            if not is_youtube:
                raise serializers.ValidationError(
                    {self.field: "Запрещено использовать ссылки на сторонние ресурсы, кроме youtube.com."}
                )
