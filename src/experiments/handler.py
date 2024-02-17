import inspect

from denz.actor import Actor


class Message:
    def __init__(self, message):
        self.message = message

class Command(Message):
    pass

class Event(Message):
    pass

class Query(Message):
    pass


class Aggregate(Actor):
    handlers = {}

    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)



    async def receive(self, message):
        handler = self.handlers.get(type(message))
        if handler:
            await handler(message)

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

class OrderService(Aggregate):
    def __init__(self):
        super().__init__()
        self.orders = {}
        self.products = {}

    def create_order(self, order_id, customer_name):
        order = {'order_id': order_id, 'customer_name': customer_name, 'items': []}
        self.orders[order_id] = order
        return order

    def order_created(self, message):
        order_id = message.data['order_id']
        customer_name = message.data['customer_name']
        return Event(f'Order created for {customer_name} with ID {order_id}.')


    def add_product(self, order_id, product_id, quantity):
        order = self.orders.get(order_id)
        if order:
            product = self.products.get(product_id)
            if product:
                order['items'].append({'product_id': product_id, 'quantity': quantity})
                return Event(f"Added {quantity} {product.name}(s) to the order.")
            else:
                return Event("Product not found.")
        else:
            return Event("Order not found.")

    def get_order_total(self, order_id):
        order = self.orders.get(order_id)
        if order:
            total = 0
            for item in order['items']:
                product = self.products.get(item['product_id'])
                if product:
                    total += product.price * item['quantity']
            return Query(f'Total for order {order_id}: ${total}')
        else:
            return Query('Order not found.')

class DeliveryService(Aggregate):
    def __init__(self):
        super().__init__()
        self.deliveries = {}
        self.orders = {}

    def schedule_delivery(self, order_id, delivery_date):
        order = self.orders.get(order_id)
        if order:
            self.deliveries[order_id] = {'order_id': order_id, 'delivery_date': delivery_date}
            return Event(f'Scheduled delivery for order {order_id} on {delivery_date}.')
        else:
            return Event('Order not found.')


# Initialize services
order_service =
delivery_service = DeliveryService()


# Usage example
product1 = Product(1, 'Widget', 10.0)
product2 = Product(2, 'Gadget', 20.0)

order = order_service.create_order(1, 'John Doe')
order_service.products[1] = product1
order_service.products[2] = product2

order_service.add_product(1, 1, 3)  # Add 3 Widgets to the order
order_service.add_product(1, 2, 2)  # Add 2 Gadgets to the order

query_result = order_service.get_order_total(1)
print(query_result.message)

delivery_result = delivery_service.schedule_delivery(1, '2023-12-31')
print(delivery_result.message)

import anyio

async def main():
    # Create an ActorSystem
    actor_system = ActorSystem()

    # Create an Order actor
    order_actor = actor_system.actor_of(Order, order_id="123", customer_id="456")

    # Simulate order processing
    await order_actor.create_order()
    await asyncio.sleep(1)
    await order_actor.add_item(product_id="P1", quantity=2, unit_price=10.0)
    await asyncio.sleep(1)
    await order_actor.cancel_order()


if __name__ == '__main__':
    anyio.run(main)