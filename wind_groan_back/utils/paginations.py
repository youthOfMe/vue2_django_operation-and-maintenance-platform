from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    # 重写响应器
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'page': self.page.number,  # 当前页码
                'size': self.page_size,  # 每页多少个
            },
            'results': data
        })