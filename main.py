
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gemini3.db'
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)

# Create the database tables
db.create_all()

# Define the home route
@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

# Define the products route
@app.route('/products')
def products():
    """Render the products page."""
    products = Product.query.all()
    return render_template('products.html', products=products)

# Define the product details route
@app.route('/product-details/<int:product_id>')
def product_details(product_id):
    """Render the product details page."""
    product = Product.query.get_or_404(product_id)
    return render_template('product-details.html', product=product)

# Define the add to cart route
@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    """Add a product to the cart."""
    product = Product.query.get_or_404(product_id)

    # Check if the product is already in the cart
    if product.id in request.cookies.get('cart', ''):
        return jsonify({'error': 'Product already in cart'})

    # Add the product to the cart
    cart = request.cookies.get('cart', '')
    cart += str(product.id) + ','
    response = jsonify({'success': 'Product added to cart'})
    response.set_cookie('cart', cart)
    return response

# Define the cart route
@app.route('/cart')
def cart():
    """Render the cart page."""
    cart_ids = request.cookies.get('cart', '').split(',')
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    return render_template('cart.html', products=products)

# Define the checkout route
@app.route('/checkout')
def checkout():
    """Render the checkout page."""
    cart_ids = request.cookies.get('cart', '').split(',')
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    return render_template('checkout.html', products=products)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
