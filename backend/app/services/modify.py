from app.db.connection import get_db_connection

def modifyName(db_id ,new_name):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE document SET name = ? WHERE db_id = ?", (new_name, db_id,))
            conn.commit()

            if cur.rowcount == 0:
                return {"success" : False, "message" : f"Error trying to change the name of the db with db_id {db_id}"}
        
            return {"success" : True, "message" : "Name change was successful"}
            
    except Exception as e:
        return {"success" : False, "messgae" : f"Error trying to modify the db with db_id {db_id} with error: {e}."}