import uuid

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import status, HTTPException
from starlette.responses import Response
# from starlette import status

from orders.app import app
from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema
)

# レスポンスで返す注文オブジェクトを定義
ORDERS = []

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):

    # いずれのパラメータも指定されていない場合は、そのまま結果を返却
    if cancelled is None and limit is None:
        return {'orders': ORDERS}
    
    # どちらかのパラメータが設定されている場合は、リストを絞り込む
    query_set = [order for order in ORDERS]

    if cancelled is not None:
        if cancelled:
            query_set = [
                order
                for order in query_set
                if order['status'] == 'cancelled'
            ]
        else:
            query_set = [
                order
                for order in query_set
                if order['status'] != 'cancelled'
            ]
    
    if limit is not None and len(query_set) > limit:
        return {'orders': query_set[:limit]}
    
    return {'orders': query_set}

@app.post('/orders',
          status_code=status.HTTP_201_CREATED,
          response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):

    # 注文データに必要な情報を付け加えて、リストに追加
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.now()
    order['status'] = 'created'
    ORDERS.append(order)
    return order

@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):

    # 注文リストからIDで検索して、返却する
    for order in ORDERS:
        if order['id'] == order_id:
            return order
    
    # 注文が見つからない場合は404を返す
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} is not found'
    )

@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):

    # IDが同じ注文情報を更新して、返却
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
    
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} is not found'
    )

@app.delete('/orders/{order_id}', 
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response)
def delete_order(order_id: UUID):

    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=204)
    
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} is not found'
    )

@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} is not found'
    )

@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} is not found'
    )
