from rest_framework.filters import BaseFilterBackend

class MongoSearchFilter(BaseFilterBackend):
    search_param = 'search'

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        search_terms = params.split() # []

        if not search_fields or not search_terms:
            return queryset

        return queryset
