from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    items = association_proxy('reviews', 'item')

    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(db.Float)

    reviews = relationship('Review', back_populates='item', cascade='all, delete-orphan')

    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    comment = Column(String)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

    customer = relationship('Customer', back_populates='reviews')
    item = relationship('Item', back_populates='reviews')

    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'
