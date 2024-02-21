from rdddy.event import Event


class SupplierInventoryUpdate(Event):
    """
    This class represents an external event that is triggered when the inventory of a supplier needs to be updated in a reactive DDD system. It contains information about the supplier and the updated inventory, and is responsible for notifying the system to update its records accordingly. This class plays a crucial role in maintaining the consistency of data in the system and ensuring that all relevant entities are updated in a timely manner.
    """ 
    pass
    