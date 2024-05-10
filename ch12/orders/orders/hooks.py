import json
import dredd_hooks

response_stash = {}

@dredd_hooks.after('/orders > Creates an order > 201 > application/json')
def save_created_order(transaction):
    response_payload = transaction['real']['body']
    order_id = json.loads(response_payload)['id']
    response_stash['created_order_id'] = order_id
