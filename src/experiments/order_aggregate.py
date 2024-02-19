import asyncio
import logging

from experiments.abstract_aggregate import AbstractAggregate
from rdddy.actor_system import ActorSystem
from rdddy.messages import AbstractEvent

# Define the AggregateMixin and Actor classes (as provided in the previous code)

logger = logging.getLogger(__name__)


class OrderCreated(AbstractEvent):
    def __init__(self, order_id, customer_id, total_amount):
        super().__init__()
        self.order_id = order_id
        self.customer_id = customer_id
        self.total_amount = total_amount


class OrderItemAdded(AbstractEvent):
    def __init__(self, order_id, product_id, quantity, unit_price):
        super().__init__()
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price


class OrderCancelled(AbstractEvent):
    def __init__(self, order_id):
        super().__init__()
        self.order_id = order_id


class OrderStatus:
    CREATED = "Created"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"


class Order(AbstractAggregate):
    def __init__(self, actor_system, order_id, customer_id):
        super().__init__(actor_system)
        self.order_id = order_id
        self.customer_id = customer_id
        self.status = OrderStatus.CREATED
        self.items = []
        self.total_amount = 0.0

    async def create_order(self):
        # Validate and process order creation
        if self.status != OrderStatus.CREATED:
            await self.handle_error("Order is not in a valid state for creation.")
            return
        self.status = OrderStatus.PROCESSING
        event = OrderCreated(self.order_id, self.customer_id, self.total_amount)
        await self.emit_event(event)

    async def add_item(self, product_id, quantity, unit_price):
        # Validate and process item addition
        if self.status != OrderStatus.PROCESSING:
            await self.handle_error("Cannot add items to a non-processing order.")
            return
        event = OrderItemAdded(self.order_id, product_id, quantity, unit_price)
        await self.emit_event(event)

    async def cancel_order(self):
        # Validate and process order cancellation
        if self.status != OrderStatus.PROCESSING:
            await self.handle_error("Cannot cancel a non-processing order.")
            return
        self.status = OrderStatus.CANCELLED
        event = OrderCancelled(self.order_id)
        await self.emit_event(event)

    def apply_event(self, event):
        # Apply events to update the order's state
        if isinstance(event, OrderCreated):
            self.customer_id = event.customer_id
        elif isinstance(event, OrderItemAdded):
            self.items.append(
                {
                    "product_id": event.product_id,
                    "quantity": event.quantity,
                    "unit_price": event.unit_price,
                }
            )
            self.total_amount += event.quantity * event.unit_price
        elif isinstance(event, OrderCancelled):
            self.status = OrderStatus.CANCELLED

    def handle_order_cancelled(self, event: OrderCancelled):
        print("Order Cancelled", event)


import anyio


async def main():
    # Create an ActorSystem
    actor_system = ActorSystem()

    # Create an Order actor
    order_actor = await actor_system.actor_of(Order, order_id="123", customer_id="456")

    # Simulate order processing
    await order_actor.create_order()
    await asyncio.sleep(1)
    await order_actor.add_item(product_id="P1", quantity=2, unit_price=10.0)
    await asyncio.sleep(1)
    await order_actor.cancel_order()


if __name__ == "__main__":
    anyio.run(main)
