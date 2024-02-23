from typing import cast

from experiments.collaboration_context import *
from experiments.collaborative_agent import CollaborativeAgent
from rdddy.actor_system import ActorSystem


class AlbertoBrandoliniAgent(CollaborativeAgent):
    def handle_agent_created(self, event: AgentCreated):
        print(f"Alberto Brandolini created with name: {event.agent_name}")

    def handle_message_sent(self, event: MessageSent):
        print(
            f"Alberto Brandolini sent a message to Greg Young: {event.message_content}"
        )

    def handle_task_assigned(self, event: TaskAssigned):
        print(
            f"Alberto Brandolini assigned a task (ID: {event.task_id}): {event.task_description}"
        )

    def handle_task_completed(self, event: TaskCompleted):
        print(
            f"Alberto Brandolini completed a task (ID: {event.task_id}): {event.task_description}"
        )

    def handle_decision_made(self, event: DecisionMade):
        print(
            f"Alberto Brandolini made a significant decision: {event.decision_description}"
        )

    def handle_resource_allocation(self, event: ResourceAllocation):
        print(
            f"Alberto Brandolini allocated {event.amount} units of {event.resource_type} resources."
        )

    def handle_resource_deallocation(self, event: ResourceDeallocation):
        print(
            f"Alberto Brandolini deallocated {event.amount} units of {event.resource_type} resources."
        )

    def handle_feedback_received(self, event: FeedbackReceived):
        print(f"Alberto Brandolini received feedback: {event.feedback_content}")

    def handle_learning_update(self, event: LearningUpdate):
        print(
            f"Alberto Brandolini updated its behavior based on learning: {event.update_description}"
        )

    def handle_system_health_check(self, event: SystemHealthCheck):
        print(f"System health check report: {event.health_status}")


class GregYoungAgent(CollaborativeAgent):
    def handle_message_received(self, event: MessageReceived):
        print(
            f"Greg Young received a message from Alberto Brandolini: {event.message_content}"
        )

    def handle_collaboration_initiated(self, event: CollaborationInitiated):
        agents_involved = ", ".join(map(str, event.agents_involved))
        print(
            f"Collaboration initiated by Alberto Brandolini and Greg Young: {agents_involved}"
        )

    def handle_conflict_detected(self, event: ConflictDetected):
        conflicting_agents = ", ".join(map(str, event.conflicting_agents))
        print(
            f"Conflict detected among Alberto Brandolini and Greg Young: {conflicting_agents}"
        )

    def handle_conflict_resolved(self, event: ConflictResolved):
        resolved_agents = ", ".join(map(str, event.resolved_agents))
        print(
            f"Conflict resolved among Alberto Brandolini and Greg Young: {resolved_agents}"
        )

    def handle_emergency_shutdown(self, event: EmergencyShutdown):
        print(f"Emergency shutdown triggered. Reason: {event.reason}")


# Define the event storming results
event_results = [
    AgentCreated(actor_id=1),
    AgentCreated(actor_id=2),
    MessageSent(recipient_id=2, message_content="Brainstorming ideas"),
    MessageReceived(recipient_id=2, message_content="Received brainstorming ideas"),
    TaskAssigned(task_id=1, task_description="Write book content"),
    TaskCompleted(task_id=1, task_description="Completed writing chapter 1"),
    DecisionMade(actor_id=1, decision_description="Select book cover design"),
    ResourceAllocation(actor_id=1, resource_type="Design", amount=1),
    ResourceDeallocation(actor_id=1, resource_type="Design", amount=1),
    CollaborationInitiated(agents_involved=[1, 2]),
    ConflictDetected(conflicting_agents=[1, 2]),
    ConflictResolved(resolved_agents=[1, 2], conflicting_agents=[1, 2]),
    EmergencyShutdown(reason="Technical issue"),
    FeedbackReceived(actor_id=1, feedback_content="Positive feedback received"),
    LearningUpdate(actor_id=1, update_description="Improved writing style"),
    SystemHealthCheck(health_status="Healthy"),
]

import anyio


class AgentSystem:
    pass


async def main():
    sys = ActorSystem()

    alberto_brandolini = cast(
        AlbertoBrandoliniAgent, await sys.actor_of(AlbertoBrandoliniAgent)
    )
    greg_young = cast(GregYoungAgent, await sys.actor_of(GregYoungAgent))

    event_results = [
        AgentCreated(),
        AgentCreated(),
        MessageSent(
            message_content="Brainstorming ideas",
        ),
        MessageReceived(
            message_content="Received brainstorming ideas",
        ),
        TaskAssigned(
            task_id=1,
            task_description="Write book content",
        ),
        TaskCompleted(
            task_id=1,
            task_description="Completed writing chapter 1",
        ),
        DecisionMade(
            decision_description="Select book cover design",
        ),
        ResourceAllocation(resource_type="Design", amount=1),
        ResourceDeallocation(resource_type="Design", amount=1),
        CollaborationInitiated(
            agents_involved=[alberto_brandolini.actor_id, greg_young.actor_id]
        ),
        ConflictDetected(
            conflicting_agents=[alberto_brandolini.actor_id, greg_young.actor_id]
        ),
        ConflictResolved(
            resolved_agents=[alberto_brandolini.actor_id, greg_young.actor_id]
        ),
        EmergencyShutdown(reason="Technical issue"),
        FeedbackReceived(
            feedback_content="Positive feedback received",
        ),
        LearningUpdate(
            update_description="Improved writing style",
        ),
        SystemHealthCheck(health_status="Healthy"),
    ]

    for event in event_results:
        await sys.publish(event)


if __name__ == "__main__":
    anyio.run(main)
