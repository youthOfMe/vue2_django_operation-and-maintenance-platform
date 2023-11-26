import operator

from rest_framework.filters import BaseFilterBackend
from django.db.models.constants import LOOKUP_SEP
from mongoengine import Q
from functools import reduce

class MongoSearchFilter(BaseFilterBackend):
    search_param = 'search' # 配置搜索的参数 就是前端传过来的数据

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        params = request.query_params.get(self.search_param, '')
        search_term = params.replace('\x00', '')  # strip null characters
        # params = params.replace(',', ' ')
        # search_terms = params.split() # []

        if not search_fields or not search_term:
            return queryset


        orm_lookups = [
            LOOKUP_SEP.join([str(search_field), 'icontains'])
            for search_field in search_fields
        ] # ['label__icontains', 'name__icontains'# ]

        base = queryset
        conditions = []

        # for search_term in search_terms:
        queries = [
            Q(**{orm_lookup: search_term})
            for orm_lookup in orm_lookups
        ]
        # operator就是函数化使用数学字符
        # conditions.append(reduce(operator.or_, queries)) # 复习reduce opeator运算符重载函数 重载or =》 |
        queryset = queryset.filter(reduce(operator.or_, queries))

        return queryset
