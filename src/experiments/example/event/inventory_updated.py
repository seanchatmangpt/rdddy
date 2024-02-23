from rdddy.event import Event


class InventoryUpdated(Event):
    """
    The InventoryUpdated class is responsible for representing an event that indicates a change in the inventory of a product. It contains information such as the product ID, the quantity before and after the update, and the timestamp of the event. This class is used to notify other parts of the system about changes in the inventory, allowing them to react accordingly. It is an essential part of a reactive DDD system as it enables communication and synchronization between different components.
    """

    pass
