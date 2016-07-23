django_queryset_splitter
========================
[![Build Status](https://travis-ci.org/SakuradaJun/django-queryset-splitter.svg?branch=master)](https://travis-ci.org/SakuradaJun/django-queryset-splitter)
[![Coverage Status](https://coveralls.io/repos/github/SakuradaJun/django-queryset-splitter/badge.svg?branch=master)](https://coveralls.io/github/SakuradaJun/django-queryset-splitter?branch=master)

Split large Django QuerySets to chunks for handling by queues like Celery or RQ

That utility works only with default Django PK and ordering PK by ASC.

Currently only supports Python 2.7.x and Django 1.7, 1.8, 1.9

Installation
------------
```bash
$ pip install git+https://github.com/SakuradaJun/django-queryset-splitter.git
```

Usage
-----
This is an example with using [Python RQ (Redis Queue)](http://python-rq.org/)

```python
import requests
from redis import Redis
from rq import Queue
from django_queryset_splitter import QuerySetSplitter

q = Queue(connection=Redis())

base_qs = Article.objects.all()
qss = QuerySetSplitter(base_qs, 50) # Max chunk size 50

def count_words_at_url(chunks):
    qs = qss.get_qs_from_chunks(chunks)
    results = 0
    for article_obj in qs:
        resp = requests.get(article_obj.url)
        results += len(resp.text.split())
    return results

if __name__ == "__main__":
    for chunks in qss.get_chunks():
        q.enqueue(count_words_at_url, chunks)
```

Similar projects
----------------

https://github.com/pelletier/django-parallelized_querysets
