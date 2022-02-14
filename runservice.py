import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import click
from flask_migrate import Migrate
from app import create_app, db
from app.models.user import User
from app.models.order import Order
from app.models.burger import Burger
from app.models.restaurant import Restaurant
from app.models.order_detail import OrderDetail

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Restaurant=Restaurant, Order=Order, OrderDetail=OrderDetail, Burger=Burger)


@app.cli.command()
def initialvalues():
    from app.models.user import User
    from app.models.restaurant import Restaurant
    from app.models.burger import Burger
    User.insert_user()
    Restaurant.insert_restaurant()
    Burger.insert_burger()
    return 1


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run unit test """
    import unittest

    if test_names:
        """
        flask test tests.test_dataset_model
        """
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests', pattern='test*.py')

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
