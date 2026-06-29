import json

import google.generativeai as genai

from src.ai.prompts import TICKET_ANALYSIS_PROMPT
from src.ai.schemas import TicketAnalysis
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