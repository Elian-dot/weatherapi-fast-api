from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Configuración de conexión
DB_CONFIG = {
    "host": "localhost",
    "database": "wheatherapi",
    "use": "postgress",
    "password": "*********", 
    "port": 5432   
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.get("/")
async def root():
    return {"message": "API de Clima Funcionando"}

@app.post("/insert/dispositivo")
async def insert_dispositivo(id: int, w: str, n: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "INSERT INTO dispositivo (id, w, n) VALUES (%s, %s, %s)"
        cursor.execute(sql, (id, w, n))
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))
    
@app.post("/insert/sensor")
async def inser_sensor(id: int, referencia: str, descripcion: str, disposito_id: int):
    try:
        conn = get_db_connection();
        cursor = conn.cursor()

        sql =  "INSERT INTO sensor (id, referencia, descripcion, dispositivo_id) VALUES (%s, %s, %s, %s)"

        cursor.execute(sql, (id, referencia, descripcion, disposito_id))

        conn.commit()
        cursor.close()
        conn.close()

        return {"status": "success", "message": f"sensor {id} insertando correctamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al insertar: {str(e)}")

@app.post("/insert/lectura")
async def insert_lectura(id: int, fechahora: str, valor: str, sensor_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO lectura (id, fechahora, valor, sensor_id) VALUES (%s, %s, %s, %s)"

        cursor.execute(sql, (id, fechahora, valor, sensor_id))
        
        conn.commit()
        cursor.close()
        conn.close()

        return {"status": "success", "id_lectura": id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la inserción: {str(e)}")

@app.get("/select")
async def read_items(table:str):
    # Validación para evitar inyección sql.
    allowed_tables = ["dispositivo", "sensor", "lectura"]
    if table not in allowed_tables:
        raise HTTPException(status_code=400, detail="Tabla no permitida")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        sql = f"SELECT * FROM {table} ORDER BY id"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))