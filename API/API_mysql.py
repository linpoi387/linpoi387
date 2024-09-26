from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy import create_engine, engine
import pandas as pd 



def get_mysql_conn() -> engine.base.Connection:
    address = "mysql+mysqlconnector://root:test@127.0.0.1:3306/crawler"
    engine = create_engine(address)
    connect = engine.connect()
    return connect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者設置特定的來源，例如 ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 127.0.0.1/foreign_currency?way=in&bank=esun&date=2024-09-12
@app.get("/foreign_currency")
def foreign_currency(
    # country: str = "",
    # start_date: str = "",
    # way: str = "",
    bank: str = "",
    date: str = "",
):
    sql = f"""
    select * from '{bank}'
    where timestamp = '{date}'
    """

    # sql = f"""
    # select * from esun
    # where country = '{country}'
    # and timestamp>= '{start_date}'
    # and timestamp<= '{end_date}'
    # """

    mysql_conn = get_mysql_conn()
    data_df = pd.read_sql(sql, con=mysql_conn)
    data_dict = data_df.to_dict(orient="records")
    return {"data": data_dict}


@app.get("/esun_foreign_currency")
def esun_foreign_currency(
    # country: str = "",
    # start_date: str = "",
    date: str = "",
):
    sql = f"""
    select * from esun
    where timestamp = '{date}'
    """

    # sql = f"""
    # select * from esun
    # where country = '{country}'
    # and timestamp>= '{start_date}'
    # and timestamp<= '{end_date}'
    # """

    mysql_conn = get_mysql_conn()
    data_df = pd.read_sql(sql, con=mysql_conn)
    data_dict = data_df.to_dict(orient="records")
    return {"data": data_dict}


@app.get("/cathaybk_foreign_currency")
def cathaybk_foreign_currency(
    # country: str = "",
    # start_date: str = "",
    date: str = "",
):
    sql = f"""
    select * from cathaybk
    where timestamp = '{date}'
    """

    # sql = f"""
    # select * from cathaybk
    # where country = '{country}'
    # and timestamp>= '{start_date}'
    # and timestamp<= '{end_date}'
    # """

    mysql_conn = get_mysql_conn()
    data_df = pd.read_sql(sql, con=mysql_conn)
    data_dict = data_df.to_dict(orient="records")
    return {"data": data_dict}
    