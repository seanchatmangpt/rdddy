from datetime import datetime
from pydantic import BaseModel
from enum import Enum

from denz.actor import Message


# Define an enumeration for workshop statuses
class WorkshopStatus(str, Enum):
    PLANNED = "Planned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


# Base class for messages
class WorkshopMessage(Message):
    workshop_id: int


# Commands
class ScheduleWorkshop(WorkshopMessage):
    name: str
    start_date: datetime
    end_date: datetime


class AssignPresenter(WorkshopMessage):
    presenter_name: str


class SendInvitations(WorkshopMessage):
    participant_emails: list


class AcceptInvitation(WorkshopMessage):
    participant_email: str


class UpdateWorkshopDetails(WorkshopMessage):
    name: str
    description: str


class CancelWorkshop(WorkshopMessage):
    reason: str


# Events
class WorkshopScheduled(WorkshopMessage):
    name: str
    start_date: datetime
    end_date: datetime
    status: WorkshopStatus = WorkshopStatus.PLANNED


class PresenterAssigned(WorkshopMessage):
    presenter_name: str


class InvitationsSent(WorkshopMessage):
    sent_to: list


class InvitationAccepted(WorkshopMessage):
    participant_email: str


class WorkshopDetailsUpdated(WorkshopMessage):
    name: str
    description: str


class WorkshopCanceled(WorkshopMessage):
    reason: str
    status: WorkshopStatus = WorkshopStatus.COMPLETED


# Queries
class GetWorkshopDetails(WorkshopMessage):
    pass


class ListWorkshops(WorkshopMessage):
    pass
