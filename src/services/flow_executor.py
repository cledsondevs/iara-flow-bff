import uuid
from typing import Dict, Any
from src.services.ai_service import AIService

class FlowExecutor:
    def __init__(self):
        self.ai_service = AIService()

    def validate_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        warnings = []

        if "nodes" not in flow_data or not isinstance(flow_data["nodes"], list):
            errors.append("O fluxo deve conter uma lista de nós ('nodes').")
            
        if "edges" not in flow_data or not isinstance(flow_data["edges"], list):
            errors.append("O fluxo deve conter uma lista de arestas ('edges').")

        node_ids = set()
        for node in flow_data.get("nodes", []):
            if "id" not in node:
                errors.append(f"Nó sem ID: {node}")
            else:
                node_ids.add(node["id"])
            
            if "type" not in node:
                errors.append(f"Nó {node.get("id")} sem tipo.")
            
            if "data" not in node:
                errors.append(f"Nó {node.get("id")} sem dados.")
            
            if node.get("type") == "agent":
                if "agentType" not in node.get("data", {}):
                    errors.append(f"Nó de agente {node.get("id")} sem agentType.")
                if "provider" not in node.get("data", {}):
                    errors.append(f"Nó de agente {node.get("id")} sem provedor.")
                if "model" not in node.get("data", {}):
                    errors.append(f"Nó de agente {node.get("id")} sem modelo.")

        for edge in flow_data.get("edges", []):
            if "source" not in edge or "target" not in edge:
                errors.append(f"Aresta mal formatada: {edge}")
            else:
                if edge["source"] not in node_ids:
                    errors.append(f"Aresta com nó de origem inválido: {edge["source"]}")
                if edge["target"] not in node_ids:
                    errors.append(f"Aresta com nó de destino inválido: {edge["target"]}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def execute_flow(self, flow_data: Dict[str, Any], initial_input: str = "") -> Dict[str, Any]:
        nodes = {node["id"]: node for node in flow_data.get("nodes", [])}
        edges = flow_data.get("edges", [])
        
        execution_path = []
        node_outputs = {}
        
        # Encontrar o nó inicial (geralmente User Input)
        current_node_id = None
        for node_id, node in nodes.items():
            if node.get("type") == "data" and node.get("data", {}).get("dataType") == "input":
                current_node_id = node_id
                break
        
        if not current_node_id:
            return {"success": False, "error": "Nó de entrada não encontrado no fluxo."}

        # Simular execução
        while current_node_id:
            current_node = nodes.get(current_node_id)
            if not current_node:
                return {"success": False, "error": f"Nó {current_node_id} não encontrado."}
            
            execution_path.append(current_node_id)
            
            node_type = current_node["type"]
            node_data = current_node["data"]
            
            output = None
            
            if node_type == "data":
                if node_data.get("dataType") == "input":
                    output = initial_input
                elif node_data.get("dataType") == "output":
                    # Nó de saída, o fluxo termina aqui
                    output = node_outputs.get(current_node_id, "") # Pega o último output
                    node_outputs[current_node_id] = output
                    break
                
            elif node_type == "agent":
                agent_type = node_data.get("agentType")
                provider = node_data.get("provider")
                model = node_data.get("model")
                instructions = node_data.get("instructions", "")
                
                if agent_type == "chatbot":
                    prompt = node_data.get("prompt", initial_input) # Usar input do nó anterior ou inicial
                    ai_response = self.ai_service.get_completion(prompt, provider, model)
                    if "error" in ai_response:
                        return {"success": False, "error": ai_response["error"]}
                    output = ai_response["output"]
                elif agent_type == "analyzer":
                    data_to_analyze = node_data.get("dataToAnalyze", initial_input)
                    ai_response = self.ai_service.analyze_data(data_to_analyze, provider, model, instructions)
                    if "error" in ai_response:
                        return {"success": False, "error": ai_response["error"]}
                    output = ai_response["output"]
                elif agent_type == "generator":
                    topic = node_data.get("topic", initial_input)
                    ai_response = self.ai_service.generate_content(topic, provider, model, instructions)
                    if "error" in ai_response:
                        return {"success": False, "error": ai_response["error"]}
                    output = ai_response["output"]
                else:
                    return {"success": False, "error": f"Tipo de agente desconhecido: {agent_type}"}
            
            elif node_type == "logic":
                logic_type = node_data.get("logicType")
                if logic_type == "condition":
                    condition = node_data.get("condition", "False")
                    # Para simplificar, vamos apenas avaliar a condição como Python
                    # Em um ambiente real, isso precisaria de um motor de regras mais robusto e seguro
                    try:
                        # Usar o output do nó anterior para a condição
                        context = {"input": initial_input, "prev_output": output} 
                        if eval(condition, {"__builtins__": {}}, context):
                            output = "True"
                        else:
                            output = "False"
                    except Exception as e:
                        return {"success": False, "error": f"Erro ao avaliar condição: {str(e)}"}
                else:
                    return {"success": False, "error": f"Tipo de lógica desconhecido: {logic_type}"}
            
            node_outputs[current_node_id] = output
            
            # Encontrar o próximo nó
            next_node_id = None
            for edge in edges:
                if edge["source"] == current_node_id:
                    next_node_id = edge["target"]
                    break
            
            current_node_id = next_node_id
            
        return {"success": True, "output": output, "execution_path": execution_path, "node_outputs": node_outputs}

