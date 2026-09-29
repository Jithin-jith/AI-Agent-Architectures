"""
Gemini Client Provider and Execution Runner.

This module initializes the Google GenAI SDK client for all agent modules.
It centralizes:
- Environment variable discovery (.env and system environment)
- API key validation
- Model selection defaults (gemini-2.5-flash)

Supported Models:
- gemini-2.5-flash (Fast, cost-efficient, tool-use optimized)
- gemini-2.5-pro (Deep reasoning, long-context analysis)
"""

import os
import sys
from typing import Any, Callable, Dict, List, Optional
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()

# Default model configuration
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def is_gemini_configured() -> bool:
    """
    Checks if a valid-looking GEMINI_API_KEY exists in the environment.

    Returns:
        bool: True if GEMINI_API_KEY is present and not the placeholder.
    """
    key = os.getenv("GEMINI_API_KEY", "").strip()
    return bool(key) and key != "your_gemini_api_key_here"


def get_model_name() -> str:
    """
    Returns the configured Gemini model name.

    Returns:
        str: Model identifier string (e.g., 'gemini-2.5-flash').
    """
    return os.getenv("GEMINI_MODEL", DEFAULT_MODEL)


def get_gemini_client():
    """
    Instantiates and returns the official Google GenAI client if configured.

    Returns:
        google.genai.Client or None: Configured client instance or None.
    """
    if not is_gemini_configured():
        return None

    try:
        from google import genai
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        return genai.Client(api_key=api_key)
    except ImportError:
        return None


def call_gemini(
    prompt: str,
    system_instruction: Optional[str] = None,
    tools: Optional[List[Any]] = None,
    temperature: float = 0.2,
) -> str:
    """
    Executes a prompt against the Gemini API using google-genai SDK.

    Args:
        prompt: User prompt or message.
        system_instruction: Optional system instruction guiding model behavior.
        tools: Optional list of Python functions or Tool objects for function calling.
        temperature: Sampling temperature (lower = more deterministic).

    Returns:
        str: Text output from the model.
    """
    client = get_gemini_client()
    model_name = get_model_name()

    if client is not None:
        try:
            from google.genai import types

            config_args: Dict[str, Any] = {"temperature": temperature}
            if system_instruction:
                config_args["system_instruction"] = system_instruction
            if tools:
                config_args["tools"] = tools

            config = types.GenerateContentConfig(**config_args)

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            return response.text
        except Exception as api_err:
            from .console import console
            console.print(
                f"[dim yellow]Notice: Gemini API temporary issue ({api_err.__class__.__name__}: {str(api_err)[:100]}...). "
                f"Gracefully falling back to deterministic response.[/dim yellow]\n"
            )
            raise api_err
    else:
        # Inform learner that simulation mode is active
        from .console import console
        console.print(
            "[dim yellow]ℹ [SIMULATION MODE] No active GEMINI_API_KEY detected in .env. "
            "Using realistic deterministic simulation. "
            "To use live Gemini 2.5 Flash API calls, add your key to .env.[/dim yellow]\n"
        )
        raise Exception("No active GEMINI_API_KEY detected in .env")
