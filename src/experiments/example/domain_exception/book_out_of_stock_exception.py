from rdddy.domain_exception import DomainException


class BookOutOfStockException(DomainException):
    """
    This class represents an exception that is thrown when a book is out of stock in a reactive ddd system. It is used to handle situations where a user tries to purchase a book that is currently unavailable. This class is responsible for notifying the user and providing information on when the book will be back in stock. It also contains relevant information such as the book title and author to help the user make an informed decision. This class plays a crucial role in maintaining the integrity of the system and ensuring a smooth user experience.
    """

    pass
