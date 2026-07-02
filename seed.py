from src.tickets.controller import create_ticket
from src.tickets.schemas import TicketCreate
from src.tickets.models import Ticket
import random
from sqlalchemy.orm import Session
from src.utils.db import SessionLocal
from src.users.models import User
from src.utils.security import hash_password


db: Session = SessionLocal()


def create_demo_users():
    # ----------------------------
    # Demo Customer
    # ----------------------------
    customer = (
        db.query(User)
        .filter(User.email == "customer@example.com")
        .first()
    )

    if not customer:
        customer = User(
            name="Demo Customer",
            email="customer@example.com",
            hashed_password=hash_password("Customer@123"),
            role="customer"
        )

        db.add(customer)

    # ----------------------------
    # Demo Agent
    # ----------------------------
    agent = (
        db.query(User)
        .filter(User.email == "agent@example.com")
        .first()
    )

    if not agent:
        agent = User(
            name="Demo Agent",
            email="agent@example.com",
            hashed_password=hash_password("Agent@123"),
            role="agent"
        )

        db.add(agent)

    db.commit()

    db.refresh(customer)
    db.refresh(agent)

    print("✅ Demo Customer Ready")
    print("   Email: customer@example.com")
    print("   Password: Customer@123")

    print()

    print("✅ Demo Agent Ready")
    print("   Email: agent@example.com")
    print("   Password: Agent@123")

    return customer, agent


demo_tickets = [
    {
        "title": "Cannot login after password reset",
        "description": "I reset my password yesterday but I still cannot login to my account."
    },
    {
        "title": "Premium payment not reflected",
        "description": "I upgraded to Premium yesterday but my account still shows the free plan."
    },
    {
        "title": "Payment charged twice",
        "description": "My credit card has been charged twice for the same subscription."
    },
    {
        "title": "Need invoice",
        "description": "Can you send me the invoice for last month's payment?"
    },
    {
        "title": "Website is very slow",
        "description": "The dashboard takes almost a minute to load."
    },
    {
        "title": "App crashes",
        "description": "The mobile application crashes immediately after opening."
    },
    {
        "title": "Forgot username",
        "description": "I forgot my username and cannot access my account."
    },
    {
        "title": "Refund request",
        "description": "I'd like to request a refund because I cancelled my subscription."
    },
    {
        "title": "Change email",
        "description": "I need to update the email address associated with my account."
    },
    {
        "title": "Two-factor authentication",
        "description": "The verification code is never sent to my phone."
    },
    {
        "title": "Delete account",
        "description": "Please permanently delete my account and all associated data."
    },
    {
        "title": "Upload issue",
        "description": "Uploading my profile picture always fails."
    },
    {
        "title": "API error",
        "description": "Every request to the API returns a 500 Internal Server Error."
    },
    {
        "title": "Notifications missing",
        "description": "I stopped receiving email notifications this week."
    },
    {
        "title": "Dark mode",
        "description": "Please add dark mode support to the dashboard."
    },
    {
        "title": "Export reports",
        "description": "I need an option to export reports as Excel files."
    },
    {
        "title": "Phone number",
        "description": "I'd like to change the phone number linked to my account."
    },
    {
        "title": "Subscription cancelled",
        "description": "My subscription became inactive even though I already paid."
    },
    {
        "title": "Dashboard bug",
        "description": "Graphs on the analytics dashboard are not loading correctly."
    },
    {
        "title": "Password reset email",
        "description": "I'm not receiving the password reset email."
    }
]
def create_demo_tickets(customer):
    created = 0

    statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    for ticket in demo_tickets:

        # Skip if ticket already exists
        existing_ticket = (
            db.query(Ticket)
            .filter(
                Ticket.title == ticket["title"],
                Ticket.customer_id == customer.id
            )
            .first()
        )

        if existing_ticket:
            continue

        ticket_data = TicketCreate(
            title=ticket["title"],
            description=ticket["description"]
        )

        try:
            new_ticket = create_ticket(
                db=db,
                ticket=ticket_data,
                current_user=customer
            )

            new_ticket.status = random.choice(statuses)

            db.commit()

            created += 1

        except Exception as e:
            db.rollback()
            print(f"❌ Failed to create '{ticket['title']}'")
            print(e)

    print(f"✅ Created {created} demo tickets.")
def main():
    customer, agent = create_demo_users()

    create_demo_tickets(customer)

    print()
    print("🎉 Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    main()