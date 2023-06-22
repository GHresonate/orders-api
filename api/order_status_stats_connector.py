from connector import DatabaseConnector
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text


class OrderStStConnector(DatabaseConnector):
    @staticmethod
    def check_dates(start_date, end_date):
        try:
            if not (datetime.strptime(start_date, '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d')):
                raise ValueError
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Data is not valid")

    def get_order_status_stats(self, start_date, end_date):
        self.check_dates(start_date, end_date)
        select = f"SELECT * FROM order_status_stats WHERE dt >= '{start_date}' AND dt <= '{end_date}'"
        sql = text(select)
        result = self.engine.execute(sql).all()
        return JSONResponse(jsonable_encoder(result))
