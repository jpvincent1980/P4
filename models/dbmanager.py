#! /usr/bin/env python3
# coding: utf-8
from tinydb import TinyDB

class DBManager:
    """
        A class that interacts with the TinyDB database.

        Attributes
        ----------
        DB -> creates or connects to the TinyDB database
        table -> a dynamic variable that represents the table(s)
        of the TinyDB database

        Methods
        -------
        add_record -> add data (record_data) as a new record to the table
        (table_name) of the TinyDB database
        update_record_data -> update the value of a specific key (data_key)
        of a record named with its doc_id (record_id) in a specific table (table_name)
        with a new value (data_value) by replacing the existing value (append=False)
        or appending the existing value (append=True)
        get_record_data -> fetches all data (data_key=None) of a record named
        with its doc_id (record_id) for a specific table (table_name) or only
        a specific key (data_key) of this record.
        """

    def __init__(self, db_name, *table_name):
        self.DB = TinyDB(db_name)
        for table in table_name:
            setattr(self, table, self.DB.table(table))

    def add_record(self, table_name, record_data):
        getattr(self,table_name).insert(record_data)

    def update_record_data(self,table_name, record_id, data_key, new_value, append=False):
        if append:
            key_value = getattr(self, table_name).get(doc_id=record_id)[data_key]
            key_value.append(new_value)
            getattr(self, table_name).update({data_key:key_value}, doc_ids=[record_id])
        else:
            getattr(self, table_name).update({data_key:new_value}, doc_ids=[record_id])

    def get_record_data(self,table_name, record_id, data_key=None):
        if data_key:
            return getattr(self, table_name).get(doc_id=record_id)[data_key]
        else:
            return getattr(self, table_name).get(doc_id=record_id)

if __name__ == "__main__":
    pass