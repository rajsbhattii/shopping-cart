class Product:
    def __init__(self, name, price, category):
        # Initialize product attributes
        self._name = name
        self._price = price
        self._category = category

    # Define how products are classified
    def __eq__(self, other):
        if isinstance(other, Product):
            if (self._name == other._name and self._price == other._price and self._category == other._category):
                return True
            else:
                return False

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        productInfo = 'Product(' + self._name + ',' + str(self._price) + ',' + self._category + ')'
        return productInfo


class Inventory:
    def __init__(self):
        self.inventory = {}

    def add_to_productInventory(self, productName, productPrice, productQuantity):
        self.inventory[productName] = {'price': productPrice, 'quantity': productQuantity}

    def add_productQuantity(self, nameProduct, addQuantity):
        if nameProduct in self.inventory:
            self.inventory[nameProduct]['quantity'] += addQuantity
        else:
            print(f"{nameProduct} not found in inventory.")

    def remove_productQuantity(self, nameProduct, removeQuantity):
        if nameProduct in self.inventory:
            if self.inventory[nameProduct]['quantity'] >= removeQuantity:
                self.inventory[nameProduct]['quantity'] -= removeQuantity
            else:
                print(f"Insufficient quantity of {nameProduct} in inventory.")
        else:
            print(f"{nameProduct} not found in inventory.")

    def get_productPrice(self, nameProduct):
        return self.inventory[nameProduct]['price']

    def get_productQuantity(self, nameProduct):
        if nameProduct in self.inventory:
            return self.inventory[nameProduct]['quantity']

    def display_Inventory(self):
        for product, details in self.inventory.items():
            print(f"{product}, {details['price']}, {details['quantity']}")


class ShoppingCart:
    def __init__(self, buyerName, inventory):
        self.buyerName = buyerName
        self.cart = {}
        self.inventory = inventory

    def add_to_cart(self, nameProduct, requestedQuantity):

        available_quantity = self.inventory.get_productQuantity(nameProduct)

        if requestedQuantity > available_quantity:
            return "Can not fill the order"
        else:
            self.inventory.remove_productQuantity(nameProduct, requestedQuantity)
            if nameProduct in self.cart:
                self.cart[nameProduct] += requestedQuantity
            else:
                self.cart[nameProduct] = requestedQuantity
            return "Filled the order"

    def remove_from_cart(self, nameProduct, requestedQuantity):
        if nameProduct in self.cart:
            if self.cart[nameProduct] >= requestedQuantity:
                self.cart[nameProduct] -= requestedQuantity
                self.inventory.add_productQuantity(nameProduct, requestedQuantity)
                return "Successful"
            else:
                return "The requested quantity to be removed from cart exceeds what is in the cart"
        else:
            return "Product not in the cart"

    def view_cart(self):
        #print(self.cart.items())
        for product, quantity in self.cart.items():
            print(f"{product} {quantity}")
        total = sum(self.inventory.get_productPrice(product) * quantity for product, quantity in self.cart.items())
        print(f"Total: {total}")
        print(f"Buyer Name: {self.buyerName}")


class ProductCatalog:
    def __init__(self):
        self.product_list = []  # Initializing an empty list to store products
        self.low_prices = set()
        self.medium_prices = set()
        self.high_prices = set()

    def addProduct(self, product):
        if isinstance(product, Product):
            self.product_list.append(product)
            price = product.get_price()
            if price >= 0 and price <= 99:
                self.low_prices.add(product.get_name())
            elif price >= 100 and price <= 499:
                self.medium_prices.add(product.get_name())
            else:
                self.high_prices.add(product.get_name())

    def price_category(self):
        num_low_price = len(self.low_prices)
        num_medium_price = len(self.medium_prices)
        num_high_price = len(self.high_prices)
        print(f"Number of low price items: {num_low_price}")
        print(f"Number of medium price items: {num_medium_price}")
        print(f"Number of high price items: {num_high_price}")

    def display_catalog(self):
        for product in self.product_list:
            print(f"Product: {product.get_name()} Price: {product.get_price()} Category: {product.get_category()}")


def populate_inventory(filename):
    inventory = Inventory()  # Instantiate Inventory object
    openInven = open(filename, 'r')
    for line in openInven:
        data = line.strip().split(',')
        if len(data) == 4:  # Ensure all fields are present
            name, price, quantity, category = data
            price = int(price)
            quantity = int(quantity)
            inventory.add_to_productInventory(name, price, quantity)
    return inventory


def populate_catalog(filename):
    openInven = open(filename, 'r')
    product_catalog = ProductCatalog()
    for line in openInven:
        data = line.strip().split(',')
        if len(data) == 4:  # Ensure all fields are present
            name, price, quantity, category = data
            price = int(price)
            quantity = int(quantity)
            product = Product(name, price, category)
            product_catalog.addProduct(product)
    return product_catalog