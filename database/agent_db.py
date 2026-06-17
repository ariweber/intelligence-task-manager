from database.db_connection import DB
from database.utils import check_is_exists

class AgentDB:
    RANK = {'Junior', 'Senior', 'Commander'}

    def create_agent(self, data):
        values = [data["name"], data["specialty"], data["agent_rank"]]
        if not check_is_exists(data["agent_rank"],self.RANK):
           raise ValueError("valid fild agent_rank")
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
        pass
       
    
    def get_agent_by_id(self, id):
        conn = DB.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
        data = cursor.fetchall()
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
       pass


    def increment_failed(self, id):
       pass

    def get_agent_performance(id):
       pass

    def count_active_agents(self):
       pass


dbagant = AgentDB()

print(dbagant.get_agent_by_id(1))