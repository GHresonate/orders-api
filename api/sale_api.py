from fastapi import APIRouter, Query
from typing import Union
from pydantic import BaseModel
from sale_connector import SaleConnector
import os


class Sale(BaseModel):
    amount: float
    date_sale: str
    product_id: int
    user_id: int
    store_id: int


class UpdateSale(Sale):
    amount: Union[float, None] = None
    date_sale: Union[str, None] = None
    product_id: Union[int, None] = None
    user_id: Union[int, None] = None
    store_id: Union[int, None] = None


sale_connector = SaleConnector(table_name="sale",
                               fields_for_insert=('amount', 'date_sale', 'product_id', 'user_id', 'store_id'),
                               fields=('sale_id', 'amount', 'date_sale', 'product_id', 'user_id', 'store_id'))

router = APIRouter(prefix="/sale",
                   tags=["sale"])


@router.get("/all")
def get_all():
    return sale_connector.get_all_items()


@router.get("/get/{sale_id}")
def get_by_id(sale_id: str):
    return sale_connector.get_item_by_id(sale_id)


@router.get("/get/full/{sale_id}")
def get_all_info_by_id(sale_id: str):
    return sale_connector.get_all_info_by_id(sale_id)


@router.delete("/delete/{sale_id}", status_code=204)
def delete_one(sale_id: str):
    return sale_connector.delete_by_id(sale_id)


@router.delete("/delete_all/", status_code=204)
def delete_all():
    return sale_connector.delete_all()


@router.post("/update/{sale_id}", status_code=204)
def update(sale_id: str, sale: UpdateSale):
    return sale_connector.update_item(sale_id, sale)


@router.post("/create", status_code=204)
def create(sale: Sale):
    return sale_connector.create_item(sale)
