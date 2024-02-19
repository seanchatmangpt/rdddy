import os
import pickle
from datetime import datetime

from experiments.workshop_messages import *


class MessageStore:
    def __init__(self, filename):
        self.filename = filename
        self.messages = []

    def add_message(self, message):
        """Add a message to the message store."""
        self.messages.append(message)

    def save_messages_to_disk(self):
        """Save messages to disk using pickle serialization."""
        with open(self.filename, "wb") as file:
            pickle.dump(self.messages, file)

    def load_messages_from_disk(self):
        """Load messages from disk and deserialize using pickle."""
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as file:
                self.messages = pickle.load(file)


class WorkshopSimulator:
    def __init__(self):
        self.message_store = MessageStore("workshop_messages.pkl")

    def simulate_workshop(self):
        # Schedule a workshop
        schedule_message = ScheduleWorkshop(
            workshop_id=1,
            name="Workshop 1",
            start_date=datetime.now(),
            end_date=datetime.now(),
        )
        self.process_message(schedule_message)

        # Assign a presenter
        assign_presenter_message = AssignPresenter(workshop_id=1, presenter_name="John Doe")
        self.process_message(assign_presenter_message)

        # Send invitations
        send_invitations_message = SendInvitations(
            workshop_id=1,
            participant_emails=["email1@example.com", "email2@example.com"],
        )
        self.process_message(send_invitations_message)

        # Accept an invitation
        accept_invitation_message = AcceptInvitation(
            workshop_id=1, participant_email="email1@example.com"
        )
        self.process_message(accept_invitation_message)

        # Update workshop details
        update_details_message = UpdateWorkshopDetails(
            workshop_id=1, name="Updated Workshop", description="Updated Description"
        )
        self.process_message(update_details_message)

        # Cancel the workshop
        cancel_workshop_message = CancelWorkshop(workshop_id=1, reason="Cancellation Reason")
        self.process_message(cancel_workshop_message)

    def process_message(self, message):
        """Process a message and add it to the message store."""
        print(f"Processing message: {message}")
        self.message_store.add_message(message)

    def save_messages_to_disk(self):
        """Save messages to disk."""
        self.message_store.save_messages_to_disk()

    def load_messages_from_disk(self):
        """Load messages from disk."""
        self.message_store.load_messages_from_disk()


if __name__ == "__main__":
    simulator = WorkshopSimulator()
    simulator.simulate_workshop()
    simulator.save_messages_to_disk()

    # Load and print the saved messages
    simulator.load_messages_from_disk()
    for message in simulator.message_store.messages:
        print(message)
