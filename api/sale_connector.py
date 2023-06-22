from connector import DatabaseConnector
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.exc import DataError, IntegrityError


class SaleConnector(DatabaseConnector):
    def update_item(self, item_id, item):
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
        update = update[0:-2] + f" WHERE sale_id='{item_id}'"
        sql = text(update)
        try:
            self.engine.execute(sql)
        except (DataError, IntegrityError):
            raise HTTPException(status_code=400, detail=f"Data is not valid")

    def _check_if_exist(self, item_id):
        select = f"SELECT sale_id FROM "+ f'"{self.table_name}"'+ f" WHERE sale_id='{item_id}'"
        sql = text(select)
        result = self.engine.execute(sql).all()
        if not len(result):
            raise HTTPException(status_code=404, detail=f"Item with the id {item_id} does not exist")

    def delete_by_id(self, item_id):
        self._check_if_exist(item_id)
        select = f'DELETE FROM "{self.table_name}"' + f" WHERE sale_id='{item_id}'"
        sql = text(select)
        try:
            self.engine.execute(sql)
        except (IntegrityError):
            raise HTTPException(status_code=400, detail=f"Can not delete. This item is used in another table(s).")

    def get_item_by_id(self, item_id):
        select = f'SELECT '
        for field in self.fields:
            select += field + ', '
        select = select[0:-2] + f' FROM "{self.table_name}"' + f" WHERE sale_id='{item_id}'"
        sql = text(select)
        result = self.engine.execute(sql).all()
        if not len(result):
            raise HTTPException(status_code=404, detail=f"Item with the id {item_id} does not exist")
        else:
            return JSONResponse(jsonable_encoder(result))

    def get_all_info_by_id(self, item_id):
        select = f'SELECT '
        for field in self.fields:
            select += field + ', '
        select = f'SELECT "{self.table_name}".sale_id, "{self.table_name}".amount, "{self.table_name}".date_sale, ' \
                                f'"{self.table_name}".product_id, "{self.table_name}".user_id, "{self.table_name}".store_id,' \
                                f'"product".name as productname, "store".name as store_name, "store".city_id,' \
                                f'"users".name as username FROM "{self.table_name}"' + \
                                f' LEFT JOIN "product" ' \
                                f'ON "{self.table_name}".product_id = "product".product_id ' + \
                                f' LEFT JOIN "users" ' \
                                f'ON "{self.table_name}".user_id = "users".user_id ' + \
                                f' LEFT JOIN "store" ' \
                                f'ON "{self.table_name}".store_id = "store".store_id ' + \
                                f" WHERE sale_id='{item_id}'"
        sql = text(select)
        result = self.engine.execute(sql).all()
        if not len(result):
            raise HTTPException(status_code=404, detail=f"Item with the id {item_id} does not exist")
        else:
            return JSONResponse(jsonable_encoder(result))
