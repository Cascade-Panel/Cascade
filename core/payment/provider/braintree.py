

import aio_braintree

class BraintreeProvider:
    def __init__(self, enviroment, merchant_id, public_key, private_key):
        self.client = aio_braintree.BraintreeClient(
            environment=enviroment,
            merchant_id=merchant_id,
            public_key=public_key,
            private_key=private_key
        )

    async def gen_invoice(self, amount, currency, order_id, description):
        result = await self.client.transaction.sale({
            'amount': amount,
            'currency_iso_code': currency,
            'order_id': order_id,
            'description': description,
            'payment_method_nonce': 'fake-valid-nonce',
            'options': {
                'submit_for_settlement': True
            }
        })
        return result

    async def check_payment(self, order_id):
        transaction = await self.client.transaction.find(order_id)
        return transaction.status

    async def refund_payment(self, transaction_id, amount):
        result = await self.client.transaction.refund(transaction_id, amount)
        return result

    async def get_transaction_status(self, transaction_id):
        transaction = await self.client.transaction.find(transaction_id)
        return transaction.status

    async def list_invoices(self):
        # Braintree does not support direct invoice management, implement as needed
        raise NotImplementedError

    async def cancel_invoice(self, invoice_id):
        # Braintree does not support direct invoice cancellation, implement as needed
        raise NotImplementedError
