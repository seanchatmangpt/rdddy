from rdddy.domain_exception import DomainException


class OrderNotFoundException(DomainException):
    """
    The OrderNotFoundException class is used to represent an exception that occurs when an order cannot be found in the system. This class is typically used in a reactive ddd system to handle errors related to retrieving or processing orders. It contains information about the specific order that could not be found, such as its ID or other identifying details. This class is important for maintaining the integrity of the system and ensuring that errors are handled appropriately.
    """

    pass
