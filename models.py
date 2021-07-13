from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import inspect

db = SQLAlchemy()

class Users(UserMixin,db.Model):
    """Model for the users table"""
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key = True,autoincrement=True)
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    verified = db.Column(db.Boolean, default = False, nullable=False)
    phone = db.Column(db.String(11),nullable=True)

    def __repr__(self):
        """Define a way to print Users model"""
        return '<Users %r>' % self.id

    def __init__(self,fname,lname,email,password,role,verified=False):
        self.fname=fname
        self.lname=lname
        self.email=email
        self.password=password
        self.role=role
        self.verified=verified

class ProductCategory(db.Model):

    """Model for the product_category table"""
    __tablename__ = 'product_category'

    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    category = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        """Define a way to print ProductCategory model"""
        return '<ProductCategory %r>' % self.id

    def __init__(self,category):
        self.category=category

class Product(db.Model):
    """Model for the product table"""
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    vendor_name = db.Column(db.String(100), nullable=True)
    vendor_phone = db.Column(db.String(15), nullable=True)
    vendor_email = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text,nullable=True)
    category = db.Column(db.Integer, db.ForeignKey('product_category.id'),nullable=False)
    posted_by = db.Column(db.BigInteger, db.ForeignKey('users.id'),nullable=False)
    short_description = db.Column(db.Text, nullable = False)
    created_on = db.Column(db.DateTime,nullable = False,default=datetime.now())
    images = db.relationship('ProductImages', backref='product')
    critical_limit = db.Column(db.Integer,nullable=False,default=1)

    def __repr__(self):
        """Define a way to print Product model"""
        return '<Product %r>' % self.id

    def __init__(self,name,critical_limit,vendor_name,vendor_email,vendor_phone,description,category,short_description,posted_by):
        self.name=name
        self.vendor_email=vendor_email
        self.vendor_name=vendor_name
        self.vendor_phone=vendor_phone
        self.description=description
        self.category=category
        self.posted_by=posted_by
        self.short_description=short_description
        self.critical_limit=critical_limit

class ProductImages(db.Model):
    """Model for the product_images table"""
    __tablename__ = 'product_images'

    id = db.Column(db.BigInteger, primary_key = True,autoincrement=True)
    image = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)
    show = db.Column(db.Boolean, default=True,nullable=False)
    filename = db.Column(db.String(250),nullable=False,default='undefined')

    def __str__(self):
        """Return image path"""
        return self.image

    def __repr__(self):
        """Define a way to print ProductImages model"""
        return '<ProductImages %r>' % self.id

class Images(db.Model):
    """Model for the images table"""
    __tablename__ = 'images'

    id = db.Column(db.BigInteger, primary_key = True,autoincrement=True)
    image = db.Column(db.Text, nullable=False)
    external_id = db.Column(db.BigInteger,nullable=False)
    image_of = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(250),nullable=False,default='undefined')

    def __str__(self):
        """Return image path"""
        return self.image

    def __repr__(self):
        """Define a way to print Images model"""
        return '<Images %r>' % self.id

class Inventory(db.Model):
    """Model for the inventory table"""
    __tablename__ = 'inventory'

    id = db.Column(db.BigInteger, primary_key = True,autoincrement=True)
    status = db.Column(db.Integer, nullable=False, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now,nullable=False)

    def __repr__(self):
        """Define a way to print Inventory model"""
        return '<Inventory %r>' % self.id

    def __init__(self,status,product_id):
        self.status=status
        self.product_id=product_id

class ItemIssued(db.Model):
    """Model for the item_issued table"""
    __tablename__ = 'item_issued'

    id = db.Column(db.BigInteger, primary_key = True,autoincrement=True)
    location = db.Column(db.String("150"), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.id'),nullable=False)
    issued_to = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    received_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    issued_on = db.Column(db.DateTime,default=datetime.now,nullable=False)
    expected_return = db.Column(db.DateTime,nullable=False)
    returned_on = db.Column(db.DateTime,nullable=True)
    returned = db.Column(db.Boolean,nullable=False,default=False)
    transfered = db.Column(db.Boolean,nullable=False,default=False)
    
    def __repr__(self):
        """Define a way to print ItemIssued model"""
        return '<ItemIssued %r>' % self.id

    def __init__(self,item_id,location,remarks,issued_to,approved_by,expected_return):
        self.item_id=item_id
        self.approved_by=approved_by
        self.expected_return=expected_return
        self.issued_to=issued_to
        self.remarks=remarks
        self.location=location

class Ticket(db.Model):
    """Model for the ticket table"""
    __tablename__ = 'ticket'

    id = db.Column(db.BigInteger, primary_key = True,autoincrement=True)
    title = db.Column(db.String(250),nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.id'),nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    closed_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    status_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    created_on = db.Column(db.DateTime,default=datetime.now,nullable=False)
    closed_on = db.Column(db.DateTime,nullable=True)
    due_date = db.Column(db.DateTime,nullable=False)
    priority = db.Column(db.String(8),nullable=False,default='low')
    status_updated_on = db.Column(db.DateTime,default=datetime.now,nullable=False)
    isclosed = db.Column(db.Boolean,nullable=False,default=False)
    status = db.Column(db.String(100),nullable=False,default='Request Initiated')
    ticket_type = db.Column(db.String(20),nullable=False)
    
    def __repr__(self):
        """Define a way to print Ticket model"""
        return '<Ticket %r>' % self.id


class Replies(db.Model):
    """Model for the replies table"""
    __tablename__ = 'replies'

    id = db.Column(db.BigInteger, primary_key = True,autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    posted_on = db.Column(db.DateTime,default=datetime.now,nullable=False)

    def __repr__(self):
        """Define a way to print Replies model"""
        return '<Replies %r>' % self.id
