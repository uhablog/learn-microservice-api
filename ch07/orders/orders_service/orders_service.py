from orders.orders_service.exceptions import OrderNotFoundError

class OrdersService:
    def __init__(self, orders_repository):
        self.orders_repository = orders_repository

    def place_order(self, item):
        # データベースレコードを作成して注文を実行
        return self.orders_repository.add(items)

    def get_order(self, order_id):
        # 注文リポジトリにリクエストされたIDを私て注文の詳細を取得
        order = self.orders_repository.get(order_id)

        # 注文が存在しない場合はOrderNotFoundError例外を生成
        if order is not None:
            return order

        raise OrderNotFoundError(f'Order with id {order_id} is not found')

    def update_order(self,order_id, items):
        order = self.orders_repository.get(order_id)

        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')

        return self.orders_repository.update(order_id, {'items': items})

    def list_order(self, **filters):
        limit = filters.pop('limit', None)
        return self.orders_repository.list(limit, **filters)

    def pay_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')

        order.pay()
        schedule_id = order.schedule()

        return self.orders_repository.update(
            order_id, status='progress', schedule_id=schedule_id
        )

    def cancel_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')

        order.cancel()
        return self.orders_repository.update(order_id, status='cancelled')

