# Module 01: ReAct Agent (Reasoning + Acting)

## 1. Architectural Overview

The **ReAct** (Reasoning + Acting) pattern, introduced by Yao et al. (ICLR 2023), represents the foundational architecture for modern tool-using AI agents. Before ReAct, AI agents either operated in pure reasoning mode (Chain-of-Thought, where the model rationalizes internally without interacting with external reality) or pure acting mode (direct API or tool invocation without verbalizing why the action was chosen).

ReAct unifies both into an iterative, closed-loop execution cycle:

```
                  ┌──────────────────────┐
                  │      User Query      │
                  └──────────┬───────────┘
                             │
                             ▼
                    ┌────────────────┐
              ┌────►│ Thought (LLM)  │◄───┐
              │     └────────┬───────┘    │
              │              │            │
              │              ▼            │
              │     ┌────────────────┐    │
              │     │  Action (Tool) │    │
              │     └────────┬───────┘    │
              │              │            │
              │              ▼            │
              │     ┌────────────────┐    │
              │     │  Observation   │────┘
              │     └────────┬───────┘
              │              │
              └──────────────┼────────────┐
                             ▼            │
                    ┌─────────────────┐   │ (if final answer)
                    │  Final Answer   │   │
                    └─────────────────┘   ▼
```

### The Three Core Primitives

1. **Thought (Reasoning)**:
   The LLM generates a verbal self-reflection on what it currently knows, what information is missing, and what action should be taken next. This decomposes complex multi-hop problems and reduces hallucinations.
2. **Action (Acting)**:
   The LLM selects a specific tool and emits a structured call (e.g., `tool_name(param="value")`).
3. **Observation (Grounding)**:
   The execution environment runs the requested tool, captures the real-world output or error, and appends this observation to the agent's context window.

---

## 2. Practical Scenario & Flow

### User Goal
> *"Find the cheapest flight from Kochi (COK) to Bangalore (BLR) on 2026-10-15 and check whether I have a conflicting meeting that day."*

### Step-by-Step Trajectory
1. **Thought 1**: "I need to find flights between Kochi (COK) and Bangalore (BLR) on 2026-10-15 and also check the user's schedule for conflicts."
2. **Action 1**: `search_flights(origin="COK", destination="BLR", date="2026-10-15")`
3. **Observation 1**: Returned 3 flights:
   - AI-502: Depart 07:00, Arrive 08:15, Price: $65
   - 6E-241: Depart 11:30, Arrive 12:45, Price: $52 (Cheapest)
   - SG-811: Depart 18:00, Arrive 19:15, Price: $58
4. **Thought 2**: "The cheapest flight is 6E-241 departing at 11:30 and arriving at 12:45. Now I must check whether the user has a calendar meeting on 2026-10-15 that conflicts with this travel window."
5. **Action 2**: `get_calendar_events(date="2026-10-15")`
6. **Observation 2**: Returned:
   - 09:00 - 10:00: Team Standup
   - 12:00 - 13:00: Client Strategy Review
7. **Thought 3**: "Flight 6E-241 lands at 12:45, directly conflicting with the Client Strategy Review (12:00 - 13:00). I should check if the early morning flight AI-502 ($65) allows the user to attend the meeting safely."
8. **Final Answer**: Synthesizes the analysis, highlights the cheapest conflicting option vs. the viable non-conflicting flight.

---

## 3. Key Strengths & Failure Modes

### Strengths
- **Dynamic Reactivity**: The agent adapts based on intermediate tool outputs rather than following a rigid path.
- **Traceability & Auditability**: Every decision is explained in human language before an action is executed.
- **Error Recovery**: If a tool returns an error or empty result, the LLM reads the error in the observation and attempts an alternative strategy.

### Failure Modes & Production Mitigations
| Failure Mode | Description | Production Mitigation |
| :--- | :--- | :--- |
| **Infinite Tool Loops** | Agent repeatedly calls the same tool with the same arguments. | Track action history; terminate if duplicate action detected or step limit reached. |
| **Hallucinated Tools** | Model invents functions not defined in the tool catalog. | Strictly validate tool names and arguments against a registry schema before execution. |
| **Context Window Bloat** | Massive tool observations fill up the context. | Truncate, summarize, or extract structured keys from raw API responses before feeding back. |

---

## 4. Hands-on Code Structure

- [tools.py](AI-Agent-Architectures/01_react_agent/tools.py): Mock flight search, calendar inspection, and currency tools with complete type signatures and docstrings.
- [agent.py](AI-Agent-Architectures/01_react_agent/agent.py): Pure ReAct execution engine implementing the Thought-Action-Observation loop using Google Gemini models.
- [main.py](AI-Agent-Architectures/01_react_agent/main.py): Complete executable script demonstrating the flight and calendar conflict resolution scenario.

## 5. Running the Code

```bash
# Activate your virtual environment
.\venv\Scripts\activate

# Run the ReAct agent
python 01_react_agent/main.py
```
