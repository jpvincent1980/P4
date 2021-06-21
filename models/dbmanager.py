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
            (table_name) of the DBManager object
            update_record_data -> update the value of a specific key (data_key)
            of a record identified by its doc_id (record_id) in a specific table (table_name)
            with a new value (data_value) by replacing the existing value (append=False)
            or appending the existing value (append=True)
            get_record_data -> fetches all data (data_key=None) of a record identified by
            its doc_id (record_id) for a specific table (table_name) or only
            a specific key (data_key) of this record.
        """

    def __init__(self, db_name, *table_name):
        """
        Constructor of the DBManager class

            Parameters
            ----------
        db_name: name of the TinyDB database (a JSON file in our case)
        table_name: name(s) of the TinyDB database table(s)

            Returns
            ----------
                None
        """
        self.DB = TinyDB(db_name)
        for table in table_name:
            setattr(self, table, self.DB.table(table))

    def add_record(self, table_name, record_data):
        """
        Adds a record to a table of a DBManager object

            Parameters
            ----------
                table_name -> name of the TinyDB table to which the record must be added
                record_data -> data that must be added to the TinyDB table

            Returns
            -------
                None
        """
        getattr(self,table_name).insert(record_data)
        return

    def update_record_data(self,table_name, record_id, data_key, new_value, append=False):
        """
        Updates a record of a DBManager object

            Parameters
            ----------
                table_name -> name of the TinyDB table to which a record must be updated
                record_id -> doc_id of the record that must be updated
                data_key -> name of the record's key that must be updated
                new_value -> new value that must be assigned to the record's key
                append -> a boolean that specifies if new_value must be appended (=True) to
                the existing value or replaces (=False) the existing value

            Returns
            -------
                None
        """
        if append:
            key_value = getattr(self, table_name).get(doc_id=record_id)[data_key]
            key_value.append(new_value)
            getattr(self, table_name).update({data_key:key_value}, doc_ids=[record_id])
        else:
            getattr(self, table_name).update({data_key:new_value}, doc_ids=[record_id])
        return

    def get_record_data(self,table_name, record_id, data_key=None):
        """
        Retrieves a record of a table of a DBManager object

            Parameters
            ----------
                table_name -> name of the DBManager object's table on which
                a record must be updated
                record_id -> doc_id of the record that must be updated
                data_key -> name of the record's key that must be updated. If a data_key is
                entered, only the value of that key is retrieved, if no data_key is entered
                (=None), the entire record is retrieved

            Returns
            -------
                The entire record data (as a TinyDB table document) if data_key=None or
                the value of the record's key if data_key is not None.
        """
        if data_key:
            return getattr(self, table_name).get(doc_id=record_id)[data_key]
        else:
            return getattr(self, table_name).get(doc_id=record_id)


if __name__ == "__main__":
    pass