from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FlexiblePageNumberPagination(PageNumberPagination):
    """Personnaliser la réponse pour inclure les détails de pagination"""

    # Taille de la page par défaut
    page_size = 4

    # Permettre de spécifier la taille de la page dans la requête
    page_size_query_param = 'page_size'

    # Taille maximale de la page
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page.paginator.per_page,
            'results': data
        })
