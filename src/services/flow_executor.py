import uuid
from typing import Dict, Any, List, Optional
from src.services.ai_service import AIService
from src.services.langchain_agent import invoke_langchain_agent # Importar o agente LangChain

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
                errors.append(f"Nó {node.get('id')} sem tipo.")
            
            if "data" not in node:
                errors.append(f"Nó {node.get('id')} sem dados.")
            
            if node.get("type") == "agent":
                if "agentType" not in node.get("data", {}):
                    errors.append(f"Nó de agente {node.get('id')} sem agentType.")
                if "provider" not in node.get("data", {}):
                    errors.append(f"Nó de agente {node.get('id')} sem provedor.")
                if "model" not in node.get("data", {}):
                    errors.append(f"Nó de agente {node.get('id')} sem modelo.")

        for edge in flow_data.get("edges", []):
            if "source" not in edge or "target" not in edge:
                errors.append(f"Aresta mal formatada: {edge}")
            else:
                if edge["source"] not in node_ids:
                    errors.append(f"Aresta com nó de origem inválido: {edge['source']}")
                if edge["target"] not in node_ids:
                    errors.append(f"Aresta com nó de destino inválido: {edge['target']}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def find_start_node(self, nodes: Dict[str, Any]) -> Optional[str]:
        """Encontra o nó inicial do fluxo (User Input)"""
        for node_id, node in nodes.items():
            if (node.get("type") == "data" and 
                node.get("data", {}).get("dataType") == "input"):
                return node_id
        return None

    def get_next_nodes(self, current_node_id: str, edges: List[Dict], node_outputs: Dict) -> List[str]:
        """Obtém os próximos nós baseado nas arestas e condições lógicas"""
        next_nodes = []
        
        for edge in edges:
            if edge["source"] == current_node_id:
                # Verificar se é uma aresta condicional
                edge_id = edge.get("id", "")
                if "true" in edge_id.lower():
                    # Aresta para condição verdadeira
                    current_output = node_outputs.get(current_node_id, "")
                    if self._evaluate_condition_result(current_output, True):
                        next_nodes.append(edge["target"])
                elif "false" in edge_id.lower():
                    # Aresta para condição falsa
                    current_output = node_outputs.get(current_node_id, "")
                    if self._evaluate_condition_result(current_output, False):
                        next_nodes.append(edge["target"])
                else:
                    # Aresta normal
                    next_nodes.append(edge["target"])
        
        return next_nodes

    def _evaluate_condition_result(self, output: str, expected: bool) -> bool:
        """Avalia se o resultado de uma condição corresponde ao esperado"""
        if not output:
            return False
        
        output_lower = str(output).lower().strip()
        
        if expected:
            return output_lower in ["true", "verdadeiro", "sim", "yes", "1"]
        else:
            return output_lower in ["false", "falso", "não", "no", "0"]

    def execute_node(self, node: Dict[str, Any], input_data: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa um nó específico"""
        node_type = node["type"]
        node_data = node["data"]
        
        try:
            if node_type == "data":
                return self._execute_data_node(node_data, input_data, context)
            elif node_type == "agent":
                return self._execute_agent_node(node_data, input_data, context)
            elif node_type == "logic":
                return self._execute_logic_node(node_data, input_data, context)
            else:
                return {"success": False, "error": f"Tipo de nó desconhecido: {node_type}"}
        
        except Exception as e:
            return {"success": False, "error": f"Erro ao executar nó: {str(e)}"}

    def _execute_data_node(self, node_data: Dict, input_data: str, context: Dict) -> Dict[str, Any]:
        """Executa nó de dados"""
        data_type = node_data.get("dataType")
        
        if data_type == "input":
            return {"success": True, "output": input_data}
        elif data_type == "output":
            # Para nós de saída, usar o último output do contexto
            last_output = context.get("last_output", input_data)
            return {"success": True, "output": last_output}
        else:
            return {"success": False, "error": f"Tipo de dados desconhecido: {data_type}"}

    def _execute_agent_node(self, node_data: Dict, input_data: str, context: Dict) -> Dict[str, Any]:
        """Executa nó de agente IA"""
        agent_type = node_data.get("agentType")
        provider = node_data.get("provider", "openai")
        model = node_data.get("model", "gpt-3.5-turbo")
        temperature = node_data.get("temperature", 0.7)
        instructions = node_data.get("instructions", "")
        
        # Usar o último output como entrada para este nó
        prompt_input = context.get("last_output", input_data)
        
        if agent_type == "chatbot":
            # Para chatbot, combinar instruções com o input
            if instructions:
                prompt = f"{instructions}\n\nUsuário: {prompt_input}"
            else:
                prompt = prompt_input
            
            ai_response = self.ai_service.get_completion(prompt, provider, model, temperature)
            
        elif agent_type == "analyzer":
            prompt = f"Analise os seguintes dados: {prompt_input}"
            if instructions:
                prompt = f"{instructions}\n\n{prompt}"
            
            ai_response = self.ai_service.get_completion(prompt, provider, model, temperature)
            
        elif agent_type == "generator":
            prompt = f"Gere conteúdo sobre: {prompt_input}"
            if instructions:
                prompt = f"{instructions}\n\n{prompt}"
            
            ai_response = self.ai_service.get_completion(prompt, provider, model, temperature)
        elif agent_type == "langchain_agent":
            # Chamar o agente LangChain
            ai_response = {"output": invoke_langchain_agent(prompt_input)}
        else:
            return {"success": False, "error": f"Tipo de agente desconhecido: {agent_type}"}
        
        if "error" in ai_response:
            return {"success": False, "error": ai_response["error"]}
        
        return {"success": True, "output": ai_response["output"]}

    def _execute_logic_node(self, node_data: Dict, input_data: str, context: Dict) -> Dict[str, Any]:
        """Executa nó de lógica"""
        condition_type = node_data.get("conditionType", "if")
        condition = node_data.get("condition", "")
        
        if condition_type == "if":
            # Usar o último output para avaliar a condição
            current_input = context.get("last_output", input_data)
            
            try:
                # Criar contexto seguro para avaliação
                safe_context = {
                    "__builtins__": {},
                    "input": current_input,
                    "len": len,
                    "str": str,
                    "int": int,
                    "float": float,
                    "bool": bool
                }
                
                # Substituir 'length' por 'len(input)' se necessário
                if "length" in condition:
                    condition = condition.replace("length", "len(str(input))")
                
                # Avaliar condição
                result = eval(condition, safe_context)
                output = "true" if result else "false"
                
                return {"success": True, "output": output}
                
            except Exception as e:
                return {"success": False, "error": f"Erro ao avaliar condição '{condition}': {str(e)}"}
        
        else:
            return {"success": False, "error": f"Tipo de condição desconhecido: {condition_type}"}

    def execute_flow(self, flow_data: Dict[str, Any], initial_input: str = "") -> Dict[str, Any]:
        """Executa o fluxo completo"""
        nodes = {node["id"]: node for node in flow_data.get("nodes", [])}
        edges = flow_data.get("edges", [])
        
        execution_path = []
        node_outputs = {}
        context = {"last_output": initial_input}
        
        # Encontrar o nó inicial
        current_node_id = self.find_start_node(nodes)
        if not current_node_id:
            return {"success": False, "error": "Nó de entrada não encontrado no fluxo."}

        # Executar fluxo
        visited_nodes = set()
        max_iterations = 100  # Prevenir loops infinitos
        iterations = 0
        
        while current_node_id and iterations < max_iterations:
            iterations += 1
            
            # Verificar se já visitamos este nó (prevenir loops)
            if current_node_id in visited_nodes:
                break
            
            current_node = nodes.get(current_node_id)
            if not current_node:
                return {"success": False, "error": f"Nó {current_node_id} não encontrado."}
            
            execution_path.append(current_node_id)
            visited_nodes.add(current_node_id)
            
            # Executar nó atual
            result = self.execute_node(current_node, initial_input, context)
            
            if not result["success"]:
                return {"success": False, "error": result["error"]}
            
            output = result["output"]
            node_outputs[current_node_id] = output
            context["last_output"] = output
            
            # Verificar se é um nó de saída
            if (current_node["type"] == "data" and 
                current_node.get("data", {}).get("dataType") == "output"):
                break
            
            # Encontrar próximos nós
            next_nodes = self.get_next_nodes(current_node_id, edges, node_outputs)
            
            if not next_nodes:
                # Fim do fluxo
                break
            elif len(next_nodes) == 1:
                current_node_id = next_nodes[0]
            else:
                # Múltiplos caminhos - pegar o primeiro válido
                current_node_id = next_nodes[0]
        
        final_output = context["last_output"]
        
        return {
            "success": True, 
            "output": final_output, 
            "execution_path": execution_path, 
            "node_outputs": node_outputs
        }


