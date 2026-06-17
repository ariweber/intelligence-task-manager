# intelligence-task-manager

## project description

Tasks assigned to them. It uses MySQL as a database to store information about agents and tasks. And fastAPI kvrm to run the local server The project includes two main classes, AgentDB and MissionDB, ABU, BU, the ability to create, update agents and tasks. And managing agents and tasks in the database and the status of tasks by agents. The process of managing the status of tasks is managed according to the rules of the system.


## database setup
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0


## project structure
```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Tables structure

### Agents Table

* id (INT, PRIMARY KEY, AUTO_INCREMENT)
* name (VARCHAR(50)) not null
* specialty (VARCHAR(255)) not null
* is_active (BOOLEAN) default TRUE
* completed_missions (INT) default 0
* failed_missions (INT) default 0
* agent_rank  enum('Junior', 'Senior', 'Commander') (VARCHAR(255)) not null 

### missions table

* id (INT, PRIMARY KEY, AUTO_INCREMENT)
* title (VARCHAR(100))
* description (TEXT)
* location (VARCHAR(50))
* difficulty (INT) 1-10
* importance (INT) 1-10
* status enum('New', 'Assigned', 'In Progress', 'Completed', 'Failed', 'Cancelled') (VARCHAR(50) default 'New')
* risk_level enum('Low', 'Medium', 'High') (VARCHAR(50))
* assigned_agent_id (INT)


## Explanation of the DB classes,  dbconnection, AgentDB, MissionDB

###  dbconnection

* get_connection(): Returns an active connection to MySQL
* create_database(): Creates Intelligence_db if it does not exist.
* create_tables(): Creates both tables if they do not exist.

### AgentDB.py
 
 * create_agent(data): Creates a new agent and returns the agent object.
 * get_all_agents(): Returns a list of all agents
 * get_agent_by_id(id): Returns one agent by ID, or None
 * update_agent(id, data): Updates the specified agent with the provided data.
 * deactivate_agent(id): Sets is_active to False for the specified agent.
 * increment_completed(id): Increments the completed_missions count for the specified agent.
 * increment_failed(id): Updates the number of failed tasks
 * get_agent_performance(id): Returns a dictionary with these keys completed, failed, total, success_rate
 * count_active_agents(): Returns the number of active agents

 ### MissionDB

 * create_mission(data): Creates a new task and returns the entire object
 * get_all_missions(): Returns all tasks
 * get_mission_by_id(id): Returns one task by ID, or None
 * assign_mission(m_id, a_id): Returns one task by ID, or None
 * update_mission_status(id, status)
 * get_open_missions_by_agent(id)
 * count_all_missions()
 * count_by_status(status)
 * count_open_missions()
 * count_critical_missions()
 * get_top_agent()

 ## System rules

 1. rank must be Junior / Senior / Commander. any other value throws an error.
 2. Difficulty and importance must be between 1 and 10 — otherwise an error.
 3. risk_level is calculated automatically when a task is created—the user does not submit it.
 4. An agent with is_active=False cannot accept tasks.
 5. An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
 6. If risk_level=CRITICAL — only an agent with the rank of Commander can accept the task.
 7. Only a task with a status of NEW can be assigned. After assignment: status=ASSIGNED.
 8. Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
 9. Only a task can be completed. IN_PROGRESS and changed to failed or completed status.
 10. Only a task with a status of NEW or ASSIGNED can be canceled — otherwise an error.


 ## How to run
1. Clone the repository
2. Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies: pip install -r requirements.txt
4. Run the database setup command to start the MySQL container
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
5. Run the application (assuming you have a main.py to start the FastAPI server)
uvicorn main:app --reload
6. Access the API documentation at http://localhost:8000/docs




