from database.db_connection import DB
from utils import check_is_exists, is_within_range

class MissionDB:
    STATUS = ['New', 'Assigned', 'In Progress', 'Completed', 'Failed', 'Cancelled']

    def create_mission(self, data):
        values = [data["title"],
                data["description"],
                data["location"],
                data["difficulty"],
                data["importance"],
                data["status"]]
       
        if not check_is_exists(data["status"],self.STATUS):
           raise ValueError(f"valid fild agent_rank in {self.STATUS}, {data["status"]} Does not fit the options" )

        if not is_within_range(data["difficulty"]):
            raise ValueError(f"{data["difficulty"]} is not in the right range.")
        elif not is_within_range(data["importance"]):
            raise ValueError(f"{data["difficulty"]} is not in the right range.") 
        conn = DB.get_connection()
        cursor = conn.cursor()
        sql ="INSERT INTO missions (title, description, location,difficulty,importance,status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql,values)
        conn.commit()
        new_id  = cursor.lastrowid
        cursor.close()
        conn.close()
        return self.get_agent_by_id(new_id)


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
        mission = self.get_mission_by_id(id)
            
        if mission is None:
                return None
            
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE missions SET assigned_agent_id = %s WHERE id = %s", (a_id))
        chake = cursor.rowcount() > 0
        cursor.close()
        conn.close()
        return chake    
            

    def update_mission_status(self, id, status):
            mission = self.get_mission_by_id(id)
            
            if mission is None:
                return None
            
            
            conn = DB.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE missions SET status = %s WHERE id = %s", (status,id))
            chake = cursor.rowcount() > 0
            cursor.close()
            conn.close()
            return chake

    def get_open_missions_by_agent(self, id):
        pass

    def count_all_missions(self):
        pass

    def count_by_status(self, status):
        pass

    def count_open_missions(self):
        pass

    def count_critical_missions(self):
        pass

    def get_top_agent(self):
        pass