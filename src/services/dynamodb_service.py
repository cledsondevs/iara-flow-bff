
import boto3
import os
import uuid
from datetime import datetime

class DynamoDBService:
    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("Credenciais da AWS não configuradas")
        
        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )
        
        self.flows_table_name = "iara-flows"
        self.executions_table_name = "iara-flow-executions"
        
        self._create_tables()

    def _create_tables(self):
        try:
            self.dynamodb.create_table(
                TableName=self.flows_table_name,
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"}
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            )
            print(f"Tabela {self.flows_table_name} criada com sucesso")
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            print(f"Tabela {self.flows_table_name} já existe")
        
        try:
            self.dynamodb.create_table(
                TableName=self.executions_table_name,
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"}
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            )
            print(f"Tabela {self.executions_table_name} criada com sucesso")
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            print(f"Tabela {self.executions_table_name} já existe")

    def create_flow(self, data):
        try:
            table = self.dynamodb.Table(self.flows_table_name)
            flow_id = str(uuid.uuid4())
            
            item = {
                "id": flow_id,
                "name": data.get("name", ""),
                "description": data.get("description", ""),
                "flow_data": data.get("flow_data", {}),
                "status": "created",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=item)
            
            return {"success": True, "flow": item}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_flows(self):
        try:
            table = self.dynamodb.Table(self.flows_table_name)
            response = table.scan()
            return {"success": True, "flows": response.get("Items", [])}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_flow(self, flow_id):
        try:
            table = self.dynamodb.Table(self.flows_table_name)
            response = table.get_item(Key={"id": flow_id})
            
            if "Item" in response:
                return {"success": True, "flow": response["Item"]}
            else:
                return {"success": False, "error": "Fluxo não encontrado"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_flow(self, flow_id, data):
        try:
            table = self.dynamodb.Table(self.flows_table_name)
            
            update_expression = "SET "
            expression_attribute_values = {}
            
            for key, value in data.items():
                if key != "id":
                    update_expression += f"{key} = :{key}, "
                    expression_attribute_values[f":{key}"] = value
            
            update_expression += "updated_at = :updated_at"
            expression_attribute_values[":updated_at"] = datetime.utcnow().isoformat()
            
            response = table.update_item(
                Key={"id": flow_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            
            return {"success": True, "flow": response["Attributes"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_flow(self, flow_id):
        try:
            table = self.dynamodb.Table(self.flows_table_name)
            table.delete_item(Key={"id": flow_id})
            return {"success": True, "message": "Fluxo deletado com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_execution(self, data):
        try:
            table = self.dynamodb.Table(self.executions_table_name)
            execution_id = str(uuid.uuid4())
            
            item = {
                "id": execution_id,
                "flow_id": data["flow_id"],
                "input_data": data.get("input_data", {}),
                "status": "running",
                "started_at": datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=item)
            
            return {"success": True, "execution": item}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_execution(self, execution_id, data):
        try:
            table = self.dynamodb.Table(self.executions_table_name)
            
            update_expression = "SET "
            expression_attribute_values = {}
            
            for key, value in data.items():
                if key != "id":
                    update_expression += f"{key} = :{key}, "
                    expression_attribute_values[f":{key}"] = value
            
            update_expression = update_expression.rstrip(", ")
            
            response = table.update_item(
                Key={"id": execution_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            
            return {"success": True, "execution": response["Attributes"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_execution(self, execution_id):
        try:
            table = self.dynamodb.Table(self.executions_table_name)
            response = table.get_item(Key={"id": execution_id})
            
            if "Item" in response:
                return {"success": True, "execution": response["Item"]}
            else:
                return {"success": False, "error": "Execução não encontrada"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_flow_executions(self, flow_id):
        try:
            table = self.dynamodb.Table(self.executions_table_name)
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr("flow_id").eq(flow_id)
            )
            return {"success": True, "executions": response.get("Items", [])}
        except Exception as e:
            return {"success": False, "error": str(e)}

