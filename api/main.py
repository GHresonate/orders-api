import order_status_api
import order_status_stats_api
import sale_api
from fastapi import FastAPI


app = FastAPI()
app.include_router(order_status_api.router)
app.include_router(order_status_stats_api.router)
app.include_router(sale_api.router)
