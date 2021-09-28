from flask import Flask
from .controller.Orders import orders_bp
from .controller.Products import products_bp
from .controller.Customers import customers_bp

api = Flask(__name__)
api.register_blueprint(customers_bp, url_prefix='/customers')
api.register_blueprint(orders_bp, url_prefix='/orders')
api.register_blueprint(products_bp, url_prefix='/products')


class API:

    def run(self):
        api.debug = False
        api.run()
