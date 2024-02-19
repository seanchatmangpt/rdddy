from datetime import datetime

from pydantic import Field

from rdddy.messages import AbstractCommand, AbstractEvent


class CollaborativeEvent(AbstractEvent):
    agent_name: str = Field("", description="Agent name")


class AgentCreated(CollaborativeEvent):
    """An agent was created"""

    created_at: datetime = Field(default_factory=datetime.now)


class AgentTerminated(CollaborativeEvent):
    reason: str
    terminated_at: datetime = Field(default_factory=datetime.now)


class MessageEvent(CollaborativeEvent):
    recipient_id: int = None
    message_content: str


class MessageSent(MessageEvent):
    pass


class MessageReceived(MessageEvent):
    pass


class TaskEvent(CollaborativeEvent):
    task_id: int
    task_description: str


class TaskAssigned(TaskEvent):
    pass


class TaskCompleted(TaskEvent):
    pass


class TaskFailed(TaskEvent):
    reason: str


class DecisionMade(CollaborativeEvent):
    decision_description: str


class ResourceEvent(CollaborativeEvent):
    resource_type: str
    amount: int


class ResourceAllocation(ResourceEvent):
    pass


class ResourceDeallocation(ResourceEvent):
    pass


class StateChangeEvent(CollaborativeEvent):
    new_state: str


class StateChange(StateChangeEvent):
    pass


class CollaborationEvent(CollaborativeEvent):
    agents_involved: list[int]


class CollaborationInitiated(CollaborationEvent):
    pass


class ConflictEvent(CollaborativeEvent):
    conflicting_agents: list[int] = Field(default_factory=list)


class ConflictDetected(ConflictEvent):
    pass


class ConflictResolved(ConflictEvent):
    resolved_agents: list[int]


class EmergencyShutdown(CollaborativeEvent):
    reason: str


class FeedbackReceived(CollaborativeEvent):
    feedback_content: str


class LearningUpdate(CollaborativeEvent):
    update_description: str


class SystemHealthCheck(CollaborativeEvent):
    health_status: str


class AssignTaskCommand(AbstractCommand):
    task_id: int
    agent_id: int
    task_description: str


class ExecuteTaskCommand(AbstractCommand):
    task_id: int


class MakeDecisionCommand(AbstractCommand):
    decision_description: str


class SendMessageCommand(AbstractCommand):
    recipient_id: int
    message_content: str


class MonitorSystemCommand(AbstractCommand):
    pass


class UpdateLearningCommand(AbstractCommand):
    update_description: str
