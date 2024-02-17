from rdddy.actor import Actor
from rdddy.actor_system import ActorSystem
from slss.domain.collaboration_context import *


class CollaborativeAgent(Actor):
    def handle_agent_created(self, event: AgentCreated):
        print(f"Agent {event.agent_id} created with name: {event.agent_name}")

    def handle_agent_terminated(self, event: AgentTerminated):
        print(f"Agent {event.agent_id} terminated. Reason: {event.reason}")

    def handle_message_sent(self, event: MessageSent):
        print(
            f"Agent {event.actor_id_id} sent a message to Agent {event.recipient_id}: {event.message_content}"
        )

    def handle_message_received(self, event: MessageReceived):
        print(
            f"Agent {event.recipient_id} received a message from Agent {event.actor_id_id}: {event.message_content}"
        )

    def handle_task_assigned(self, event: TaskAssigned):
        print(f"Agent assigned a task (ID: {event.task_id}): {event.task_description}")

    def handle_task_completed(self, event: TaskCompleted):
        print(f"Agent completed a task (ID: {event.task_id}): {event.task_description}")

    def handle_task_failed(self, event: TaskFailed):
        print(
            f"Agent failed to complete a task (ID: {event.task_id}). Reason: {event.reason}"
        )

    def handle_decision_made(self, event: DecisionMade):
        print(
            f"Agent {event.agent_id} made a significant decision: {event.decision_description}"
        )

    def handle_resource_allocation(self, event: ResourceAllocation):
        print(
            f"Agent {event.agent_id} allocated {event.amount} units of {event.resource_type} resources."
        )

    def handle_resource_deallocation(self, event: ResourceDeallocation):
        print(
            f"Agent {event.agent_id} deallocated {event.amount} units of {event.resource_type} resources."
        )

    def handle_state_change(self, event: StateChange):
        print(
            f"Agent {event.agent_id} experienced a state change. New state: {event.new_state}"
        )

    def handle_collaboration_initiated(self, event: CollaborationInitiated):
        agents_involved = ", ".join(map(str, event.agents_involved))
        print(f"Agents {agents_involved} initiated a collaboration.")

    def handle_conflict_detected(self, event: ConflictDetected):
        conflicting_agents = ", ".join(map(str, event.conflicting_agents))
        print(f"Conflict detected among agents: {conflicting_agents}")

    def handle_conflict_resolved(self, event: ConflictResolved):
        resolved_agents = ", ".join(map(str, event.resolved_agents))
        print(f"Conflict resolved among agents: {resolved_agents}")

    def handle_emergency_shutdown(self, event: EmergencyShutdown):
        print(f"Emergency shutdown triggered. Reason: {event.reason}")

    def handle_feedback_received(self, event: FeedbackReceived):
        print(f"Agent {event.agent_id} received feedback: {event.feedback_content}")

    def handle_learning_update(self, event: LearningUpdate):
        print(
            f"Agent {event.agent_id} updated its behavior based on learning: {event.update_description}"
        )

    def handle_system_health_check(self, event: SystemHealthCheck):
        print(f"System health check report: {event.health_status}")


import anyio


async def main():
    sys = ActorSystem()

    agent1 = sys.actor_of(CollaborativeAgent)
    agent2 = sys.actor_of(CollaborativeAgent)

    await sys.send(
        agent1.actor_id,
        LearningUpdate(
            agent_id=agent1.actor_id, update_description="Two agents are learning"
        ),
    )


if __name__ == "__main__":
    anyio.run(main)
