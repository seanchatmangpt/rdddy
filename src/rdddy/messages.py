import inspect
from typing import Type, TypeVar, Any
from importlib import import_module
from utils.yaml_tools import YAMLMixin

from pydantic import BaseModel, Field


class Message(YAMLMixin, BaseModel):
    """
    Message class using Pydantic for data validation and serialization.
    """

    actor_id: int = -1
    content: Any = None
    message_type: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        # Calculate the relative import path at runtime
        self.message_type = self._calculate_import_path()

    def _calculate_import_path(self) -> str:
        """
        Calculate the relative import path of the class.
        """
        module = inspect.getmodule(self)
        relative_path = f"{module.__name__}.{self.__class__.__name__}"
        return relative_path

    class Config:
        allow_extra = True
        arbitrary_types_allowed = True


class Command(Message):
    """
    Command message type.
    """

    pass


class Event(Message):
    """
    Event message type.
    """

    pass


class Query(Message):
    """
    Query message type.
    """

    pass


from pydantic import BaseModel, Field


class EventStormModel(BaseModel):
    """
    Integrates Event Storming with RDDD and DFLSS to capture and analyze domain complexities through events, commands,
    and queries, using Hoare logic for correctness. It serves as a repository for interactions identified in
    Event Storming, enhancing system responsiveness and process efficiency. This model educates on designing and
    verifying systems aligned with domain requirements and operational excellence. CamelCase only.
    """

    domain_event_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of domain event names triggering system reactions. Examples: 'OrderPlaced', 'PaymentProcessed', 'InventoryUpdated'.",
    )
    external_event_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of external event names that originate from outside the system but affect its behavior. Examples: 'WeatherChanged', 'ExternalSystemUpdated', 'RegulationAmended'.",
    )
    command_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of command names driving state transitions. Examples: 'CreateOrder', 'ProcessPayment', 'UpdateInventory'.",
    )
    query_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of query names for information retrieval without altering the system state. Examples: 'GetOrderDetails', 'ListAvailableProducts', 'CheckCustomerCredit'.",
    )
    aggregate_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of aggregate names, clusters of domain objects treated as a single unit. Examples: 'OrderAggregate', 'CustomerAggregate', 'ProductAggregate'.",
    )
    policy_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of policy names governing system behavior. Examples: 'OrderFulfillmentPolicy', 'ReturnPolicy', 'DiscountPolicy'.",
    )
    read_model_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of read model names optimized for querying. Examples: 'OrderSummaryReadModel', 'ProductCatalogReadModel', 'CustomerProfileReadModel'.",
    )
    view_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of view names representing user interface components. Examples: 'OrderDetailsView', 'ProductListView', 'CustomerDashboardView'.",
    )
    ui_event_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of UI event names triggered by user interactions. Examples: 'ButtonClick', 'FormSubmitted', 'PageLoaded'.",
    )
    saga_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of saga names representing long-running processes. Examples: 'OrderProcessingSaga', 'CustomerOnboardingSaga', 'InventoryRestockSaga'.",
    )
    integration_event_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of integration event names exchanged between different parts of a distributed system. Examples: 'OrderCreatedIntegrationEvent', 'PaymentConfirmedIntegrationEvent', 'InventoryCheckIntegrationEvent'.",
    )
    exception_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of exception names representing error conditions. Examples: 'OrderNotFoundException', 'PaymentFailedException', 'InventoryShortageException'.",
    )
    value_object_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of immutable value object names within the domain model. Examples: 'AddressValueObject', 'MoneyValueObject', 'QuantityValueObject'.",
    )
    task_names: list[str] = Field(
        ...,
        min_items=3,
        description="List of task names needed to complete a process or workflow. Examples: 'ValidateOrderTask', 'AllocateInventoryTask', 'NotifyCustomerTask'.",
    )

    class Config:
        arbitrary_types_allowed = True



class MessageList(YAMLMixin, BaseModel):
    messages: list[Message]


class ExceptionMessage(Message):
    """Generic exception message"""


class TerminationMessage(Message):
    """Message indicating an actor should be terminated."""


T = TypeVar("T", bound="Message")


class MessageFactory:
    """
    Factory class to convert YAML data into appropriate Message types.
    """

    @classmethod
    def create_message(cls, data: dict) -> T:
        """
        Create a message of the appropriate type based on the data provided.

        Parameters:
        - data (dict): A dictionary containing the message data.

        Returns:
        - Type[BaseModel]: The appropriate message type.
        """
        message_class = cls._get_message_class(data["message_type"])
        return message_class(**data)

    @classmethod
    def create_messages_from_list(cls, data_list: list[dict]) -> list[T]:
        """
        Create a list of messages from a list of YAML data dictionaries.

        Parameters:
        - data_list (List[dict]): A list of dictionaries containing message data.

        Returns:
        - List[Type[BaseModel]]: A list of appropriate message types.
        """
        messages = [cls.create_message(data) for data in data_list]
        return messages

    @classmethod
    def _get_message_class(cls, module_name: str) -> Type[T]:
        """
        Get the message class corresponding to the module name. Import the module if not already imported.

        Parameters:
        - module_name (str): The module name containing the message class.

        Returns:
        - Type[BaseModel]: The message class.
        """
        # module_name = 'livingcharter.domain.collaboration_context.AgentCreated'
        # slice off the last period
        module_path, class_name = module_name.rsplit(".", 1)

        # Assuming that the message class is named the same as the last part of the module name
        module = import_module(module_path)
        message_class = getattr(module, class_name)

        return message_class
