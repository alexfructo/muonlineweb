from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import Email, EqualTo, Length, DataRequired, Regexp, NumberRange, ValidationError
from wtforms.fields.html5 import EmailField
from classes import User, Login, Character


def ValidateUsername(form, field):
    if User.user_exists(field.data):
        raise ValidationError(
            u'Este nome de usuário já está sendo utilizado, por favor informe um nome diferente.')


def ValidateEmail(form, field):
    if User.email_exists(field.data):
        raise ValidationError(
            u'Este endereço de email já está sendo utilizado, por favor informe um email diferente.')

def ValidateCharName(form, field):
    if Character.char_exists(field.data):
        raise ValidationError(u'Este nome de personagem já está sendo utilizado, por favor informe um nome diferente.')


class RegisterForm(FlaskForm):

    username = StringField(u'Nome de usuário', validators=[
        DataRequired(message='Informe um nome de usuário.'),
        Length(min=4, max=30,
               message=u'O nome de usuário deve conter no mínimo 4 caracteres e no máximo 30.'),
        Regexp(r'^\w+$', message=u'O nome de usuário deve conter somente caracteres alpha-numéricos (a-z/0-9) e underline.'),
        ValidateUsername
    ])
    password = PasswordField(u'Senha', validators=[
        DataRequired(message=u'Informe uma senha.'),
        Length(min=4, max=30,
               message=u'A senha deve conter no mínimo 4 caracteres e no máximo 30.')
    ])
    password_r = PasswordField(u'Confirmação da senha', validators=[
        DataRequired(message=u'Informe a confirmação da senha.'),
        EqualTo('password', message=u'A senha e confirmação da senha não são iguais.')
    ])
    email = StringField(u'Email', validators=[
        DataRequired(message=u'Informe um endereço de e-mail.'),
        Email(message=u'Informe um endereço de e-mail válido.'),
        ValidateEmail
    ])
    email_r = StringField(u'Confirmação do email', validators=[
        DataRequired(message=u'Informe a confirmação do email.'),
        EqualTo('email', message=u'O email e a confirmação do email não são iguais.')
    ])
    personalid = StringField(u'Número pessoal', validators=[
        DataRequired(message=u'Informe um número pessoal.'),
        Length(min=8, max=8, message=u'O número pessoal deve conter 8 dígitos'),
        Regexp(
            r'^([\s\d]+)$', message=u'O número pessoal deve conter somente caracteres numéricos (0-9).')
    ])
    personalid_r = StringField(u'Confirmação do nº pessoal', validators=[
        DataRequired(message=u'Informe a confirmação dao nº pessoal.'),
        EqualTo(
            'personalid', message=u'O número pessoal e a confirmação do nº pessoal não são iguais.')
    ])
    terms = BooleanField(u'Termos de uso', validators=[
        DataRequired(message=u'Você deve ler e aceitar os termos de uso.')
    ])
    recaptcha = RecaptchaField(u'Recaptcha')
    submit = SubmitField('Confirmar')

class LoginForm(FlaskForm):

    username = StringField('Nome de usuário', validators=[
        DataRequired(message=u'Informe seu nome de usuário.')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Informe sua senha.')
    ])
    recaptcha = RecaptchaField(u'Recaptcha')
    submit = SubmitField('Confirmar')

class CharChangeName(FlaskForm):
    charname = StringField('Nome do Personagem', validators=[
        DataRequired(message=u'Informe o nome do personagem.'),
        Length(message=u'O nome do personagem deve conter no mínimo 4 caracteres e no máximo 10.', min=4, max=10),
        Regexp(r'^\w+$', message=u'O nome do personagem deve conter somente caracteres alpha-numéricos (a-z/0-9) e underline.'),
        ValidateCharName
    ])
    submit = SubmitField('Confirmar')

class UserChangePass(FlaskForm):
    password = PasswordField(label='Senha atual', validators=[
        DataRequired(message=u'Informe a sua senha atual')
    ])
    new_password = PasswordField(u'Nova senha', validators=[
        DataRequired(message=u'Informe a nova senha.'),
        Length(min=4, max=30,
               message=u'A nova senha deve conter no mínimo 4 caracteres e no máximo 30.')
    ])
    new_password_r = PasswordField(u'Confirmação da nova senha', validators=[
        DataRequired(message=u'Informe a confirmação da nova senha.'),
        EqualTo('new_password', message=u'A nova senha e confirmação da nova senha não são iguais.')
    ])
    submit = SubmitField('Confirmar')

class UserChangePID(FlaskForm):
    personalid = StringField(label='Número pessoal atual', validators=[
        DataRequired(message=u'Informe o seu número pessoal atual'),
        Length(message=u'O número pessoal deve conter 8 dígitos.', min=8, max=8),
        Regexp(
            r'^([\s\d]+)$', message=u'O número pessoal deve conter somente caracteres numéricos (0-9).')
    ])
    personalid_new = StringField(label='Novo nº pessoal', validators=[
        DataRequired(message=u'Informe o seu número pessoal atual'),
        Length(message=u'O número pessoal deve conter 8 dígitos.', min=8, max=8),
        Regexp(
            r'^([\s\d]+)$', message=u'O número pessoal deve conter somente caracteres numéricos (0-9).')
    ])
    personalid_new_r = StringField(label='Confirmação do nº pessoal', validators=[
        EqualTo('personalid_new', message=u'O novo nº pessoal e a confirmação do novo nº pessoal não são iguais.')
    ])

class ContactForm(FlaskForm):
    name = StringField(label='Nome', validators=[
        DataRequired(message=u'Informe o seu nome completo.'),
        Length(message='O nome de conter pelo menos 3 caracteres e no máximo 100.', min=2, max=100),
    ])
    email = EmailField(label='Email', validators=[
        DataRequired(message=u'Informe seu endereço de e-mail.'),
        Email(message=u'Informe um endereço de e-mail válido.')
    ])
    subject = StringField(label='Assunto', validators=[
        DataRequired(message=u'Informe o assunto.'),
        Length(message=u'O assunto deve conter pelo menos 4 caracteres e no máximo 100.', min=4, max=100)
    ])
    message = TextAreaField(label='Mensagem', validators=[
        DataRequired(message=u'Informe o motivo do contato no campo mensagem.'),
        Length(message=u'A mensagem deve conter pelo menos 10 caracteres e no máximo 510.', min=10, max=500)
    ])
    recaptcha = RecaptchaField(u'Recaptcha')
    submit = SubmitField(label='Confirmar')

class NewsForm(FlaskForm):
    title = StringField(label='Título', validators=[
        DataRequired(message='Informe o título da notícia.'),
        Length(message='O título deve conter no mínimo 4 caracteres e no máximo 100.', min=4, max=100)
    ])
    description = StringField(label='Descrição', validators=[
        DataRequired(message='Informe a descrição ou resumo da notícia.'),
        Length(message='A descrição deve conter no mínimo 4 caracteres e no máximo 100.', min=4, max=100)
    ])
    message = TextAreaField(label='Mensagem', validators=[
        DataRequired(message='Informe a mensagem da notícia'),
        Length(message='O Mensagem deve conter no mínimo 4 caracteres e no máximo 255.', min=4, max=255)
    ])
    submit = SubmitField(label='Confirmar')