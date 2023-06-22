from connector import DatabaseConnector
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.exc import DataError, IntegrityError


class OrderConnector(DatabaseConnector):
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
        update = update[0:-2] + f" WHERE order_status_id='{item_id}'"
        sql = text(update)
        try:
            self.engine.execute(sql)
        except (DataError, IntegrityError):
            raise HTTPException(status_code=400, detail=f"Data is not valid")

    def _check_if_exist(self, item_id):
        select = f"SELECT order_status_id FROM "+ f'"{self.table_name}"'+ f" WHERE order_status_id='{item_id}'"
        sql = text(select)
        result = self.engine.execute(sql).all()
        if not len(result):
            raise HTTPException(status_code=404, detail=f"Item with the id {item_id} does not exist")

    def delete_by_id(self, item_id):
        self._check_if_exist(item_id)
        select = f'DELETE FROM "{self.table_name}"' + f" WHERE order_status_id='{item_id}'"
        sql = text(select)
        try:
            self.engine.execute(sql)
        except (IntegrityError):
            raise HTTPException(status_code=400, detail=f"Can not delete. This item is used in another table(s).")

    def get_item_by_id(self, item_id):
        select = f'SELECT '
        for field in self.fields:
            select += field + ', '
        select = select[0:-2] + f' FROM "{self.table_name}"' + f" WHERE order_status_id='{item_id}'"
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
        select = f'SELECT "{self.table_name}".order_status_id, "{self.table_name}".update_at, "{self.table_name}".sale_id,' \
                                f'"{self.table_name}".status_name_id, "sale".amount, "sale".date_sale,' \
                                f' "sale".product_id, "sale".user_id,' \
                                f'"sale".store_id, "status_name".status_name FROM "{self.table_name}"' + f' LEFT JOIN "sale" ' \
                                f'ON "{self.table_name}".sale_id = "sale".sale_id ' + \
                                f' LEFT JOIN "status_name" ' \
                                f'ON "{self.table_name}".status_name_id = "status_name".status_name_id ' +\
                                f" WHERE order_status_id='{item_id}'"
        sql = text(select)
        result = self.engine.execute(sql).all()
        if not len(result):
            raise HTTPException(status_code=404, detail=f"Item with the id {item_id} does not exist")
        else:
            return JSONResponse(jsonable_encoder(result))
