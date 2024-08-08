""" A module for handling payment providers """

class Payeer:
    def __init__(self, provider):
        self.provider = provider
    
    async def gen_invoice(self, amount, currency, order_id, description):
        return await self.provider.gen_invoice(amount, currency, order_id, description)
    
    async def check_payment(self, order_id):
        return await self.provider.check_payment(order_id)

    async def refund_payment(self, transaction_id, amount):
        return await self.provider.refund_payment(transaction_id, amount)

    async def get_transaction_status(self, transaction_id):
        return await self.provider.get_transaction_status(transaction_id)

    async def list_invoices(self):
        return await self.provider.list_invoices()

    async def cancel_invoice(self, invoice_id):
        return await self.provider.cancel_invoice(invoice_id)