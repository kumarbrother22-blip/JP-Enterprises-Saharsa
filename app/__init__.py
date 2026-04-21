import os
import sqlite3
from functools import wraps

from flask import Flask, flash, g, redirect, render_template, request, session, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'dev-secret-change-me'),
        DATABASE=os.path.join(app.instance_path, 'inventory.sqlite3'),
        ADMIN_USERNAME=os.environ.get('ADMIN_USERNAME', 'admin'),
        ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD', 'jp@2022'),
        STORE_PHONE='+919122291700',
        STORE_WHATSAPP='919122291700',
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(app.config['DATABASE'])
            g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(_=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price TEXT,
                condition TEXT NOT NULL DEFAULT 'New',
                image_url TEXT,
                featured INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        row_count = db.execute('SELECT COUNT(*) as count FROM products').fetchone()['count']
        if row_count == 0:
            sample_products = [
                ('iPhone 14', 'Apple iPhones (New & Second-hand)', '₹52,999', 'Second-hand', 'https://images.unsplash.com/photo-1678911820864-e5fef2a8dc7f?auto=format&fit=crop&w=900&q=80', 1),
                ('Samsung Galaxy S23', 'Samsung', 'Call for best price', 'New', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=900&q=80', 0),
                ('OnePlus 12R', 'OnePlus', '₹38,999', 'New', 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80', 0),
                ('Redmi Note 13', 'Xiaomi', '₹18,999', 'New', 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=80', 0),
                ('Vivo V30', 'Vivo', 'Call for best price', 'New', 'https://images.unsplash.com/photo-1510557880182-3f8a7a7f4f03?auto=format&fit=crop&w=900&q=80', 0),
            ]
            db.executemany(
                'INSERT INTO products (name, category, price, condition, image_url, featured) VALUES (?, ?, ?, ?, ?, ?)',
                sample_products,
            )
        db.commit()

    def login_required(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))
            return view(**kwargs)

        return wrapped_view

    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()

    @app.route('/')
    def home():
        db = get_db()
        products = db.execute('SELECT * FROM products ORDER BY created_at DESC LIMIT 9').fetchall()
        return render_template('index.html', products=products)

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
                session['admin_logged_in'] = True
                flash('Welcome to admin panel!', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Invalid credentials. Please try again.', 'error')
        return render_template('admin_login.html')

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('admin_login'))

    @app.route('/admin')
    @login_required
    def admin_dashboard():
        db = get_db()
        products = db.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
        return render_template('admin_dashboard.html', products=products)

    @app.route('/admin/products/add', methods=['POST'])
    @login_required
    def admin_add_product():
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', '').strip() or 'Call for best price'
        condition = request.form.get('condition', 'New').strip()
        image_url = request.form.get('image_url', '').strip() or 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80'
        featured = 1 if request.form.get('featured') == 'on' else 0

        if not name or not category:
            flash('Product name and category are required.', 'error')
            return redirect(url_for('admin_dashboard'))

        db = get_db()
        db.execute(
            'INSERT INTO products (name, category, price, condition, image_url, featured) VALUES (?, ?, ?, ?, ?, ?)',
            (name, category, price, condition, image_url, featured),
        )
        db.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    @app.post('/admin/products/<int:product_id>/delete')
    @login_required
    def admin_delete_product(product_id):
        db = get_db()
        db.execute('DELETE FROM products WHERE id = ?', (product_id,))
        db.commit()
        flash('Product deleted.', 'success')
        return redirect(url_for('admin_dashboard'))

    @app.context_processor
    def inject_store_data():
        return {
            'store': {
                'name': 'JP Enterprises Saharsa',
                'type': 'Mobile & Gadget Store',
                'established': '2022',
                'rating': '4.6',
                'address': 'Near Bangaon Rd, Ward Number 22, Krishna Nagar, Saharsa, Bihar 852201',
                'phone_display': '+91 91222 91700',
                'phone_tel': app.config['STORE_PHONE'],
                'whatsapp': app.config['STORE_WHATSAPP'],
            }
        }

    return app


# Expose a module-level app for WSGI servers (e.g., gunicorn app:app)
app = create_app()
