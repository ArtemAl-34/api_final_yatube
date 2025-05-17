from rest_framework.pagination import LimitOffsetPagination


class PostPagination(LimitOffsetPagination):
    """Класс пагинации для публикаций."""
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
