import datetime
from afrocentricapp import db

pkg_inclusions = db.Table('pkg_inclusives', db.Column('fk_pkg_inclusive_tourpackage_id', db.Integer, db.ForeignKey('tourpackage.tourpackage_id')),
db.Column('fk_pkg_inclusive_id', db.Integer, db.ForeignKey('inclusive.inclusive_id')))


class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_fname = db.Column(db.String(255), nullable=False)
    admin_lname = db.Column(db.String(255), nullable=False)
    admin_email = db.Column(db.String(255), nullable=False, unique=True)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)


class Country(db.Model): 
    country_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    country_iso = db.Column(db.String(255), nullable=False)
    country_name = db.Column(db.String(255), nullable=False)
    country_nicename = db.Column(db.String(255), nullable=False)
    country_iso3 = db.Column(db.String(255), nullable=False)
    country_numcode = db.Column(db.Integer(), nullable=False)
    country_phonecode = db.Column(db.Integer(), nullable=False)
    #relationship
    country_destination = db.relationship('Destination', back_populates='destination_country')
    country_state = db.relationship('State', back_populates='state_country')
    country_visa = db.relationship('Visa', back_populates='visa_country')
    

class CustomRequest(db.Model):
    custom_request_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    custom_request_fname = db.Column(db.String(255), nullable=False)
    custom_request_lname= db.Column(db.String(255), nullable=False)
    custom_request_email =  db.Column(db.String(255), nullable=False)
    customer_request_phone= db.Column(db.String(255), nullable=False)
    custom_request_country =  db.Column(db.String(255), nullable=False)
    custom_request_origin_city =  db.Column(db.String(255), nullable=False)
    custom_request_destination_city =  db.Column(db.String(255), nullable=False)
    custom_request_travel_date = db.Column(db.Date(), nullable=False)
    custom_request_return_date = db.Column(db.Date(), nullable=False)
    custom_request_group_size = db.Column(db.Enum('Solo','Couple','Family','Group'), nullable=False)
    custom_request_additional_info = db.Column(db.Text(), nullable=False)

class Contactus(db.Model):
    contactus_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    contactus_fullname = db.Column(db.String(255), nullable=False)
    contactus_email= db.Column(db.String(255), nullable=False)
    contactus_subject =  db.Column(db.String(255), nullable=False)
    contactus_message = db.Column(db.Text(), nullable=False)

class Customer(db.Model): 
    customer_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    customer_fname = db.Column(db.String(255), nullable=False)
    customer_lname = db.Column(db.String(255), nullable=False)
    customer_phone = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False, unique=True)
    customer_gender = db.Column(db.Enum('Male','Female'), nullable=False)
    customer_pword = db.Column(db.String(255), nullable=False)
    customer_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)
    #relationship
    customer_order = db.relationship('Order', back_populates='order_customer')
    customer_tourbooking= db.relationship('Tourbooking', back_populates='tourbooking_customer')
    customer_procurement= db.relationship('Visaprocurement', back_populates = 'procurement_customer')


class Destination(db.Model):
    destination_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    destination_location = db.Column(db.String(255), nullable=False)
    fk_destination_state = db.Column(db.Integer(), db.ForeignKey("state.state_id"))
    fk_destination_country = db.Column(db.Integer(), db.ForeignKey("country.country_id"))
    #relationship
    destination_state = db.relationship('State', back_populates='state_destination')
    destination_country = db.relationship('Country', back_populates='country_destination')
    destination_tourpackage = db.relationship('Tourpackage', back_populates='tourpackage_destination')


class Inclusive(db.Model):
    inclusive_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    inclusive_name = db.Column(db.String(255), nullable=False)
    #secondary relationship(pkg_inclusions)
    inclusive_tourpackage = db.relationship('Tourpackage', secondary=pkg_inclusions, back_populates = 'tourpackage_inclusives')


class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    order_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    order_shipment_address = db.Column(db.Text(255), nullable=False)
    fk_order_customer_id = db.Column(db.Integer(), db.ForeignKey("customer.customer_id"))
    #relationship
    order_customer = db.relationship('Customer', back_populates='customer_order')
    order_details = db.relationship('OrderDetails', back_populates='details_order')
    order_shipment = db.relationship('Shipment', back_populates='shipment_order')


class OrderDetails(db.Model):
    order_details_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    order_details_qty = db.Column(db.Integer(), nullable=False)
    order_details_amt = db.Column(db.Float(), nullable=False)
    fk_order_details_product_id = db.Column(db.Integer(), db.ForeignKey("product.product_id"))
    fk_order_details_order_id = db.Column(db.Integer(), db.ForeignKey("order.order_id"))
    #relationship
    details_product = db.relationship('Product', back_populates='product_details')
    details_order = db.relationship('Order', back_populates='order_details')


class Product(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    product_qty = db.Column(db.Integer(), nullable=False)
    product_category = db.Column(db.Enum('Afro-art','Travel Souvenir','Afro-fashion'))
    product_pics = db.Column(db.String(255), nullable=False)
    product_title = db.Column(db.String(255), nullable=False)
    product_desc = db.Column(db.Text(), nullable=False)
    product_price = db.Column(db.Float(), nullable=False)
    product_availability = db.Column(db.Enum('Available','Out of Stock'))
    #relationship
    product_details = db.relationship('OrderDetails', back_populates='details_product')


class Shipment(db.Model):
    shipment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    shipment_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    fk_shipment_order_id = db.Column(db.Integer(), db.ForeignKey("order.order_id"))
    shipment_status = db.Column(db.Enum('Shipped','Pending'))
    #relationship
    shipment_order = db.relationship('Order', back_populates='order_shipment')


class State(db.Model):
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)
    fk_state_country_id = db.Column(db.Integer(), db.ForeignKey("country.country_id"))
    #relationship
    state_country = db.relationship('Country', back_populates='country_state')
    state_destination = db.relationship('Destination', back_populates='destination_state')


class Tourbooking(db.Model):
    tourbooking_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tourbooking_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)
    tourbooking_customer_email= db.Column(db.String(255), nullable=False)
    tourbooking_status = db.Column(db.Enum('Confirmed','Pending'),nullable=False) 
    tourbooking_fname = db.Column(db.String(255), nullable=False)
    tourbooking_lname= db.Column(db.String(255), nullable=False)
    tourbooking_ref= db.Column(db.Integer(), nullable=False)
    tourbooking_amount= db.Column(db.Float(), nullable=False)
    fk_tourbooking_tourpackageid = db.Column(db.Integer(), db.ForeignKey("tourpackage.tourpackage_id"))
    fk_tourbooking_customerid = db.Column(db.Integer(), db.ForeignKey("customer.customer_id"))
    #relationship
    tourbooking_tourpackage = db.relationship('Tourpackage', back_populates='tourpackage_tourbooking')
    tourbooking_customer = db.relationship('Customer', back_populates='customer_tourbooking')
    tourbooking_tourpackage= db.relationship('Tourpackage', back_populates='tourpackage_tourbooking')
    tourbooking_payment= db.relationship('TourpackagePayment', back_populates='payment_tourbooking')

class Tourpackage(db.Model):
    tourpackage_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tourpackage_name= db.Column(db.String(255), nullable=False)
    tourpackage_price_sharing = db.Column(db.Float(), nullable=False)
    tourpackage_price_single =  db.Column(db.Float(), nullable=False)
    tourpackage_desc = db.Column(db.Text(), nullable=False)
    tourpackage_pics = db.Column(db.String(255), nullable=False)
    tourpackage_dept_date = db.Column(db.Date(), nullable=False)
    tourpackage_rtn_date = db.Column(db.Date(), nullable=False)
    tourpackage_slot = db.Column(db.Integer(), nullable=True)
    tourpackage_available = db.Column(db.Integer(), nullable=False)
    fk_tourpackage_destination_id = db.Column(db.Integer(), db.ForeignKey("destination.destination_id"))
    #relationship
    tourpackage_destination = db.relationship('Destination', back_populates='destination_tourpackage')
    tourpackage_tourbooking = db.relationship('Tourbooking', back_populates='tourbooking_tourpackage')
    tourpackage_payment= db.relationship('TourpackagePayment', back_populates='payment_tourpackage')
    #secondary relationship(pkg_inclusions)
    tourpackage_inclusives= db.relationship('Inclusive', secondary=pkg_inclusions, back_populates = 'inclusive_tourpackage')


class TourpackagePayment(db.Model):
    tourpackage_payment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tourpackage_payment_amount = db.Column(db.Float(), nullable=False)
    tourpackage_payment_status = db.Column(db.Enum('Successful','Failed'))
    tourpackage_payment_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    tourpackage_payment_method = db.Column(db.String(255), nullable=False)
    tourpackage_payment_ref = db.Column(db.Integer(), nullable=False)
    tourpackage_payment_currency = db.Column(db.String(255), nullable=False)
    fk_tourpackage_payment_tourpackage_id = db.Column(db.Integer(), db.ForeignKey("tourpackage.tourpackage_id"))
    fk_tourpackage_payment_tourbooking_id = db.Column(db.Integer(), db.ForeignKey("tourbooking.tourbooking_id"))
    #relationship
    payment_tourpackage = db.relationship('Tourpackage', back_populates='tourpackage_payment')
    payment_tourbooking = db.relationship('Tourbooking', back_populates='tourbooking_payment')


class Visa(db.Model):
    visa_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    visa_name = db.Column(db.String(255), nullable=False)
    visa_category = db.Column(db.Enum('Tourist Visa','Study Visa','Business Visa','Work Visa'))
    visa_requirement = db.Column(db.Text(), nullable=False)
    visa_pics = db.Column(db.String(255), nullable=False)
    visa_price = db.Column(db.Float(), nullable=False)
    visa_duration = db.Column(db.String(255), nullable=False)
    fk_visa_country = db.Column(db.Integer(), db.ForeignKey('country.country_id'))
    #relationship
    visa_payment= db.relationship('VisaPayment', back_populates='payment_visa')
    visa_country = db.relationship('Country', back_populates = 'country_visa')
    visa_procurement = db.relationship('Visaprocurement', back_populates = 'procurement_visa')


class VisaPayment(db.Model):
    visa_payment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    visa_payment_amount= db.Column(db.Float(), nullable=False)
    visa_payment_status = db.Column(db.Enum('Successful','Failed'))
    visa_payment_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    visa_payment_method = db.Column(db.Enum('Card','Bank Transfer'))
    fk_visa_payment_visa_id = db.Column(db.Integer(), db.ForeignKey("visa.visa_id"))
    fk_visa_payment_procurement = db.Column(db.Integer(), db.ForeignKey('visaprocurement.visa_procurement_id'))
    #relationship
    payment_visa = db.relationship('Visa', back_populates='visa_payment')
    payment_procurement = db.relationship('Visaprocurement', back_populates='procurement_payment')


class Visaprocurement(db.Model):
    visa_procurement_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    visa_procurement_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    visa_procurement_customer_email = db.Column(db.String(255), nullable=False)
    visa_procurement_customer_phone = db.Column(db.String(255), nullable=False)
    visa_procurement_fname = db.Column(db.String(255), nullable=False)
    visa_procurement_lname = db.Column(db.String(255), nullable=False)
    fk_visa_procurement_visa_id = db.Column(db.Integer(), db.ForeignKey("visa.visa_id"))
    fk_visa_procurement_customer_id = db.Column(db.Integer(), db.ForeignKey("customer.customer_id"))
    #relationship
    procurement_visa = db.relationship('Visa', back_populates = 'visa_procurement')
    procurement_customer = db.relationship('Customer', back_populates = 'customer_procurement')
    procurement_payment= db.relationship('VisaPayment', back_populates='payment_procurement')
    

class Reviews(db.Model):
    review_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    r_customer_fullname = db.Column(db.String(255), nullable=False)
    r_customer_email = db.Column(db.String(255), nullable=False)
    review_ratings = db.Column(db.Integer(), nullable=False)
    review_Info = db.Column(db.Text(), nullable=False)


class Subscribers(db.Model):
    subscribers_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    subscribers_email = db.Column(db.String(255), nullable=False)

