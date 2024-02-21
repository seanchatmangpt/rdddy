from rdddy.domain_exception import DomainException


class PaymentDeclinedException(DomainException):
    """
    This class represents an exception that is thrown when a payment is declined in a reactive DDD system. It is responsible for handling errors related to payment processing and notifying the system of a declined payment. This class is necessary in a reactive DDD system because it allows for proper handling of payment failures and ensures that the system can react and respond accordingly.
    """ 
    pass
    