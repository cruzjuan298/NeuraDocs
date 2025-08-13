from app.db.connection import get_db_connection

def deleteDbPerm(db_id: str):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM document WHERE db_id = ?", (db_id,))
            conn.commit()

            if cur.rowcount == 0:
                return {"success" : False, "message" : "Database not found"}

            return {"success" : True, "message" : "Database has been deleted"}
        
    except Exception as e:
        return {"success" : False, "message" : e}