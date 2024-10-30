from mongoengine import Document, fields,DateTimeField
import datetime


class vendor_master_data(Document):
    sno=fields.IntField(uniuqe=True)
    company_name=fields.StringField()
    company_code=fields.StringField()
    company_address=fields.StringField()
    city=fields.StringField()
    state=fields.StringField()
    pincode=fields.StringField()
    gst=fields.StringField()
    phone_number=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    status=fields.StringField(default='A')
    

class generate_bill(Document):
    sno=fields.IntField(unique=True)
    invoice_no=fields.StringField()
    eway_number=fields.StringField()
    purchase_number=fields.StringField()
    purchase_date=fields.DateField()
    company_name=fields.StringField()
    billing_address=fields.StringField()
    shipping_address=fields.StringField()
    gst_number=fields.StringField()
    vechine_number=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    status=fields.StringField()

class product_details(Document):
    sno=fields.IntField()
    inv_bill=fields.StringField()
    product_name=fields.StringField()
    Hsn=fields.StringField()
    Quantity=fields.FloatField()
    UOM_data=fields.StringField()
    price=fields.FloatField()
    Amount=fields.FloatField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    status=fields.StringField()


class bill_details(Document):
    sno=fields.IntField()
    company_name=fields.StringField()
    bill_id=fields.StringField()
    inv_bill=fields.StringField()
    total_amount=fields.FloatField()
    sgst=fields.FloatField()
    cgst=fields.FloatField()
    total_amount_after_tax=fields.FloatField()
    file_path=fields.StringField()
    qr_code=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    status=fields.StringField()

class generate_bill_qua(Document):
    sno=fields.IntField(unique=True)
    invoice_no=fields.StringField()
    billing_address=fields.StringField()
    company_name=fields.StringField()
    gst_number=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    status=fields.StringField()
    
class product_details_qua(Document):
    sno=fields.IntField()
    inv_bill=fields.StringField()
    product_name=fields.StringField()
    Quantity=fields.FloatField()
    UOM_data=fields.StringField()
    price=fields.FloatField()
    Amount=fields.FloatField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    status=fields.StringField()


class bill_details_qua(Document):
    sno=fields.IntField()
    company_name=fields.StringField()
    bill_id=fields.StringField()
    inv_bill=fields.StringField()
    total_amount=fields.FloatField()
    sgst=fields.FloatField()
    cgst=fields.FloatField()
    total_amount_after_tax=fields.FloatField()
    file_path=fields.StringField()
    created_on=fields.DateTimeField()
    created_by=fields.StringField()
    status=fields.StringField()


# models.py
from mongoengine import Document, StringField, EmailField
from django.contrib.auth.hashers import make_password, check_password

class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default='user')  # Can be 'user', 'admin', etc.
    status=StringField()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


