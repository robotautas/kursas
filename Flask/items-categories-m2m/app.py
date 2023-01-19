from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    SubmitField, 
    )
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
key = 'blablablaverysecure'

app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


########################### DB Models ############################################

association_table = db.Table(
    'item_category', db.metadata,
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) 
    categories = db.relationship("Category", secondary=association_table, back_populates='items')

    def get_string_of_categories(self):
        string = ' '
        for cat in self.categories:
            string += f'{cat.name}, '
        return string[:-2]

    def __init__(self, name, categories):
        self.name = name
        self.categories = categories

    def __repr__(self):
        return f'Item({self.name})'


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    items = db.relationship("Item", secondary=association_table, back_populates='categories')

    def get_string_of_items(self):
        string = ' '
        for item in self.items:
            string += f'{item.name}, '
        return string[:-2]

    def __init__(self, name, items):
        self.name = name
        self.items = items

    def __repr__(self):
        return f'Category({self.name})'


########################### Forms  ############################################

def category_query():
    return Category.query

def item_query():
    return Item.query


class ItemForm(FlaskForm):
    name = StringField('Item', [DataRequired()])
    categories = QuerySelectMultipleField(
        query_factory=category_query,
        get_label='name',
        get_pk = lambda x: str(x)
    )
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    items = QuerySelectMultipleField(
        query_factory=item_query,
        get_label='name',
        get_pk = lambda x: str(x)
    )
    submit = SubmitField('Submit')


########################### Routes ############################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/items', methods=['GET', 'POST'])
def items():
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            categories=form.categories.data
        )
        db.session.add(new_item)
        db.session.commit()
    all_items = Item.query.all()
    return render_template('item.html', form=form, items=all_items)



@app.route('/categories', methods=['GET', 'POST'])
def contacts():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data, items=form.items.data)
        db.session.add(new_category)
        db.session.commit()
    all_categories = Category.query.all()
    return render_template('category.html', form=form, cats = all_categories)

@app.route('/delete_item/<int:id>')
def delete(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('items'))

@app.route('/update_item/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Item.query.get(id)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.categories = form.categories.data
        db.session.commit()
        return redirect(url_for('items'))
    return render_template('update_item.html', form=form, item=item)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3456, debug=True)



