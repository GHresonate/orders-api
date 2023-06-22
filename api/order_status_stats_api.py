from fastapi import APIRouter, Query
from order_status_stats_connector import OrderStStConnector

router = APIRouter(prefix="/order_status_stats",
                   tags=["order_status_stats"])


status_stats_connector = OrderStStConnector(table_name="order_status_stats")


@router.get("/order_status_stats")
async def get_order_status_stats(start_date: str = Query(description='"YYYY-MM-DD"'), end_date: str = Query(description='"YYYY-MM-DD"')):
    return status_stats_connector.get_order_status_stats(start_date, end_date)