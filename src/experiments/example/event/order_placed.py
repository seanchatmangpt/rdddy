from rdddy.event import Event


class OrderPlaced(Event):
    """
    This class represents a domain event that is triggered when a new order is placed in the system. It contains information about the order, such as the order ID, customer information, and items ordered. This event is used to notify other parts of the system that a new order has been placed and may trigger further actions or processes. It is an important part of the reactive DDD system as it allows for real-time updates and reactions to changes in the domain.
    """

    pass
