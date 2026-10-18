import json
import networkx as nx

# 1. Dataset Configuration Paths
JSON_FILE = "amr_fmea_graph.json"

def load_graph(json_file):
    G = nx.DiGraph()
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for node in data['nodes']:
        G.add_node(node['id'], type=node['type'], desc=node['description'])
    for rel in data['relationships']:
        G.add_edge(rel['source'], rel['target'], type=rel['type'])
    return G

def get_graph_context(query, graph):
    """Topologically traces cascading fault steps 2 steps downstream."""
    matched_nodes = [n for n in graph.nodes if n.lower() in query.lower()]
    if not matched_nodes:
        return None
    
    context_lines = []
    propagated_faults = []
    mitigations = []
    final_effects = []
    
    for node in matched_nodes:
        context_lines.append(f"Focus Entity Detected: {node} ({graph.nodes[node]['desc']})")
        
        # 1-Hop Neighbor Lookup
        for neighbor in graph.successors(node):
            edge = graph.get_edge_data(node, neighbor)
            context_lines.append(f"- [{node}] {edge['type']} -> {neighbor} ({graph.nodes[neighbor]['desc']})")
            
            if graph.nodes[neighbor]['type'] in ['Failure_Mode', 'Electrical']:
                propagated_faults.append(f"{neighbor} ({graph.nodes[neighbor]['desc']})")
            elif graph.nodes[neighbor]['type'] == 'Mitigation':
                mitigations.append(f"{neighbor} ({graph.nodes[neighbor]['desc']})")
                
            # 2-Hop Neighbor Lookup
            for sub_neighbor in graph.successors(neighbor):
                sub_edge = graph.get_edge_data(neighbor, sub_neighbor)
                context_lines.append(f"  - Leads to: [{neighbor}] {sub_edge['type']} -> {sub_neighbor} ({graph.nodes[sub_neighbor]['desc']})")
                
                if graph.nodes[sub_neighbor]['type'] == 'Mitigation':
                    mitigations.append(f"{sub_neighbor} ({graph.nodes[sub_neighbor]['desc']})")
                elif graph.nodes[sub_neighbor]['type'] == 'Effect':
                    final_effects.append(f"{sub_neighbor} ({graph.nodes[sub_neighbor]['desc']})")
                    
    return {
        "raw_context": "\n".join(context_lines),
        "faults": list(set(propagated_faults)),
        "mitigations": list(set(mitigations)),
        "effects": list(set(final_effects))
    }

def query_robot_rag(user_query, graph):
    # Step A: Query structural paths from graph topology
    graph_data = get_graph_context(user_query, graph)
    
    # Step B: Safe verification lookup for user edge cases
    if not graph_data:
        return (
            "--- DETECTED SYSTEM REFUSAL PATH ---\n"
            "I cannot find any cascading fault propagation rules or matching subsystem components "
            "for this entity inside the current Autonomous Mobile Robot architecture graph configuration."
        )
    
    # Step C: Dynamic Local Reasoner Engine
    report = [
        "=================================================================",
        "                 AMR ENGINEERING SAFETY ANALYSIS REPORT          ",
        "=================================================================",
        f"CRITICAL FAULT QUERY: {user_query}\n",
        "--- GRAPH LOCAL CONTEXT RETRIEVED ---",
        graph_data["raw_context"],
        "\n--- FMEA RISK & EFFECTS PROPAGATION ANALYSIS ---"
    ]
    
    if graph_data["faults"]:
        report.append("\n[!] IDENTIFIED DANGER CHANNELS / ACTIVE FAULTS:")
        for fault in graph_data["faults"]:
            report.append(f"    -> CRITICAL RISK: {fault}")
            
    if graph_data["mitigations"]:
        report.append("\n[*] AUTOMATED SYSTEMS SAFEGUARD RESPONSES:")
        for mit in graph_data["mitigations"]:
            report.append(f"    -> SAFEGUARD: {mit}")
            
    if graph_data["effects"]:
        report.append("\n[X] TERMINAL DOWNTIME CONSEQUENCES:")
        for eff in graph_data["effects"]:
            report.append(f"    -> SYSTEM IMPACT: {eff}")
            
    report.append("=================================================================")
    return "\n".join(report)

# --- Execute ---
if __name__ == "__main__":
    amr_graph = load_graph(JSON_FILE)
    
    query = "What happens if a wheel falls completely off the frame?"
    ai_response = query_robot_rag(query, amr_graph)
    print(ai_response)