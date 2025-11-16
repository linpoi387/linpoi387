from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
import redis
from typing import Dict

app = FastAPI()

# MySQL 連接配置
MYSQL_CONFIG = {
    "host": "54.150.84.198",
    "user": "interview",
    "password": "nfaafrCya2zTwnHn",
    "database": "test_db"
}

# Redis 連接配置
REDIS_CONFIG = {
    "host": "54.250.236.103",
    "port": 6379,
    "password": "fYNmRdZVkuX6",
    "db": 0
}

def get_mysql_connection():
    try:
        return mysql.connector.connect(**MYSQL_CONFIG)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"MySQL連接失敗: {str(e)}")

def get_redis_connection():
    try:
        return redis.Redis(**REDIS_CONFIG)
    except redis.ConnectionError as e:
        raise HTTPException(status_code=400, detail=f"Redis連接失敗: {str(e)}")

@app.get("/users/{id}")
async def get_user(id: int) -> Dict:
    try:
        # MySQL 查詢
        mysql_conn = get_mysql_connection()
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT username, email FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        
        if not user:
            return JSONResponse(
                status_code=400,
                content={"detail": f"找不到ID為 {id} 的用戶"}
            )
        
        # Redis 查詢
        redis_conn = get_redis_connection()
        redis_value = redis_conn.get(user['username'])
        
        if not redis_value:
            return JSONResponse(
                status_code=400,
                content={"detail": f"Redis中找不到用戶 {user['username']} 的資料"}
            )
        
        return {
            "username": user['username'],
            "email": user['email'],
            "redis_value": redis_value.decode('utf-8')
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"detail": f"查詢失敗: {str(e)}"}
        )
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)