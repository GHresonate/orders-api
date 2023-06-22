from abc import ABC
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json


class DatabaseConnector(ABC):
    def __init__(self, table_name, url=None, fields_for_insert=None, fields=None, items=1000):
        if url is None:
            with open('secret/db_link') as secret_file:
                url = secret_file.read()
        self.database_url = url
        self.engine = create_engine(self.database_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()
        self.ITEMS_BEFORE_INSERT = items
        self.fields = fields
        self.table_name = table_name
        self.fields_for_insert = fields_for_insert

    def _check_if_exist(self, item_id):
        select = f'SELECT * FROM "{self.table_name}" WHERE ID={item_id}'
        sql = text(select)
        result = self.engine.execute(sql).all()
        if not len(result):
            raise HTTPException(status_code=404, detail=f"Item with the id {item_id} does not exist")

    @staticmethod
    def _validate_string(string):
        bad_words = (' select ', ' drop ', ' delete ', ' where ')
        for word in bad_words:
            if word in string.lower():
                raise HTTPException(status_code=400, detail=f"Police is going for you, hacker.")

    def _prepare_insert(self):
        insert = f'INSERT INTO "{self.table_name}" ('
        for field in self.fields_for_insert:
            insert += field + ', '
        insert = insert[0:-2] + ') VALUES '
        return insert

    def _validate_item(self, item):
        for x in item:
            if x[1] is not None:
                self._validate_string(str(x[1]))

    def get_item_by_id(self, item_id):
        try:
            item_id = int(item_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Id must be integer")
        select = f'SELECT '
        for field in self.fields:
            select += field + ', '
        select = select[0:-2] + f' FROM "{self.table_name}" WHERE ID={item_id}'
        sql = text(select)
        result = self.engine.execute(sql).all()
        if not len(result):
            raise HTTPException(status_code=404, detail=f"Item with the id {item_id} does not exist")
        else:
            return JSONResponse(jsonable_encoder(result))

    def get_all_items(self):
        select = f'SELECT '
        for field in self.fields:
            select += field + ', '
        select = select[0:-2] + f' FROM "{self.table_name}"'
        sql = text(select)
        result = self.engine.execute(sql).all()
        return JSONResponse(jsonable_encoder(result))

    def delete_by_id(self, item_id):
        try:
            item_id = int(item_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Id must be integer")
        self._check_if_exist(item_id)
        select = f'DELETE FROM "{self.table_name}" WHERE ID={item_id}'
        sql = text(select)
        try:
            self.engine.execute(sql)
        except (IntegrityError):
            raise HTTPException(status_code=400, detail=f"Can not delete. This item is used in another table(s).")

    def delete_all(self):
        select = f'DELETE FROM "{self.table_name}"'
        sql = text(select)
        try:
            self.engine.execute(sql)
        except (DataError, IntegrityError):
            raise HTTPException(status_code=400,
                                detail=f"Can not delete. One or more items are used in another table(s).")

    def update_item(self, item_id, item):
        try:
            item_id = int(item_id)
            self._validate_item(item)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Data is not valid")
        self._check_if_exist(item_id)
        update = f'UPDATE "{self.table_name}" SET '

        for field in self.fields:
            for x in item:
                if x[0] == field:
                    value = x[1]
                    if isinstance(value, str):
                        update += field + ' = '
                        update += "'" + value + "'" + ', '
                    elif value is None:
                        continue
                    else:
                        update += field + ' = '
                        update += str(value) + ', '
        update = update[0:-2] + f' WHERE ID={item_id}'
        sql = text(update)
        try:
            self.engine.execute(sql)
        except (DataError, IntegrityError):
            raise HTTPException(status_code=400, detail=f"Data is not valid")

    @staticmethod
    def _is_include(item, field):
        for x in item:
            if x[0] == field:
                return True
        return False

    def create_item(self, item):
        try:
            self._validate_item(item)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Data is not valid")
        insert = self._prepare_insert() + '('
        for field in self.fields_for_insert:
            place = self._is_include(item, field)
            if place:
                for x in item:
                    if x[0] == field:
                        value = x[1]
                        if isinstance(value, str):
                            insert += "'" + value + "'" + ', '
                        elif value is None:
                            insert += "NULL" + ', '
                        else:
                            insert += str(value) + ', '
            else:
                insert += "NULL" + ', '
        insert = insert[0:-2] + ');'
        sql = text(insert)
        try:
            self.engine.execute(sql)
        except (DataError, IntegrityError):
            raise HTTPException(status_code=400, detail=f"Data is not valid")
