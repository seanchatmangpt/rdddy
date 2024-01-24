from jinja2 import Template

# Define the actor name and a list of events
actor_name = "MyActor"
events = [
    {
        "name": "EventOne",
        "type": "EventOneType",
        "description": "Description of Event One",
    },
    {
        "name": "EventTwo",
        "type": "EventTwoType",
        "description": "Description of Event Two",
    },
    # Add more events as needed
]

# Load and render the template
template_string = '''# actor_template.jinja

class {{ actor_name }}(Actor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        # Additional initialization here if necessary

    {% for event in events %}
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
rendered_actor_class = template.render(actor_name=actor_name, events=events)

# Output the rendered actor class
print(rendered_actor_class)
