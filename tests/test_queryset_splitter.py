# -*- coding: utf-8 -*-
import random

from django.test import TestCase
from django.contrib.auth.models import User
from django_queryset_splitter import QuerySetSplitter


class ModelTestCase(TestCase):

    def test_range_len(self):
        qss = QuerySetSplitter(User.objects.none(), 500)
        ids_rage = (
            1,
            2,
            3,
            (100, 201),
            (400, 600),
        )
        self.assertEqual(qss.get_ids_range_len(ids_rage), 304)

    def setUp(self):
        users = list()
        for x in xrange(0, 9000):
            user = User(username='%d-user' % x,
                        email='%d-user@mydomain.com' % x,
                        password='hashedPasswordStringPastedHereFromStep1!',
                        is_active=True,
                        is_staff=random.choice([True, False]),
                        is_superuser=True if x % 2 == 0 else False)
            users.append(user)
        User.objects.bulk_create(users)
        base_qs = User.objects.filter(is_staff=True)
        self.count = base_qs.count()
        self.assertGreater(self.count, 1000)
        self.qss = QuerySetSplitter(base_qs, 500)
        self.ids_ranges = list(self.qss.get_chunks())

    def test_get_qs_from_chunks(self):
        items_count = 0
        for r in self.ids_ranges:
            items_count += self.qss.get_qs_from_chunks(r).count()
        self.assertEqual(self.count, items_count)

    def test_get_qs_iterator_from_chunks(self):
        items_count = 0
        for r in self.ids_ranges:
            for qs in self.qss.get_qs_iterator_from_chunks(r):
                items_count += qs.count()
        self.assertEqual(self.count, items_count)

    def test_different_queryset(self):
        qs_list = [
            User.objects.none(),
            User.objects.all(),
            User.objects.all().order_by('-username'),
        ]
        for qs in qs_list:
            count = qs.count()
            qss = QuerySetSplitter(qs)
            items_count = 0
            ids_ranges = list(qss.get_chunks())
            for r in ids_ranges:
                items_count += qss.get_qs_from_chunks(r).count()
            self.assertEqual(count, items_count)
