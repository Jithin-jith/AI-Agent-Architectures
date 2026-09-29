"""
Module 01: ReAct Agent - Main Entry Point.

Hands-on demonstration of the classic ReAct (Think -> Act -> Observe) pattern using Google Gemini.

Scenario:
"Find the cheapest flight from Kochi to Bangalore on 2026-10-15 and check whether I have a meeting that day."

Run with:
    python 01_react_agent/main.py
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from agent import ReActAgent


def main():
    agent = ReActAgent(max_iterations=5)
    query = "Find the cheapest flight from Kochi to Bangalore on 2026-10-15 and check whether I have a meeting that day."
    agent.run(query)


if __name__ == "__main__":
    main()
