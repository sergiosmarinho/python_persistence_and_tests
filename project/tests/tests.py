import datetime
import unittest

import sys
sys.path.append('../')

from dao import DaoPerson


class Tests(unittest.TestCase):
    def test(self):
        d = DaoPerson()
        d.clear()

        self.assertEqual(d.add("johnson", "1992-09-21", "av 3"), 1)
        self.assertEqual(d.add("ralph", "1992-09-18", "st 7"), 1)
        self.assertEqual(d.add("christopher", "1976-09-18", "st 7"), 1)
        self.assertEqual(d.add("joe", "2007-12-30", "av 9"), 1)
        self.assertEqual(d.add("juan", "2000-01-30", "st 9"), 1)
        id_to_update = d.select_all()[0][0]

        self.assertEqual(len(d.select_by_id(id_to_update)), 1)

        with self.assertRaises(Exception):
            d.select_by_id("dfd")

        with self.assertRaises(Exception):
            d.add("44", "745", "55")

        self.assertEqual(d.update(id_to_update, "john", "av 4", "1992-09-22"), 1)

        min_age_18 = d.select_by_min_age(18)
        self._check_min_age(min_age_18, 18)

        max_age_18 = d.select_by_max_age(18)
        self._check_max_age(max_age_18, 18)

        range_age = d.select_by_range_age(3, 20)
        self._check_range(range_age, 3, 20)

        id_to_remove = d.select_all()[0][0]

        self.assertEqual(len(d.select_by_address("st")), 3)

        self.assertEqual(d.remove(id_to_remove), 1)

        d.clear()
        self.assertEqual(d.select_all(), [])

    def _check_min_age(self, data, min_age):
        for x in data:
            birth = x[2]
            age = self._calc_age(birth)
            self.assertGreaterEqual(age, min_age)

    def _check_max_age(self, data, max_age):
        for x in data:
            birth = x[2]
            age = self._calc_age(birth)
            self.assertLessEqual(age, max_age)

    def _check_range(self, data, min_age, max_age):
        for x in data:
            birth = x[2]
            age = self._calc_age(birth)
            self.assertGreaterEqual(age, min_age)
            self.assertLessEqual(age, max_age)

    def _calc_age(self, birth):
        today = datetime.datetime.now()
        try:
            birthday = birth.replace(year=today.year)
        except ValueError: # pragma: no cover
            birthday = birth.replace(year=today.year, month=birth.month + 1, day=1)
        if birthday > today:
            return today.year - birth.year - 1
        else:
            return today.year - birth.year
