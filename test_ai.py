from src.ai.service import analyze_ticket

result = analyze_ticket(
    """
    I paid for Premium yesterday but my account still says Free.
    Please help.
    """
)

print(result)