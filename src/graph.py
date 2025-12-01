import json
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.observability import RunLogger

# Initialize Logger
run_logger = RunLogger()

# Init Agents
data_agent = DataAgent()
insight_agent = InsightAgent("Insight")
evaluator_agent = EvaluatorAgent("Evaluator")
creative_agent = CreativeAgent("Creative")

# --- Nodes ---

def data_node(state: AgentState):
    print("🔍 Data Agent analyzing deltas...")
    result = data_agent.execute(state["query"])
    
    run_logger.log_step("DataAgent", {"query": state["query"]}, result)
    
    # Check for failure
    if "error" in result:
        print(f"⚠️ Data Error Detected: {result['error']}")
        return {
            "data_summary": json.dumps(result), # Pass the error so state has the key
            "final_report": f"CRITICAL FAILURE: {result['error']}"
        }
        
    return {"data_summary": json.dumps(result)}

def insight_node(state: AgentState):
    print(" Insight Agent diagnosing drivers...")
    # Safe access to data
    data_str = state.get("data_summary", "{}")
    
    hypo = insight_agent.generate(state["query"], data_str, state.get("critique"))
    
    run_logger.log_step("InsightAgent", {"data_summary": data_str}, hypo)
    return {"hypothesis": hypo}

def evaluator_node(state: AgentState):
    print("Evaluator validating evidence...")
    val = evaluator_agent.validate(state["hypothesis"], state["data_summary"])
    
    run_logger.log_step("EvaluatorAgent", {"hypothesis": state["hypothesis"]}, val)
    return {"validation": val}

def creative_node(state: AgentState):
    print(" Creative Agent generating targeted copy...")
    creatives = creative_agent.generate(state["hypothesis"], ["Ad_Variant_A"])
    
    run_logger.log_step("CreativeAgent", {"insight": state["hypothesis"]}, creatives)
    return {"creatives": creatives}

def reporting_node(state: AgentState):
    print(f" Saving Final Report to {run_logger.log_dir}...")
    
    final_output = {
        "run_id": run_logger.run_id,
        "status": "Success" if not state.get("final_report", "").startswith("CRITICAL") else "Failed",
        "final_insight": state.get("hypothesis"),
        "validation": state.get("validation"),
        "creatives": state.get("creatives"),
        "error_log": state.get("final_report")
    }
    
    with open(f"{run_logger.log_dir}/final_report.json", "w") as f:
        json.dump(final_output, f, indent=2, default=str)
        
    with open("reports/final_report.json", "w") as f:
        json.dump(final_output, f, indent=2, default=str)
        
    return {"final_report": "Saved"}

# --- Logic Edges ---

def check_data_health(state: AgentState):
    """Circuit Breaker: Stop if data is bad."""
    if state.get("final_report", "").startswith("CRITICAL"):
        return "report" # Go straight to end
    return "insight"    # Continue normally

def check_validation(state: AgentState):
    val = state.get("validation", {})
    if val.get("is_valid"):
        return "creative"
    
    if state.get("retry_count", 0) < 3:
        print(f" Rejected: {val.get('critique')} (Retrying...)")
        return "retry"
    
    return "report"

# --- Graph Build ---

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("data", data_node)
workflow.add_node("insight", insight_node)
workflow.add_node("evaluator", evaluator_node)
workflow.add_node("creative", creative_node)
workflow.add_node("report", reporting_node)

# Add Edges
workflow.set_entry_point("data")

# NEW: Add conditional edge after Data to handle errors
workflow.add_conditional_edges(
    "data",
    check_data_health,
    {
        "report": "report", # Failure path
        "insight": "insight" # Success path
    }
)

workflow.add_edge("insight", "evaluator")

workflow.add_conditional_edges("evaluator", check_validation, {
    "creative": "creative", "retry": "insight", "report": "report"
})

workflow.add_edge("creative", "report")
workflow.add_edge("report", END)

app = workflow.compile()