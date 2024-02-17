from jinja2 import Template

# Define the actor name and a list of messages
actor_name = "MyActor"
messages = [
    {
        "name": "RequirementSpecificationCommand",
        "type": "Command",
        "description": "Description of RequirementSpecificationCommand",
    },
    {
        "name": "ModelGeneratedEvent",
        "type": "Event",
        "description": "Description of ModelGeneratedEvent",
    },
    # Add more messages as needed
]

# Load and render the template
template_string = '''# actor_template.jinja

class {{ actor_name }}(Actor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        # Additional initialization here if necessary

    {% for event in messages %}
    async def handle_{{ event.name|lower }}(self, event: {{ event.type }}):
        """
        Handle {{ event.name }} event.
        {% if event.description %}# {{ event.description }}{% endif %}
        """
        # Logic to handle {{ event.name }} event
        pass
    {% endfor %}
'''  # The string content of the actor_template.jinja
template = Template(template_string)
rendered_actor_class = template.render(actor_name=actor_name, messages=messages)

# Output the rendered actor class
print(rendered_actor_class)
