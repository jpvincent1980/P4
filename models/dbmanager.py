#! /usr/bin/env python3
# coding: utf-8
from tinydb import TinyDB

class DBManager:
    pass

    def __init__(self, db_name, *table_name):
        self.DB = TinyDB(db_name)
        for table in table_name:
            setattr(self, table, self.DB.table(table))

    def add_record(self, table_name, record_data):
        getattr(self,table_name).insert(record_data)

    def update_record_data(self,table_name, data_key, data_value, record_id, append=False):
        if append:
            key_value = getattr(self, table_name).get(doc_id=record_id)[data_key]
            key_value.append(data_value)
            getattr(self, table_name).update({data_key:key_value}, doc_ids=[record_id])
        else:
            getattr(self, table_name).update({data_key:data_value},doc_ids=[record_id])

    def get_record_data(self,table_name, record_id, data_key=None):
        if data_key:
            return getattr(self, table_name).get(doc_id=record_id)[data_key]
        else:
            return getattr(self, table_name).get(doc_id=record_id)

if __name__ == "__main__":
    # DB = DBManager("test.json","tournaments","players")
    # print(DB)
    # print(DB.__dict__)
    # DB.add_record("players",{"name":"Rabbit"})
    # DB.update_record_data("players","name","Lapin",2)
    # print(DB.get_record_data("tournaments",3))
    pass