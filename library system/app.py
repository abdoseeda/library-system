from flask import Flask, render_template, request, redirect, url_for, session, jsonify


app = Flask(__name__)
app.secret_key = 'supersecretkey'


users = {} 
books = [
    {
        'id': 1,
        'title': 'The Twenty Greatest Philosophy Books',
        'image': '/static/images/9780826490544.jpg',
        'price': 20.99
    },
    {
        'id': 2,
        'title': 'Best of Philosophy Books',
        'image': '/static/images/813iZu3lpaL._AC_UF1000,1000_QL80_.jpg',
        'price': 15.99
    },
    {
        'id': 3,
        'title': 'The Philosophy Book',
        'image': '/static/images/91YTGVJZepL._AC_UF1000,1000_QL80_.jpg',
        'price': 18.50
    },
]
carts = {}  

@app.route('/')
def index():
    return render_template('index.html', logged_in='email' in session)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users:
            return render_template('signup.html', error='Account already exists!')

        users[email] = {'name': name, 'password': password}
        carts[email] = []  
        session['email'] = email  
        return redirect(url_for('books_page'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email]['password'] == password:
            session['email'] = email  # Store user in session
            return redirect(url_for('books_page'))

        return render_template('signin.html', error='Invalid email or password!')

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/books')
def books_page():
    if 'email' not in session:
        return redirect(url_for('signin'))

    email = session['email']
    user_cart = carts[email]
    return render_template('books.html', books=books, cart=user_cart, logged_in=True)

@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    if 'email' not in session:
        return redirect(url_for('signin'))

    email = session['email']
    if request.method == 'POST':
        data = request.get_json()
        book_id = data.get('id')

        
        for book in books:
            if book['id'] == book_id:
                carts[email].append(book)
                return jsonify({'message': f"{book['title']} added to cart!"})

    return render_template('cart.html', cart=carts[email], logged_in=True)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'email' not in session:
        return redirect(url_for('signin'))

    email = session['email']
    user_cart = carts[email]

    if request.method == 'POST':
        
        carts[email] = []
        return render_template('confirmation.html', message="Your order has been placed successfully!")

    return render_template('checkout.html', cart=user_cart, logged_in=True)

@app.route('/about')
def about():
    return render_template('about.html', logged_in='email' in session)

if __name__ == '__main__':
    app.run(debug=True)
