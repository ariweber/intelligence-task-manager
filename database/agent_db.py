from database.db_connection import DB
from utils import check_is_exists

class AgentDB:
    FIELDS = {"name", "specialty", "agent_rank"}

    def create_agent(self, data):
        values = [data["name"], data["specialty"], data["agent_rank"]]
        conn = DB.get_connection()
        cursor = conn.cursor()
        sql ="INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)"
        cursor.execute(sql,values)
        conn.commit()
        new_id  = cursor.lastrowid
        cursor.close()
        conn.close()
        return self.get_agent_by_id(new_id)


    def get_all_agents(self):
        conn = DB.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def update_agent(self, id, data):
        agent = self.get_agent_by_id(id)
        if agent is None:
            return None
        
        fields = {key: value for key, value in data.items() if key in self.FIELDS and value is not None} 
        if not self.FIELDS:
            return agent

        set_clause = ", ".join(f"{fielde} = %s" for fielde in fields)
        values = list(fields.values()) + [id]
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE agents SET {set_clause} WHERE id = %s", values)
        conn.commit()
        cursor.close()
        conn.close()
        return self.get_agent_by_id(id)
       
    
    def get_agent_by_id(self, id):
        conn = DB.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    def deactivate_agent(self, id):
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET is_active = %s WHERE id = %s", (0,id))
        conn.commit()
        chake = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return chake
        

    def increment_completed(self, id):
        agent =  self.get_agent_by_id(id)
        
        if agent == None:
            return None
        
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s", (id,))
        conn.commit()
        check = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return check
       


    def increment_failed(self, id):
        agent =  self.get_agent_by_id(id)
        
        if agent == None:
            return None
        
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s", (id,))
        conn.commit()
        check = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return check
       

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)

        if agent is None:
            return None

        completed = agent["completed_missions"]
        failed = agent["failed_missions"]
        total = completed + failed
        if total > 0:
            success_rate = (completed / total) * 100
        else:
            success_rate = 0
        return {
            "completed": completed,
            "failed": failed,
            "total": total,
            "success_rate": success_rate, }

    
    
    def count_active_agents(self):
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active = %s", (1,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0]


dbagant = AgentDB()

