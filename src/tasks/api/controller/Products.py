from flask import Blueprint
from ..datamapper import DataMapper
from ..model.Products import Products as ProductsModel

products_bp = Blueprint('products_bp', __name__)


@products_bp.route('/top_selling/<int:num_items>', methods=['GET'])
def top_selling(num_items):
    items = ProductsModel(DataMapper()).top_selling(num_items)
    top = {}
    for (product_id, total_value) in items:
        top[product_id] = float(total_value)
    return top
