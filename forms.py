from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, SubmitField, validators

from models import Product

class NewProductForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    category = SelectField('Category', [validators.DataRequired()])
    amount = IntegerField('Amount', [validators.NumberRange(min=0)])
    price = DecimalField('Price', [validators.NumberRange(min=0)])
    submit = SubmitField('Add Product', [validators.DataRequired()])


class UpdateProductForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired() ], )
    category = SelectField('Category', [validators.DataRequired()])
    amount = IntegerField('Amount', [validators.NumberRange(min=0)])
    price = DecimalField('Price', [validators.NumberRange(min=0)])
    submit = SubmitField('Save', [validators.DataRequired()])


class CustomerInfoForm(FlaskForm):
    f_name = StringField('First Name', [validators.DataRequired()], )
    l_name = StringField('Last Name', [validators.DataRequired()], )
    phone = StringField('Phone Num', [validators.DataRequired()], )
    address = StringField('Address', [validators.DataRequired()], )
    submit = SubmitField('Place Order', [validators.DataRequired()])
    