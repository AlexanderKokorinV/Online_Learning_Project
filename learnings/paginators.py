from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    """Пагинатор для списка курсов"""

    page_size = 5  # Количество курсов на одной странице по умолчанию
    page_size_query_param = "page_size"  # Позволяет клиенту менять размер страницы через URL (?page_size=10)
    max_page_size = 50  # Максимально разрешенный размер страницы для клиента


class LessonPagination(PageNumberPagination):
    """Пагинатор для списка уроков"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
