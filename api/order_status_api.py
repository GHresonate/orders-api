from fastapi import APIRouter
from typing import Union
from pydantic import BaseModel
from order_connector import OrderConnector


class OrderStatus(BaseModel):
    sale_id: str
    status_name_id: int


class UpdateOrderStatus(OrderStatus):
    sale_id: Union[str, None] = None
    status_name_id: Union[int, None] = None


order_connector = OrderConnector(table_name="order_status",
                                 fields_for_insert=('sale_id', 'status_name_id'),
                                 fields=('order_status_id', 'sale_id', 'status_name_id', 'update_at'))

router = APIRouter(prefix="/order_status",
                   tags=["order_status"])


@router.get("/all")
def get_all():
    return order_connector.get_all_items()


@router.get("/get/{order_id}")
def get_by_id(order_id: str):
    return order_connector.get_item_by_id(order_id)


@router.get("/get/full/{order_id}")
def get_all_info_by_id(order_id: str):
    return order_connector.get_all_info_by_id(order_id)


@router.delete("/delete/{order_id}", status_code=204)
def delete_one(order_id: str):
    return order_connector.delete_by_id(order_id)


@router.delete("/delete_all/", status_code=204)
def delete_all():
    return order_connector.delete_all()


@router.post("/update/{order_id}", status_code=204)
def update(order_id: str, order: UpdateOrderStatus):
    return order_connector.update_item(order_id, order)


@router.post("/create", status_code=204)
def create(order: OrderStatus):
    return order_connector.create_item(order)
