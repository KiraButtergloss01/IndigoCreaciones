from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField, FileField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ProductForm(FlaskForm):
    categoria = StringField('Categoria', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripcion', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()])
    imagen = FileField('Imagen')
    submit = SubmitField('Agregar Producto')
