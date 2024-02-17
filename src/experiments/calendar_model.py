from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from denz.actor import Event, Command


class VEvent(BaseModel):
    """
    Represents a calendar event (VEvent from the iCalendar specification).
    """

    summary: str
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None
    location: Optional[str] = None
    attendees: Optional[list[str]] = []


# Domain Event Classes for Calendar Management Lifecycle using VEvent


class EventScheduled(Event):
    """
    Event when an event is successfully scheduled on the calendar.
    """

    event_id: int
    event_details: VEvent


class EventUpdated(Event):
    """
    Event when an existing event on the calendar is updated.
    """

    event_id: int
    new_details: VEvent


class SchedulingDecisionMade(Event):
    """
    Event when a decision to schedule an event is made.
    """

    event_details: VEvent


class UpdateDecisionMade(Event):
    """
    Event when a decision to update an existing event is made.
    """

    event_id: int
    updated_details: VEvent


# Domain Event Classes for Calendar Management Lifecycle


class UserInputReceived(Event):
    """
    Event triggered when a user's input or request is received.
    """

    input_text: str


class InputInterpreted(Event):
    """
    Event triggered when the user's input has been interpreted.
    """

    interpreted_action: str
    details: Optional[dict] = None


class DeletionDecisionMade(Event):
    """
    Event when a decision to delete an event is made.
    """

    event_id: int


class EventDeleted(Event):
    """
    Event when an event is removed from the calendar.
    """

    event_id: int


class SchedulingConflictDetected(Event):
    """
    Event when a scheduling conflict is detected.
    """

    conflicting_events: list[int]


class ConflictResolved(Event):
    """
    Event when a scheduling conflict is resolved.
    """

    resolved_action: str


class UserNotified(Event):
    """
    Event when the user is notified of a calendar action.
    """

    notification_details: str


class ErrorOccurred(Event):
    """
    Event when an error is encountered.
    """

    error_message: str


class ReminderSet(Event):
    """
    Event when a reminder is set for an event.
    """

    event_id: int
    reminder_time: datetime


class ReminderTriggered(Event):
    """
    Event when a reminder for an event is triggered.
    """

    event_id: int


class UserPreferencesUpdated(Event):
    """
    Event when user preferences related to calendar management are updated.
    """

    updated_preferences: dict


class CalendarShared(Event):
    """
    Event when a calendar is shared with another user.
    """

    shared_with_user_id: int


class CalendarAccessModified(Event):
    """
    Event when shared calendar access permissions are modified.
    """

    shared_user_id: int
    new_permissions: dict


class AddEventCommand(Command):
    """
    Command to add a new event to the calendar.
    """

    event_details: VEvent


class UpdateEventCommand(Command):
    """
    Command to update an existing event in the calendar.
    """

    event_id: int
    updated_details: VEvent


class DeleteEventCommand(Command):
    """
    Command to delete an event from the calendar.
    """

    event_id: int
