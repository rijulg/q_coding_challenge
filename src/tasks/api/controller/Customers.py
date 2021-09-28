from flask import Blueprint
from ..datamapper import DataMapper
from ..model.Customers import Customers as CustomersModel

customers_bp = Blueprint('customers_bp', __name__)


@customers_bp.route('/count_recent/<int:num_days>', methods=['GET'])
def count_recent(num_days):
    count = CustomersModel(DataMapper()).count_recent(num_days)
    return {"count": count}
