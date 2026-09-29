"""
Module 01: ReAct Agent - Tool Definitions.

This module provides mock external tools for flight search, calendar inspection,
and currency conversion. Each tool is written with complete type annotations,
comprehensive docstrings, and deterministic outputs to demonstrate ReAct execution.

In a production system, these functions would interface with real airline APIs (e.g. Amadeus,
Google Flights) and calendar systems (Google Calendar API, Microsoft Graph).
"""

from typing import Any, Callable, Dict
import json


def search_flights(origin: str, destination: str, date: str) -> str:
    """
    Searches available commercial flights between an origin and destination airport on a given date.

    Args:
        origin (str): 3-letter IATA airport code for departure (e.g., 'COK' for Kochi, 'BLR' for Bangalore).
        destination (str): 3-letter IATA airport code for arrival (e.g., 'BLR', 'BOM', 'DEL').
        date (str): Travel date formatted as YYYY-MM-DD (e.g., '2026-10-15').

    Returns:
        str: JSON-encoded string containing a list of available flight itineraries,
             including airline code, flight number, departure time, arrival time, and price in USD.

    Example:
        >>> search_flights("COK", "BLR", "2026-10-15")
        '[{"flight": "6E-241", "airline": "IndiGo", "departure": "11:30", "arrival": "12:45", "price_usd": 52}, ...]'
    """
    origin = origin.upper().strip()
    destination = destination.upper().strip()

    # Mock database of flights between Kochi (COK) and Bangalore (BLR)
    if origin == "COK" and destination == "BLR":
        flights = [
            {
                "flight_number": "AI-502",
                "airline": "Air India",
                "departure": "07:00",
                "arrival": "08:15",
                "duration": "1h 15m",
                "price_usd": 65,
                "stops": 0,
            },
            {
                "flight_number": "6E-241",
                "airline": "IndiGo",
                "departure": "11:30",
                "arrival": "12:45",
                "duration": "1h 15m",
                "price_usd": 52,
                "stops": 0,
                "notes": "Cheapest non-stop option",
            },
            {
                "flight_number": "SG-811",
                "airline": "SpiceJet",
                "departure": "18:00",
                "arrival": "19:15",
                "duration": "1h 15m",
                "price_usd": 58,
                "stops": 0,
            },
        ]
        return json.dumps({"status": "success", "query_date": date, "results_count": len(flights), "flights": flights}, indent=2)

    return json.dumps({
        "status": "error",
        "message": f"No flights found for route {origin} -> {destination} on {date}. Try 'COK' to 'BLR'."
    })


def get_calendar_events(date: str) -> str:
    """
    Retrieves the user's scheduled calendar meetings, appointments, and events for a specific date.

    Args:
        date (str): Target date formatted as YYYY-MM-DD (e.g., '2026-10-15').

    Returns:
        str: JSON-encoded string listing scheduled events with their start time, end time,
             title, and whether the event is mandatory or flexible.

    Example:
        >>> get_calendar_events("2026-10-15")
        '[{"time": "12:00 - 13:00", "title": "Client Strategy Review", "mandatory": true}]'
    """
    if date == "2026-10-15":
        events = [
            {
                "id": "evt-101",
                "start_time": "09:00",
                "end_time": "10:00",
                "title": "Engineering Team Standup",
                "mandatory": False,
                "location": "Virtual / Google Meet",
            },
            {
                "id": "evt-102",
                "start_time": "12:00",
                "end_time": "13:00",
                "title": "Key Client Strategy Review",
                "mandatory": True,
                "location": "Bangalore Office / Room 4B",
                "notes": "Critical meeting with client stakeholders. In-person attendance required.",
            },
            {
                "id": "evt-103",
                "start_time": "16:30",
                "end_time": "17:00",
                "title": "Weekly 1:1 with Engineering Lead",
                "mandatory": False,
                "location": "Virtual",
            },
        ]
        return json.dumps({"status": "success", "date": date, "events": events}, indent=2)

    return json.dumps({"status": "success", "date": date, "events": [], "message": "No scheduled events on this date."})


def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Converts a monetary sum from one currency to another using current spot exchange rates.

    Args:
        amount (float): The numeric monetary quantity to convert.
        from_currency (str): 3-letter currency code for source (e.g., 'USD', 'INR', 'EUR').
        to_currency (str): 3-letter currency code for target (e.g., 'INR', 'USD').

    Returns:
        str: JSON-encoded string containing converted amount and exchange rate used.
    """
    from_curr = from_currency.upper().strip()
    to_curr = to_currency.upper().strip()

    rates = {
        ("USD", "INR"): 86.50,
        ("INR", "USD"): 1 / 86.50,
        ("EUR", "INR"): 92.00,
        ("USD", "EUR"): 0.94,
    }

    if (from_curr, to_curr) in rates:
        rate = rates[(from_curr, to_curr)]
        converted = round(amount * rate, 2)
        return json.dumps({
            "status": "success",
            "original_amount": amount,
            "from": from_curr,
            "to": to_curr,
            "rate": rate,
            "converted_amount": converted
        })

    return json.dumps({
        "status": "error",
        "message": f"Exchange rate between {from_curr} and {to_curr} is not supported in mock registry."
    })


# Central Tool Registry mapping tool name strings to executable Python callables
TOOL_REGISTRY: Dict[str, Callable[..., str]] = {
    "search_flights": search_flights,
    "get_calendar_events": get_calendar_events,
    "convert_currency": convert_currency,
}

TOOL_DESCRIPTIONS: str = """
Available Tools:
1. search_flights(origin: str, destination: str, date: str) -> str
   Search commercial flight options between airport codes (e.g. COK to BLR) on YYYY-MM-DD.
2. get_calendar_events(date: str) -> str
   Retrieve scheduled calendar meetings and conflicts for the user on YYYY-MM-DD.
3. convert_currency(amount: float, from_currency: str, to_currency: str) -> str
   Convert monetary amount between currencies (e.g. USD to INR).
"""
