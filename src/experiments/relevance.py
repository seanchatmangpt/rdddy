from jinja2 import Environment

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from rdddy.messages import *

# Jinja template as a string

from pydantic import BaseModel, Field


class RelevantDDDToGherkinModel(BaseModel):
    """
    The specific DDD elements that should be considered when implementing the features.
    """
    domain_event_classnames: list[str] = Field(
        default=[],
        description="Domain events directly implicated by Gherkin scenarios. Include only if they trigger reactions relevant to the described features."
    )
    external_event_classnames: list[str] = Field(
        default=[],
        description="External events from outside the system that are relevant to the Gherkin scenarios. Include those that significantly impact system behavior as described."
    )
    ui_event_classnames: list[str] = Field(
        default=[],
        description="UI event names triggered by user interactions that play a significant role in the Gherkin scenarios."
    )


prompt = """
        "domain_event_classnames": ["OrderPlaced", "PaymentProcessed", "InventoryUpdated"],
        "external_event_classnames": ["ExternalPaymentConfirmation", "SupplierInventoryUpdate", "SupplierInventoryConfirmation"],
        "ui_event_classnames": ["AddToCartButtonClick", "CheckoutFormSubmitted", "OrderHistoryPageLoaded"],

Given the user is logged into the system
And the user has items in their shopping cart
But one of the items is out of stock
When the user proceeds to checkout
Then the order is not placed
And the user is informed about the out-of-stock item
    
Only return relevant classnames to the gherkin above
Explain your answer for each classname
"""


from typing import List, Optional
from pydantic import BaseModel, Field

from typing import List


class Step(BaseModel):
    step_type: str  # "Given", "When", "Then", "And", "But"
    description: str

    def __str__(self):
        return f"{self.step_type} {self.description}"


class Scenario(BaseModel):
    name: str
    steps: List[Step]

    def __str__(self):
        steps_str = "\n    ".join(str(step) for step in self.steps)
        return f"Scenario: {self.name}\n    {steps_str}"


class Feature(BaseModel):
    title: str
    description: str
    scenarios: List[Scenario]

    def __str__(self):
        scenarios_str = "\n  ".join(str(scenario) for scenario in self.scenarios)
        return f"Feature: {self.title}\n  {self.description}\n  {scenarios_str}"


def main():
    import dspy
    from rdddy.messages import (
        EventStormingDomainSpecificationModel,
    )

    # lm = dspy.OpenAI(max_tokens=3000)
    lm = dspy.OpenAI(max_tokens=4500, model="gpt-4")
    dspy.settings.configure(lm=lm)
    # Create a Jinja environment and render the template
    env = Environment()

    print("Generating Gherkin")

    gh_model = GenPydanticInstance(root_model=RelevantDDDToGherkinModel)(prompt=prompt)
    print(gh_model)

    # print(f"RelevantDDDToGherkinModel {event_storm_model}")

    # gherkin = GenPydanticInstance(root_model=Feature, child_models=[Scenario, Step])(prompt=prompt2)

    # print(str(gherkin))

    # print(f'prompt:\n{lm.history[0].get("prompt")}')
    # print(f'response:\n{lm.history[0]["response"].choices[0]["text"]}')

    # template = env.from_string(template_str)
    # rendered_classes = template.render(
    #     events=event_storm_model.events,
    #     commands=event_storm_model.commands,
    #     queries=event_storm_model.queries,
    # )
    #
    # # Output the rendered classes
    # print(rendered_classes)
    #
    # with open("rag_gen_messages.py", "w") as f:
    #     f.write(rendered_classes)


if __name__ == "__main__":
    main()
