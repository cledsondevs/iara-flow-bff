import os
import psycopg2
from datetime import datetime
import uuid

class PostgreSQLService:
    def __init__(self):
        self.conn = self._get_db_connection()
        self.cur = self.conn.cursor()
        self._create_tables()

    def _get_db_connection(self):
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL não configurada nas variáveis de ambiente.")
        return psycopg2.connect(database_url)

    def _create_tables(self):
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS flows (
                    id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    flow_data JSONB,
                    status VARCHAR(50),
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS executions (
                    id VARCHAR(255) PRIMARY KEY,
                    flow_id VARCHAR(255) REFERENCES flows(id),
                    input_data JSONB,
                    output_data JSONB,
                    status VARCHAR(50),
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    error_message TEXT
                );
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            self.conn.rollback()

    def create_flow(self, data):
        try:
            flow_id = str(uuid.uuid4())
            created_at = datetime.utcnow()
            self.cur.execute("""
                INSERT INTO flows (id, name, flow_data, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (flow_id, data["name"], data.get("flow_data"), data.get("status", "draft"), created_at, created_at))
            self.conn.commit()
            return {"success": True, "flow": {"id": flow_id, "name": data["name"], "flow_data": data.get("flow_data"), "status": data.get("status", "draft"), "created_at": created_at.isoformat(), "updated_at": created_at.isoformat()}}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": str(e)}

    def list_flows(self):
        try:
            self.cur.execute("SELECT id, name, flow_data, status, created_at, updated_at FROM flows")
            rows = self.cur.fetchall()
            flows = []
            for row in rows:
                flows.append({
                    "id": row[0],
                    "name": row[1],
                    "flow_data": row[2],
                    "status": row[3],
                    "created_at": row[4].isoformat() if row[4] else None,
                    "updated_at": row[5].isoformat() if row[5] else None
                })
            return {"success": True, "flows": flows}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_flow(self, flow_id):
        try:
            self.cur.execute("SELECT id, name, flow_data, status, created_at, updated_at FROM flows WHERE id = %s", (flow_id,))
            row = self.cur.fetchone()
            if row:
                return {"success": True, "flow": {"id": row[0], "name": row[1], "flow_data": row[2], "status": row[3], "created_at": row[4].isoformat() if row[4] else None, "updated_at": row[5].isoformat() if row[5] else None}}
            else:
                return {"success": False, "error": "Fluxo não encontrado"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_flow(self, flow_id, data):
        try:
            set_clauses = []
            values = []
            for key, value in data.items():
                if key != "id":
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
            
            set_clauses.append("updated_at = %s")
            values.append(datetime.utcnow())
            values.append(flow_id)

            self.cur.execute(f"UPDATE flows SET {', '.join(set_clauses)} WHERE id = %s", tuple(values))
            self.conn.commit()
            return self.get_flow(flow_id)
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": str(e)}

    def delete_flow(self, flow_id):
        try:
            self.cur.execute("DELETE FROM flows WHERE id = %s", (flow_id,))
            self.conn.commit()
            return {"success": True, "message": "Fluxo deletado com sucesso"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": str(e)}

    def create_execution(self, data):
        try:
            execution_id = str(uuid.uuid4())
            started_at = datetime.utcnow()
            self.cur.execute("""
                INSERT INTO executions (id, flow_id, input_data, status, started_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (execution_id, data["flow_id"], data.get("input_data"), data.get("status", "running"), started_at))
            self.conn.commit()
            return {"success": True, "execution": {"id": execution_id, "flow_id": data["flow_id"], "input_data": data.get("input_data"), "status": data.get("status", "running"), "started_at": started_at.isoformat()}}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": str(e)}

    def update_execution(self, execution_id, data):
        try:
            set_clauses = []
            values = []
            for key, value in data.items():
                if key != "id":
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
            
            values.append(execution_id)

            self.cur.execute(f"UPDATE executions SET {', '.join(set_clauses)} WHERE id = %s", tuple(values))
            self.conn.commit()
            return self.get_execution(execution_id)
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": str(e)}

    def get_execution(self, execution_id):
        try:
            self.cur.execute("SELECT id, flow_id, input_data, output_data, status, started_at, completed_at, error_message FROM executions WHERE id = %s", (execution_id,))
            row = self.cur.fetchone()
            if row:
                return {"success": True, "execution": {"id": row[0], "flow_id": row[1], "input_data": row[2], "output_data": row[3], "status": row[4], "started_at": row[5].isoformat() if row[5] else None, "completed_at": row[6].isoformat() if row[6] else None, "error_message": row[7]}}
            else:
                return {"success": False, "error": "Execução não encontrada"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_flow_executions(self, flow_id):
        try:
            self.cur.execute("SELECT id, flow_id, input_data, output_data, status, started_at, completed_at, error_message FROM executions WHERE flow_id = %s", (flow_id,))
            rows = self.cur.fetchall()
            executions = []
            for row in rows:
                executions.append({
                    "id": row[0],
                    "flow_id": row[1],
                    "input_data": row[2],
                    "output_data": row[3],
                    "status": row[4],
                    "started_at": row[5].isoformat() if row[5] else None,
                    "completed_at": row[6].isoformat() if row[6] else None,
                    "error_message": row[7]
                })
            return {"success": True, "executions": executions}
        except Exception as e:
            return {"success": False, "error": str(e)}


