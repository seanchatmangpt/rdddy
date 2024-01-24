# This script demonstrates how to create a LinkML (Link Modeling Language) version of the BBO ontology
# described in the paper "BBO: BPMN 2.0 Based Ontology for Business Process Representation".
# LinkML is used for defining and generating schemas for structured data.

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.linkml_model import (
    SchemaDefinition,
    ClassDefinition,
    SlotDefinition,
    EnumDefinition,
)

# Initialize the SchemaDefinition
bbo_schema = SchemaDefinition(
    id="https://github.com/AminaANNANE/BBO_BPMNbasedOntology",
    name="BBO",
    description="BPMN 2.0 Based Ontology for Business Process Representation",
    version="1.0",
)

# Define Classes based on the ontology
bbo_schema.classes = {
    "Process": ClassDefinition(
        name="Process", description="A class representing a process"
    ),
    "Activity": ClassDefinition(
        name="Activity", description="A class representing an activity"
    ),
    "Task": ClassDefinition(name="Task", description="A class representing a task"),
    "Event": ClassDefinition(name="Event", description="A class representing an event"),
    "Gateway": ClassDefinition(
        name="Gateway", description="A class representing a gateway"
    ),
    "SequenceFlow": ClassDefinition(
        name="SequenceFlow", description="A class representing a sequence flow"
    ),
    "Resource": ClassDefinition(
        name="Resource", description="A class representing a resource"
    ),
    "ManufacturingFacility": ClassDefinition(
        name="ManufacturingFacility",
        description="A class representing a manufacturing facility",
    ),
    "WorkProduct": ClassDefinition(
        name="WorkProduct", description="A class representing a work product"
    ),
    "Agent": ClassDefinition(name="Agent", description="A class representing an agent"),
}

# Define Slots (properties/relationships)
bbo_schema.slots = {
    "has_activity": SlotDefinition(name="has_activity", range="Activity"),
    "has_task": SlotDefinition(name="has_task", range="Task"),
    "has_event": SlotDefinition(name="has_event", range="Event"),
    "has_gateway": SlotDefinition(name="has_gateway", range="Gateway"),
    "has_sequence_flow": SlotDefinition(name="has_sequence_flow", range="SequenceFlow"),
    "requires_resource": SlotDefinition(name="requires_resource", range="Resource"),
    "located_at": SlotDefinition(name="located_at", range="ManufacturingFacility"),
    "produces_work_product": SlotDefinition(
        name="produces_work_product", range="WorkProduct"
    ),
    "performed_by": SlotDefinition(name="performed_by", range="Agent"),
}

# Define Enums if necessary
# Example Enum Definition
bbo_schema.enums = {
    "ResourceType": EnumDefinition(
        name="ResourceType",
        permissible_values={
            "MaterialResource": {},
            "SoftwareResource": {},
            "HumanResource": {},
        },
    )
}

# Create the schema view
schema_view = SchemaView(bbo_schema)

# Generate the YAML representation of the schema
bbo_yaml = yaml_dumper.dumps(bbo_schema)

# Write the YAML to a file
with open("bbo_ontology.yaml", "w") as file:
    file.write(bbo_yaml)

print("BBO ontology schema has been successfully generated in YAML format.")
