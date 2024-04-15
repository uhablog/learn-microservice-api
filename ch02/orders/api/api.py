from datetime import datetime
from uuid import UUID

from starlette.response import Response
from starlette import status

from orders.app import app

# レスポンスで返す注文オブジェクトを定義
orders = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': 'deliverd',
    'created': datetime.now(),
    'order': [
        {
            'product': 'cappucino',
            'size': 'medium',
            'quantity': 1
        }
    ]
}