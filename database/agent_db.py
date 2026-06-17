from database.db_connection import DB
from database.utils import check_is_exists

class AgentDB:
    RANK = {'Junior', 'Senior', 'Commander'}
    FIELDS = {"name", "specialty", "agent_rank"}

    def create_agent(self, data):
        values = [data["name"], data["specialty"], data["agent_rank"]]
       
        if not check_is_exists(data["agent_rank"],self.RANK):
           raise ValueError(f"valid fild agent_rank in {self.RANK}, {data["agent_rank"]} Does not fit the options" )
       
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
        
        fields = {key: value for key, value in data.items() if key in self.FIELDS}
        if not self.FIELDS:
            return agent

        if "agent_rank" in fields and not check_is_exists(fields["agent_rank"], self.RANK):
            raise ValueError(f"valid fild agent_rank in {self.RANK}, {data["agent_rank"]} Does not fit the options")

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
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET is_active = %s WHERE id = %s", (0,id))
        chake = cursor.rowcount() > 0
        cursor.close()
        conn.close()
        return chake
        

    def increment_completed(self, id):
        agent =  self.get_agent_by_id(id)
        
        if agent == None:
            return None
        
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(completed_missions) FROM agents WHERE id = %s", (id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0]
       


    def increment_failed(self, id):
        agent =  self.get_agent_by_id(id)
        
        if agent == None:
            return None
        
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(failed_missions) FROM agents WHERE id = %s", (id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0]
       

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)

        if agent is None:
            return None

        completed = agent["completed_missions"]
        failed = agent["failed_missions"]
        total = completed + failed
        if total > 0:
            success_rate = (completed / total) * 100 
        success_rate = 0  

        return {
            "completed": completed,
            "failed": failed,
            "total": total,
            "success_rate": success_rate, }

    def count_active_agents(self):
        agent =  self.get_agent_by_id(id)
        
        if agent == None:
            return None
        
        conn = DB.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active = %S", (1,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data[0]


dbagant = AgentDB()

