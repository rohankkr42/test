from flask import Flask, render_template, request, jsonify, session
import redis

app = Flask(__name__)
app.secret_key = 'random_secret_key'

# Connect to Redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# Sample product data to simulate a product catalog
PRODUCTS = {
    1: {'name': 'Laptop', 'price': 1000},
    2: {'name': 'Smartphone', 'price': 700},
    3: {'name': 'Headphones', 'price': 150}
}

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)

    # Cache the cart in Redis for fast access
    redis_client.set(f"cart_{session.sid}", str(session['cart']))
    return jsonify({"message": "Product added to cart", "cart": session['cart']}), 200

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    products_in_cart = [PRODUCTS[pid] for pid in cart_items]
    return render_template('cart.html', cart=products_in_cart)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    redis_client.delete(f"cart_{session.sid}")
    return jsonify({"message": "Cart cleared"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

