from typetemp.template.typed_template import TypedTemplate

from typetemp.template.render_funcs import render_str
import dspy

from rdddy.messages import EventStormModel

base_class_mapping = {
    "domain_event_classnames": "Event",
    "external_event_classnames": "Event",
    "command_classnames": "Command",
    "query_classnames": "Query",
    "aggregate_classnames": "AbstractAggregate",
    "policy_classnames": "AbstractPolicy",
    "read_model_classnames": "AbstractReadModel",
    "view_classnames": "AbstractView",
    "ui_event_classnames": "Event",
    "saga_classnames": "AbstractSaga",
    "integration_event_classnames": "Event",
    "exception_classnames": "DomainException",
    "value_object_classnames": "AbstractValueObject",
    "task_classnames": "AbstractTask",
}


class GenRDDDYClassTemplate(TypedTemplate):
    source = """from rdddy.{{ base_class_name | underscore }} import {{ base_class_name }}


class {{ classname }}({{ base_class_name }}):
    \"\"\"
    {{ docstring }}
    \"\"\" 
    pass
    
"""
    to = "{{ base_class_name | underscore }}/{{ classname | underscore }}.py"


class GenerateVerboseDescription(dspy.Signature):
    """Generate a docstring for a class in a reactive ddd system."""
    role = dspy.InputField(desc="The role of the class.")
    classname = dspy.InputField(desc="The name of the class.")
    description = dspy.OutputField(desc="Focused description of the class.")


class VerboseDescriptionGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_description = dspy.ChainOfThought(GenerateVerboseDescription)

    def forward(self, role, classname):
        prediction = self.generate_description(role=role, classname=classname)
        return prediction.description


def generate_verbose_class_definitions(model: EventStormModel, description_generator: VerboseDescriptionGenerator):

    for attr, base_class_name in base_class_mapping.items():
        role = attr.replace('_classnames', '')  # Simplified role name, adjust as needed
        classnames = getattr(model, attr, [])
        for classname in classnames:
            # Generate a verbose description for each class, customizing as needed
            description = description_generator(role=role, classname=classname)

            tmpl = GenRDDDYClassTemplate(base_class_name=base_class_name, classname=classname, docstring=description)()
            # print(f"{classname} written to disk.")


def main():
    event_storm_model_data = {
        "domain_event_classnames": ["OrderPlaced", "PaymentProcessed", "InventoryUpdated"],
        "external_event_classnames": ["ExternalPaymentConfirmation", "SupplierInventoryUpdate", "SupplierInventoryConfirmation"],
        "command_classnames": ["PlaceOrder", "ProcessPayment", "UpdateInventory"],
        "query_classnames": ["GetOrderDetails", "ListBooks", "CheckOrderStatus"],
        "aggregate_classnames": ["OrderAggregate", "BookAggregate", "CustomerAggregate"],
        "policy_classnames": ["OrderCancellationPolicy", "RefundPolicy", "ShippingPolicy"],
        "read_model_classnames": ["OrderSummaryReadModel", "BookCatalogReadModel", "CustomerOrderHistoryReadModel"],
        "view_classnames": ["OrderDetailsView", "BookListView", "CustomerProfileView"],
        "ui_event_classnames": ["AddToCartButtonClick", "CheckoutFormSubmitted", "OrderHistoryPageLoaded"],
        "saga_classnames": ["OrderFulfillmentSaga", "PaymentProcessingSaga", "BookRestockSaga"],
        "integration_event_classnames": ["OrderPlacedIntegrationEvent", "PaymentProcessedIntegrationEvent",
                                         "InventoryUpdatedIntegrationEvent"],
        "exception_classnames": ["OrderNotFoundException", "PaymentDeclinedException", "BookOutOfStockException"],
        "value_object_classnames": ["Address", "Price", "Quantity"],
        "task_classnames": ["ValidateOrder", "CalculateShippingCosts", "SendOrderConfirmationEmail"],
    }

    event_storm_model = EventStormModel.model_validate(event_storm_model_data)

    # generate_class_definitions(event_storm_model)


    lm = dspy.OpenAI(max_tokens=3000)
    # lm = dspy.OpenAI(max_tokens=4500, model="gpt-4")
    dspy.settings.configure(lm=lm)

    description_generator = VerboseDescriptionGenerator()
    generate_verbose_class_definitions(event_storm_model, description_generator)


if __name__ == '__main__':
    main()
