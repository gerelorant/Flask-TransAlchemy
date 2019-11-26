# Flask-TransAlchemy

Simple translation support for Flask-SQLAlchemy based database tables.

## Usage
Initialize the TransAlchemy extension with the Flask and Flask-SQLAlchemy 
instances. 
```python
from flask import Flask
from flask_transalchemy import TransAlchemy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
translations = TransAlchemy(app, db)
    

if __name__ == '__main__':
    app.run()
```
To add translatable abilities to your models, use the 
`TranslatableMixin` class. The translatable columns should be defined in the 
`translatable_columns` class attribute.
```python
from flask_transalchemy import TranslatableMixin


class SomeModel(db.Model, TranslatableMixin):
    translatable_columns = ['text_field']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_field = db.Column(db.String(40))
    not_translatable_text_field = db.Column(db.String(10))
```
Translations not bind to any model can also be utilized with the `set_label()`
and `get_label()` methods.
```python
with app.app_context():
    set_label('hello', 'Welcome {name}!', language='en')
    set_label('hello', 'Willkommen {name}!', language='de')
    set_label('hello', 'Bienvenue {name}!', language='fr')
    set_label('hello', 'Bienvenido  {name}!', language='es')

@app.route('/<name>')
def hello(name: str):
    return get_label('hello').format(name=name)
```
If the `label_route` parameter was specified at initialization, the label 
translations are accessible over the provided route. Visiting 
`/<label_route>/hello?name=John` would return `Welcome John!` in the previous 
case. This might be useful for frontend or client application development.