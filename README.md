# Kasparro Agentic Facebook Analyst

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Orchestrator](https://img.shields.io/badge/LangGraph-v0.1-purple)
![AI](https://img.shields.io/badge/OpenAI-GPT--4-green)
![License](https://img.shields.io/badge/License-MIT-grey)

An autonomous multi-agent system that diagnoses Facebook Ads performance drops, validates hypotheses using statistical evidence, and generates creative solutions.

## 🏗️ Architecture Diagram

The system uses **LangGraph** to implement a cyclic **Planner-Evaluator-Action** workflow. Unlike linear chains, this system allows for self-correction: if the Evaluator rejects a hypothesis, the Insight Agent is forced to retry with specific feedback.

```mermaid
graph TD
    Start([Start]) --> Data[Data Agent]
    Data --> Insight[Insight Agent]
    Insight --> Evaluator[Evaluator Agent]
    
    Evaluator -- "Validated (Success)" --> Creative[Creative Agent]
    Evaluator -- "Rejected (Retry)" --> Insight
    Evaluator -- "Max Retries Reached" --> Report[Final Report]
    
    Creative --> Report
    Report --> End([End])
    
    style Start fill:#f9f,stroke:#333
    style Data fill:#e1f5fe,stroke:#01579b
    style Insight fill:#fff9c4,stroke:#fbc02d
    style Evaluator fill:#f8bbd0,stroke:#880e4f
    style Creative fill:#c8e6c9,stroke:#2e7d32
    style Report fill:#e0e0e0,stroke:#333



Quick Start:-
Follow these steps to setup the environment.

1. Installation


git clone [https://github.com/minnu1102/kasparro-agentic-fb-analyst-poorna-trishitha-paladugu.git](https://github.com/minnu1102/kasparro-agentic-fb-analyst-poorna-trishitha-paladugu.git)

cd kasparro-agentic-fb-analyst-poorna-trishitha-paladugu

# Install dependencies
pip install -r requirements.txt
2. Configuration
Create a .env file in the root directory and add your API Key:

OPENAI_API_KEY=sk-proj-...
# OR if using Gemini
# GOOGLE_API_KEY=AIzaSy...

 Data Instructions:-
This project includes a synthetic data generator that engineers a specific "Ad Fatigue" scenario (Frequency increases while CTR decreases over 30 days).

Run this command to generate the dataset:

python -m data.generate_data

This will create data/synthetic_fb_data.csv.

Exact CLI Command:-
To run the full agentic workflow:

python run.py

Validation Description:-
The core innovation of this system is the Evaluator Agent, which acts as a "Unit Test" for the Analyst's insights. It prevents hallucination by enforcing strict statistical rules defined in prompts/evaluator.md:

Fatigue Check: If "Fatigue" is diagnosed, the data must show Average Frequency > 2.0 AND a negative correlation between Frequency and CTR.

Spend Check: If "Scaling" is diagnosed, the Spend trend must be positive.

Feedback Loop: If these conditions are not met, the Evaluator rejects the hypothesis, and the graph routes execution back to the Insight Agent with a critique.

Example Outputs:-
After a successful run, the system produces reports/final_report.json.

Actual V2 Run Output:

JSON

{
  "final_insight": {
    "hypothesis": "ROAS dropped due to significant CTR decline (Ad Fatigue).",
    "reasoning": "While Spend remained constant ($1000), Clicks plummeted by 48.91% (920 vs 470). This caused ROAS to drop from 138.0 to 70.5. The stable impressions rule out audience size issues, confirming creative fatigue."
  },
  "validation": {
    "is_valid": true,
    "confidence": 1.0,
    "critique": "Passed. Data supports the negative correlation."
  },
  "creatives": {
    "suggestions": [
      "Are You Making This Costly Mistake?",
      "The Secret They Don't Want You To Know",
      "You Won't Believe What Happens Next!"
    ]
  }
}

Engineering Decisions:-
LangGraph over Linear Chains: Used for state management and cyclic retries.

Pandas for Math: Decoupled calculation from the LLM to ensure arithmetic accuracy.

TypedDict State: Strictly typed state management in src/state.py to prevent data corruption.

Rich Logging: Implemented semantic logging in the terminal for real-time observability.

Submitted by Poorna Trishitha Paladugu