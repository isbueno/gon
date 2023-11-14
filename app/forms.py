from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired
    


from app.models.User import User

class RegisterUserForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=140)], render_kw={'placeholder': 'Nome'})
    cpf = StringField(validators=[InputRequired(), Length(max=14)], render_kw={'placeholder':  'CPF'})
    birth = StringField(validators=[InputRequired(), Length(max=10)], render_kw={'placeholder':  'Data de Nascimento'})
    email = StringField(validators=[InputRequired(), Length(min=4, max=75)], render_kw={'placeholder': 'E-mail'})
    whatsapp = StringField(validators=[InputRequired(), Length(max=16)], render_kw={'placeholder': 'Whatsapp'})
    password = PasswordField(validators=[InputRequired(),  Length(min=4, max=14)], render_kw={'placeholder':'Senha'})
    submit = SubmitField("Salvar")


class RegisterAddressForm(FlaskForm):
    zipcode = StringField(validators=[InputRequired()], render_kw={'placeholder':'CEP'})
    street =  StringField(validators=[InputRequired()], render_kw={'placeholder':'Rua'})
    number =  StringField(validators=[InputRequired()], render_kw={'placeholder':'Nº'})
    neighborhood =  StringField(validators=[InputRequired()], render_kw={'placeholder':'Bairro'})
    city =  StringField(validators=[InputRequired()], render_kw={'placeholder':'Cidade'})
    state =  StringField(validators=[InputRequired()], render_kw={'placeholder':'Estado'})


class RegisterVehicleForm(FlaskForm):
    model = StringField(validators=[InputRequired()], render_kw={'placeholder':'Modelo do veículo'})
    license_plate = StringField(validators=[InputRequired()], render_kw={'placeholder':'Placa'})
    type_vehicle = StringField(validators=[InputRequired()], render_kw={'placeholder':'Van/Carro'})
    color = StringField(validators=[InputRequired()], render_kw={'placeholder':'Cor'})
    number_seats = IntegerField('Quantidade de assentos', validators=[DataRequired()])
    additional_features = StringField(validators=[InputRequired()], render_kw={'placeholder':'features'})
    notes = StringField()


class RegisterSchool(FlaskForm):
    school = StringField('Sua instituição')    


class RegisterZone(FlaskForm):
    zone = StringField(validators=[InputRequired()], render_kw={'placeholder':'Cidade e região'})    


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=75)], render_kw={'placeholder': 'E-mail'})
    password = PasswordField(validators=[InputRequired(),  Length(min=4, max=14)], render_kw={'placeholder':'Password'})
    submit = SubmitField("Login")

from wtforms import HiddenField
class CommentForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    comment_text = TextAreaField('Comment_text', validators=[DataRequired()], render_kw={'placeholder': 'Mensagem'})
    user_id = HiddenField()


class SearchNameForm(FlaskForm):
    searchname = StringField(validators=[InputRequired()], render_kw={'placeholder':'Nome'})
    submit = SubmitField("Encontrar")