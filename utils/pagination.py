from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response


class UserListPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response(dict([
            ('pagination', {
                'total': self.page.paginator.count,
                'size': self.page_size,
                'page': self.page.number
            }),
            ('results', data)
        ]))
