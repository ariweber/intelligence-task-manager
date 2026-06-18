from database.db_connection import DB


class MissionDB:
    STATUS = ['New', 'Assigned', 'In Progress', 'Completed', 'Failed', 'Cancelled']

    def create_mission(self, data):
        values = [data["title"],
                data["description"],
                data["location"],
                data["difficulty"],
                data["importance"],
                data["status"],
                data["risk_level"]]

        conn = DB.get_connection()
        cursor = conn.cursor()
        sql ="INSERT INTO missions (title, description, location,difficulty,importance,status,risk_level) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,values)
        conn.commit()
        new_id  = cursor.lastrowid
        cursor.close()
        conn.close()
        return self.get_mission_by_id(new_id)


    def get_all_missions(self):
        conn = DB.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM  missions")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data  

        
    def get_mission_by_id(self, id):
        conn = DB.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data


    def assign_mission(self, m_id, a_id):
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE missions SET assigned_agent_id = %s WHERE id = %s", (a_id, m_id))
        conn.commit()
        chake = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return chake
            

    def update_mission_status(self, id, status):
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE missions SET status = %s WHERE id = %s", (status,id))
        conn.commit()
        chake = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return chake
    
            
           
    def get_open_missions_by_agent(self, id):
        conn = DB.get_connection()
        cursor = conn.cursor(dictionary=True)
        status_open = ('Assigned', 'In Progress')
        cursor.execute("SELECT * FROM missions WHERE assigned_agent_id = %s AND status IN (%s, %s)", (id, *status_open))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data     
        

    def count_all_missions(self):
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM missions")
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0] 

    def count_by_status(self, status):
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status = %s",(status,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0]

    def count_open_missions(self):
        conn = DB.get_connection()
        cursor = conn.cursor()
        status_open = 'New', 'Assigned', 'In Progress'
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status IN (%s, %s, %s)",(status_open))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0]

    def count_critical_missions(self):
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level = %s", ('critical',))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0]

    def get_top_agent(self):
        conn = DB.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1")
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data


dbmission = MissionDB()
        