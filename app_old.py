from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from models import Product, Category, Customer, Order
from forms import NewProductForm


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/sdb_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_FOLDER'] = 'static'
app.config["SECRET_KEY"] = '123'


db = SQLAlchemy(app)


@app.route('/')
def index():
    sql = text('SELECT product.*, category.title FROM product LEFT JOIN category ON product.category_id = category.id')
    with db.engine.connect() as con:
        res = con.execute(sql)
        prods = [Product(*r) for r in res.fetchall()]
    return render_template('index.html', products=prods)

@app.route('/admin')
def admin_index():
    return render_template('admin/orders.html')

@app.route('/admin/products', methods = ['GET', 'POST'])
def admin_products():
    form = NewProductForm()
    sql_prods = text('SELECT product.*, category.title FROM product LEFT JOIN category ON product.category_id = category.id')
    sql_cat = text('SELECT *FROM category')
    sql_new_product = text('INSERT INTO product (title, price, category_id, amount_in_stock) VALUES (:title, :price, :category_id, :amount)')
    
    with db.engine.connect() as con:
        res_p = con.execute(sql_prods)
        res_c = con.execute(sql_cat)
        prods = [Product(*r) for r in res_p.fetchall()]
        cats = [Category(*r) for r in res_c.fetchall()]
        form.category.choices = [(cat.id, cat.title) for cat in cats]

    if request.method == 'POST' and form.validate_on_submit():
        try:
            with db.engine.connect() as con:
                con.execute(
                    sql_new_product, 
                    {
                        'title': form.title.data, 
                        'price': form.price.data, 
                        'category_id': form.category.data, 
                        'amount': form.amount.data
                    }
                )
                con.commit()
            return redirect('/admin/products')
        except Exception as e:
            print(e)
            con.rollback()
    return render_template('admin/products.html', products=prods, categories=cats, form=form)


"""
    TODO: product add ++++
    TODO: report 1
    TODO: DAO
    TODO: report 2
    TODO: next
    
    update is basically the same form as add new, onclick update redirect to update/<prod_id> <- prod_id is button id 
    where there's the form with current values filled in. On submit, update the data
"""



@app.route('/admin/customers')
def admin_customers():
    return render_template('admin/customers.html')


if __name__ == '__main__':
    app.run(debug=True)



"""

class FactType(Enum)
    MYSQL = 0
    Mongo = 1

factory = DAOFactory(Type.MYSQL)

c_dao = factory.get_customer_dao()
p_dao = factory.get_product_dao()

prods = p.get_all()
....

"""