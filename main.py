import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Shop, Book, Stock, Sale


DSN = 'postgresql://postgres:DavidLane88.@localhost:5432/Netology'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('json_data.json', 'r') as f:
    data = json.load(f)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))


def print_decor(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        return result
    return new_function

@print_decor
def publishers_books_sold(publisher_name=None, publisher_id=None):
    if publisher_name is not None:
        sales = session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        ).filter(
            Book.id_publisher == Publisher.id,
            Book.id == Stock.id_book,
            Sale.id_stock == Stock.id,
            Shop.id == Stock.id_shop,
            Publisher.name == publisher_name
        ).all()
        return sales


    elif publisher_id is not None:
        sales = session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        ).filter(
            Book.id_publisher == Publisher.id,
            Book.id == Stock.id_book,
            Sale.id_stock == Stock.id,
            Shop.id == Stock.id_shop,
            Publisher.id == publisher_id
        ).all()

table = publishers_books_sold(publisher_name='Pearson')
for c in table:
    print('|'.join(str(s) for s in c))
#session.commit()
session.close()
