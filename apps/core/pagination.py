from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class SmallPagination(PageNumberPagination):
    """For dropdowns and small lists."""
    page_size = 10
    max_page_size = 50


class LargePagination(PageNumberPagination):
    """For admin exports."""
    page_size = 100
    max_page_size = 500