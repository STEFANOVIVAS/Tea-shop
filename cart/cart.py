from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """Inicaliza o carrinho de compras"""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = request.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """ Adiciona um produto no carrinho de compras ou atualiza a sua quantidade"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            product_id[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """marca a sessão como modificada para garantir que ela seja salva"""
        self.session.modified = True

    def remove(self, product):
        """remove um produto do carrinho de compras"""

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Itera pelos itens do carrinho e obtem os produtos do banco de dados"""
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Contabiliza todos os itens que estão no carrinho"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Contabiliza o valor total da compra"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
