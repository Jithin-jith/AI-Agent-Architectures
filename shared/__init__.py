"""
Shared Utilities Package for AI Agent Architectures.
Provides centralized Gemini client initialization, environment configuration,
and rich terminal logging for hands-on architectural implementations.
"""

from .gemini_client import get_gemini_client, get_model_name, is_gemini_configured
from .console import AgentConsole

__all__ = ["get_gemini_client", "get_model_name", "is_gemini_configured", "AgentConsole"]
