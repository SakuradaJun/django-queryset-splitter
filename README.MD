django_queryset_splitter
========================
[![Build Status](https://travis-ci.org/SakuradaJun/django-queryset-splitter.svg?branch=master)](https://travis-ci.org/SakuradaJun/django-queryset-splitter)
[![Coverage Status](https://coveralls.io/repos/github/SakuradaJun/django-queryset-splitter/badge.svg?branch=master)](https://coveralls.io/github/SakuradaJun/django-queryset-splitter?branch=master)

This util is usable in cases when you have QuerySet with large number of rows and you need split it to chunks and then handle it with Celery/Python RQ or with any others handler.

<!--Installation-->
<!---------------->
<!--```bash-->
<!--$ pip install django-queryset-splitter-->
<!--```-->

Similar projects
----------------

https://github.com/pelletier/django-parallelized_querysets
