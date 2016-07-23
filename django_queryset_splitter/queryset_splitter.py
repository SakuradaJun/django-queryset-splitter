# -*- coding: utf-8 -*-
import itertools
from django.db.models import Q


def iterable_to_ranges_gen(iterable):
    for a, b in itertools.groupby(enumerate(iterable), lambda (x, y): y - x):
        b = list(b)
        yield b[0][1], b[-1][1]


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return (filter(None, r) for r in itertools.izip_longest(fillvalue=fillvalue, *args))


class QuerySetSplitter(object):
    """
    Works only with default Django PK and ordering PK by ASC
    """
    queryset = None

    def __init__(self, queryset=None, chunk_size=1000):
        if queryset is None:
            queryset = self.queryset
        if queryset is None:
            raise Exception('queryset is None')
        self.set_queryset(queryset)
        self.chunk_size = chunk_size

    def set_queryset(self, queryset):
        self.queryset = queryset.order_by().order_by('id')

    def get_chunks(self):
        ids_gen = self.queryset.values_list('id', flat=True).iterator()

        ids_range_q = set()
        queue_size = 0

        for ids_range in self._gen_ranges(ids_gen=ids_gen):
            size = self.get_flat_range_len(ids_range)

            if queue_size+1 >= self.chunk_size:
                yield tuple(ids_range_q)
                ids_range_q.clear()
                queue_size = 0
            queue_size += size
            if len(ids_range) == 2 and ids_range[0] == ids_range[1]:
                ids_range = ids_range[0]
            ids_range_q.add(ids_range)

        if ids_range_q:
            yield tuple(ids_range_q)
            ids_range_q.clear()

    def _gen_ranges(self, ids_gen):
        ids_chunks_gen = grouper(ids_gen, self.chunk_size)
        for chunk in ids_chunks_gen:
            for ids_range in iterable_to_ranges_gen(chunk):
                yield ids_range

    def get_flat_range_len(self, flat_range):
        if isinstance(flat_range, (int, long)):
            return 1

        if flat_range[0] == flat_range[1]:
            return 1
        else:
            return flat_range[1] - flat_range[0]

    def get_ids_range_len(self, ids_range):
        return sum([self.get_flat_range_len(x) for x in ids_range])

    def get_qs_iterator_from_chunks(self, ids_ranges):
        for ids in ids_ranges:
            if isinstance(ids, (int, long)):
                yield self.queryset.filter(id=ids)
            else:
                yield self.queryset.filter(id__range=ids)

    def get_qs_from_chunks(self, ids_ranges):
        ranges_filter = list()
        list_filter = set()

        for ids in ids_ranges:
            if isinstance(ids, (int, long)):
                list_filter.add(ids)
            else:
                ranges_filter.append(ids)
        return self.queryset.filter(reduce(lambda x, y: x | y, [Q(id__range=ids) for ids in ranges_filter]) | Q(id__in=list_filter))
