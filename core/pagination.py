from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Matches the shape the React admin's mock API already returns
    (src/api/mockServer.js `paginate()`), so the frontend needed zero
    changes when pointed at this real backend.
    """
    page_size = 10
    page_size_query_param = "pageSize"
    page_query_param = "page"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "results": data,
            "count": self.page.paginator.count,
            "page": self.page.number,
            "pageSize": self.get_page_size(self.request),
            "totalPages": self.page.paginator.num_pages,
        })
