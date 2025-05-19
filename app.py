from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

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

# Admin
admin = Admin(app, name='Recipe Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Recipe, db.session))

# Context processor
@app.context_processor
def utility_processor():
    def generate_whatsapp_link(recipe_name):
        phone = app.config['WHATSAPP_NUMBER']
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

if __name__ == '__main__':
    app.run(debug=True)