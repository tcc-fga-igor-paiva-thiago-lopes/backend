from .truck_driver import TruckDriver
from .category import Category
from .freight import Freight
from .account import Account

table_to_model = {
    "FREIGHT": Freight,
    "CATEGORY": Category,
    "ACCOUNT": Account,
    "TRUCK_DRIVER": TruckDriver,
}
