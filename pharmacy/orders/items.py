from .models import Order
from medicine.models import Product


class Items:
	def __init__(self):
		self.items = {}

	def __iter__(self):
		product_ids = self.items.keys()
		products = Product.objects.filter(id__in=product_ids)
		items = self.items.copy()
		for product in products:
			items[str(product.id)]['product'] = product

		for item in items.values():
			item['total_price'] = int(item['price']) * item['quantity']
			yield item

	def add(self, product, quantity):
		product_id = str(product.id)

		if product_id not in self.items:
			self.items[product_id] = {'quantity':0, 'price':str(product.price)}
		self.items[product_id]['quantity'] += quantity

	def get_total_price(self):
		return sum(int(item['price']) * item['quantity'] for item in self.items.values())


