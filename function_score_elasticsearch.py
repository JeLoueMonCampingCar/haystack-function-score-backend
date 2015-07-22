from haystack.backends.elasticsearch_backend import (
    ElasticsearchSearchBackend, ElasticsearchSearchQuery,
    ElasticsearchSearchEngine)
from haystack.query import SearchQuerySet
from haystack.exceptions import MissingDependency
try:
    import elasticsearch
except ImportError:
    raise MissingDependency(
        "The 'elasticsearch' backend requires the installation of 'elasticsearch'. Please refer to the documentation.")


class FunctionScoreSearchBackend(ElasticsearchSearchBackend):

    """
    Search backend that add the function score to the elastic search query
    """

    def build_search_kwargs(self, query_string, decay_functions=None, **kwargs):
        kwargs = super(FunctionScoreSearchBackend, self).build_search_kwargs(
            query_string, **kwargs)
        if not decay_functions:
            return kwargs

        original_query = kwargs['query']
        function_score_query = {
            'function_score': {
                'functions': decay_functions,
                'query': original_query,
                'score_mode': 'sum'
            }
        }
        kwargs['query'] = function_score_query
        return kwargs


class FunctionScoreSearchQuery(ElasticsearchSearchQuery):

    def __init__(self, **kwargs):
        super(FunctionScoreSearchQuery, self).__init__(**kwargs)
        self.decay_functions = []

    def build_params(self, *args, **kwargs):
        search_kwargs = super(
            FunctionScoreSearchQuery, self).build_params(*args, **kwargs)
        if self.decay_functions:
            search_kwargs['decay_functions'] = self.decay_functions

        return search_kwargs

    def add_decay_function(self, function_dict):
        self.decay_functions.append(function_dict)

    def _clone(self, **kwargs):
        clone = super(FunctionScoreSearchQuery, self)._clone(**kwargs)
        clone.decay_functions = self.decay_functions[:]
        return clone


class FunctionScoreSearchQuerySet(SearchQuerySet):

    """
    usage example:
    SearchQuerySet().filter(text='foo').decay({'gauss': {'end_time' : {'origin': '2014-05-07', 'scale' : '10d' }}}
    """

    def decay(self, function_dict):
        clone = self._clone()
        clone.query.add_decay_function(function_dict)
        return clone


class CustomEsSearchEngine(ElasticsearchSearchEngine):
    backend = FunctionScoreSearchBackend
    query = FunctionScoreSearchQuery
