import json

import google.generativeai as genai

from src.ai.prompts import TICKET_ANALYSIS_PROMPT,REPLY_GENERATION_PROMPT,SEARCH_TICKET_PROMPT,INSIGHTS_PROMPT
from src.ai.schemas import TicketAnalysis,TicketSearchFilters
from src.utils.settings import settings


genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_ticket(ticket: str) -> TicketAnalysis:

    prompt = TICKET_ANALYSIS_PROMPT.format(ticket=ticket)

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown code fences if Gemini returns them
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    data = json.loads(text)

    return TicketAnalysis(**data)

def generate_reply(ticket: str) -> str:

    prompt = REPLY_GENERATION_PROMPT.format(
        ticket=ticket
    )

    response = model.generate_content(prompt)

    return response.text.strip()


def search_filters(query: str) -> TicketSearchFilters:

    prompt = SEARCH_TICKET_PROMPT.format(query=query)

    response = model.generate_content(prompt)

    text = response.text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    data = json.loads(text)

    return TicketSearchFilters(**data)


def generate_insights(stats: str) -> str:

    prompt = INSIGHTS_PROMPT.format(
        stats=stats
    )

    response = model.generate_content(prompt)

    return response.text.strip()