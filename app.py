import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from s3_helper import test_s3_connection
from botocore.exceptions import ClientError

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_pyfile('config.py')

# Database configuration
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
        'postgres://', 'postgresql://', 1
    )
else:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "recipes.db")}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
admin = Admin(app, name='Recipe Admin', template_mode='bootstrap3')

# Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.String(20))
    servings = db.Column(db.Integer)
    prep_time = db.Column(db.String(20))
    image_url = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    nutritional_info = db.Column(db.Text)

# Admin interface
admin.add_view(ModelView(Recipe, db.session))

# File upload configuration
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class RecipeForm(FlaskForm):
    image = FileField('Recipe Image', validators=[
        FileAllowed(photos, 'Images only!')
    ])

# Context processor
@app.context_processor
def utility_processor():
    def generate_whatsapp_link(recipe_name):
        phone = app.config.get('WHATSAPP_NUMBER', '')
        message = f"Order {recipe_name}"
        return f"https://wa.me/{phone}?text={message}"
    return {'whatsapp_order_link': generate_whatsapp_link}

# Routes
@app.route('/')
def home():
    recipes = Recipe.query.all()
    categories = db.session.query(Recipe.category.distinct()).all()
    return render_template('index.html',
                         recipes=recipes,
                         categories=[c[0] for c in categories])

@app.route('/recipe/<int:id>')
def recipe_detail(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = Recipe.query.filter(
        Recipe.name.ilike(f'%{query}%') |
        Recipe.description.ilike(f'%{query}%')
    ).all()
    return render_template('search.html', results=results, query=query)

@app.route('/test-s3')
def test_s3():
    return test_s3_connection()

# Database initialization
with app.app_context():
    db.create_all()

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))