# haystack-function-score-backend
A Haystack ElasticSearch backend that add function score and decay functionality 

This custom backend and queryset add one function on queryset.
FunctionScoreSearchQuerySet provide a decay() function that take a decay as dictionnary.

You can add many decays your queryset.


# prerequire

##elasticsearch function_score documentation

https://www.elastic.co/guide/en/elasticsearch/guide/current/function-score-query.html

##The closer, the Better.
### Tipical use case from elasticsearch documentation

https://www.elastic.co/guide/en/elasticsearch/guide/current/decay-functions.html#img-decay-functions

# usage
```python
# set the new engine as the default for your haystack connection
HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'function_score_elasticsearch.CustomEsSearchEngine',
		'URL': 'http://127.0.0.1:9200/',
		'INDEX_NAME': 'indexName',
	},
}

# import the new SearchQuerySet with the implemented decay functionality
from search.function_score_elasticsearch import FunctionScoreSearchQuerySet

# create your search query
sqs = FunctionScoreSearchQuerySet()
# use it like normal haystack sqs
sqs = sqs.filter(text='foo')

# define your decay function as dict
decay_distance = {
	'exp': {
		'vehicle_location': {
			'origin': {"lat": str(latitude), "lon": str(longitude)},
			'scale': "50km",
			'offset': "15km",
		}	
	},
	"weight": 2,
}

# finally just add you dict as sqs decay
sqs = sqs.decay(decay_distance)
return sqs
```
