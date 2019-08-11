import psycopg2
import json
import datetime
import traceback

from queries import query_add, query_clear, query_delete, query_select_address, \
    query_select_id, query_select_interval_age, query_select_max_age, \
    query_select_min_age, query_update, query_select_all


class DaoPerson:
    def __init__(self):
        with open("/home/sergio/person_persistence_tests/config/configs.json", "r") as file:
            json_file = json.load(file)
            self._database_name = json_file["database"]
            self._user = json_file["user"]
            self._pass = json_file["pass"]
            self._address = json_file["address"]
            self._port = json_file["port"]

    def select_by_id(self, id):
        '''
        get people by id
        :param id: id
        :return: list of tuples that satisfies the query
        '''
        query = query_select_id.format(id)
        return self._read(query)

    def select_by_min_age(self, min_age):
        '''
        get people of a certain minimum age
        :param min_age: max age (inclusive)
        :return: list of tuples of people
        '''
        now = datetime.datetime.now()
        min_date = datetime.datetime(now.year - min_age, now.month, now.day)
        query = query_select_min_age.format(min_date)
        return self._read(query)

    def select_by_max_age(self, max_age):
        '''
        get people of a certain maximum age
        :param max_age: max age (inclusive)
        :return: list of tuples of people
        '''
        now = datetime.datetime.now()
        max_date = datetime.datetime(now.year - max_age, now.month, now.day)
        query = query_select_max_age.format(max_date)
        return self._read(query)

    def select_by_range_age(self, min_age, max_age):
        '''
        get people of a certain age range
        :param min_age: minimum age
        :param max_age: minimum age
        :return: list of tuples of people meeting this range
        '''
        now = datetime.datetime.now()
        min_date = datetime.datetime(now.year - max_age - 1, now.month, now.day)
        max_date = datetime.datetime(now.year - min_age, now.month, now.day)
        query = query_select_interval_age.format(min_date, max_date)
        return self._read(query)

    def select_by_address(self, address):
        '''
        get people who have an address that contains default data
        :param address: address
        :return: list of tuples that satisfies the query
        '''
        query = query_select_address.format(address)
        return self._read(query)

    def select_all(self):
        '''
        get all records
        :return: list with all people
        '''
        return self._read(query_select_all)

    def update(self, id, name, address, date_of_birth):
        '''
        update person
        :param id: id
        :param name: name of person
        :param address: address
        :param date_of_birth: date of birth
        :return: number of affected rows
        '''
        query = query_update.format(name, date_of_birth, address, id)
        return self._write(query)

    def _read(self, query):
        '''
        private - send read operations to database
        :param query: sql statement
        :return: tuples with selected people
        '''
        try:
            connection = psycopg2.connect(user=self._user,
                                          password=self._pass,
                                          host=self._address,
                                          port=self._port,
                                          database=self._database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
        except Exception:
            traceback.print_exc()
            raise Exception()
        finally:
            if connection:
                cursor.close()
                connection.close()
        return records

    def _write(self, query):
        '''
        private - send write operations to database
        :param query: sql statement
        :return: number of affected rows
        '''
        try:
            connection = psycopg2.connect(user=self._user,
                                          password=self._pass,
                                          host=self._address,
                                          port=self._port,
                                          database=self._database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            count = cursor.rowcount
            connection.commit()
        except:
            traceback.print_exc()
            raise Exception()
        finally:
            if connection:
                cursor.close()
                connection.close()
        return count

    def add(self, name, birth, address):
        '''
        add a new person
        :param name: name
        :param birth: date of birth
        :param address: address
        :return: number of affected rows
        '''
        query = query_add.format(name, birth, address)
        return self._write(query)

    def remove(self, id):
        '''
        :param id: id of person to be removed
        :return: number of affected rows
        '''
        query = query_delete.format(id)
        return self._write(query)

    def clear(self):
        '''
        remove all data
        :return: number of affected rows
        '''
        return self._write(query_clear)

    def __str__(self): # pragma: no cover
        return self._database_name + " " + self._user + " " + self._pass + " " + self._address + ":" + self._port
