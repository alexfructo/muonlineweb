################################################################################################################################
#   Continente MU Web Page
#
#   @author     Alex <alexfructo@gmail.com>
#   @version    1.0.0
#   @date       18/04/2019
################################################################################################################################

from flask import Flask, render_template, request, abort, session, redirect, url_for, flash, abort, send_from_directory, jsonify, send_file
from flask_mail import Mail, Message
from datetime import datetime
from sql import MSSQL
import os.path
import locale
import forms
import classes
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.WEB_SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = config.WEB_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = config.WEB_SECRET_KEY
app.config['RECAPTCHA_DATA_ATTRS'] = {'theme': 'dark', 'data-size': 'compact'}
app.config['MAIL_SERVER'] = config.SMTP_HOST
app.config['MAIL_PORT'] = config.SMTP_PORT
app.config['MAIL_USE_SSL'] = config.SMTP_SSL
app.config['MAIL_USERNAME'] = config.SMTP_USER
app.config['MAIL_PASSWORD'] = config.SMTP_PASS

mail = Mail(app)
locale.setlocale(locale.LC_ALL, "Portuguese_Brazil.1252")


@app.context_processor
def context():

    return dict(
        SERVER_NAME=config.SERVER_NAME,
        NAME_CHANGE_COST=config.CHAR_CNAME_COST,
    )


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt='%Y-%m-%d'):
    return date.strftime(fmt)


@app.route('/')
def index():
    return render_template('index.html', news=classes.News.get_news())


@app.route('/noticia/<int:id>', methods=['GET'])
def news(id):
    data = classes.News.get_new_byid(id)
    if data is not None:
        return render_template('news.html', data=data)
    else:
        return abort(404)


@app.route('/downloads')
def downloads():
    return render_template('downloads.html')


@app.route('/rankings')
def rankings():
    return render_template('rankings.html')


@app.route('/informacoes')
def informations():
    return render_template('informations.html')


@app.route('/contato', methods=['GET', 'POST'])
def contact():
    form = forms.ContactForm()
    if form.validate_on_submit():

        user = 'Anônimo'
        ip = request.remote_addr
        if session.get('username'):
            user = session['username']

        try:
            msg = Message(
                '[Continente MU] - ' + form.subject.data,
                sender=config.SMTP_USER,
                recipients=[config.SMTP_USER]
            )
            msg.body = f'''
                            Olá, Administrador!
                            Você recebeu uma nova mensagem de contato pelo site.\n
                            Nome: {form.name.data}
                            Email: {form.email.data}
                            Assunto: {form.subject.data}
                            Mensagem: {form.message.data}\n
                            Usuário: {user}
                            IP: {ip}
                            Data: {datetime.now():%Y-%m-%d}
                            '''
            mail.send(msg)
            flash(u'Obrigado, a sua mensagem foi enviada com sucesso!',
                  category='success')
        except Exception as e:
            print(str(e))
            flash(u'Lamentamos, não foi possível entregar a sua mensagem, tente novamente mais tarde.', category='danger')
    return render_template('contact.html', form=form)


@app.route('/loja')
def shop():
    return render_template('shop.html')


@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = classes.User(
                form.username.data, form.password.data, form.email.data, form.personalid.data)
            user.register()
            flash(
                f'Parabéns, a conta {user.username} foi registrada com sucesso! \n Agora você já pode conectar-se no servidor.', category='success')
        else:
            flash(u'Foram encontrados erros no preenchimento do formulário, por favor verifique os itens em vermelho.',  category='danger')

    return render_template('register.html', form=form)


@app.route('/entrar', methods=['GET', 'POST'])
def login():
    if not session.get('username'):
        form = forms.LoginForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                login = classes.Login(form.username.data, form.password.data)

                if not login.auth():
                    flash(f'Atenção, nome de usuário ou senha incorretos!',
                          category='danger')
                else:
                    session['username'] = login.username
                    return redirect(url_for('profile'))

        return render_template('login.html', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/sair')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/usuario')
def profile():
    if session.get('username'):
        last_logon = classes.Login.get_last_logon(session['username'])
        characters = classes.Character.get_account_characters(
            session['username'])
        user = classes.User.get_user(session['username'])
        return render_template('profile.html', last_logon=last_logon, characters=characters, user=user)
    else:
        return abort(403)


@app.route('/usuario/personagem/nome/alterar', methods=['GET', 'POST'])
def char_change_name():

    if session.get('username'):

        form = forms.CharChangeName()
        last_logon = classes.Login.get_last_logon(session['username'])
        characters = classes.Character.get_account_characters(
            session['username'])
        user = classes.User.get_user(session['username'])

        if request.method == 'POST':
            if form.validate_on_submit():
                char = request.form.get('characterName')
                if not user[4] >= config.CHAR_CNAME_COST:
                    flash(
                        u'Créditos insuficientes para realizar a operação!', category='danger')
                elif classes.Character.char_online(form.charname.data):
                    flash(
                        u'Para realizar esta operação você não pode estar conectado no jogo.', category='danger')
                elif classes.Character.validate_charname(session['username'], char):
                    classes.Character.update_charname(
                        session['username'], char, form.charname.data)
                    flash(u'Nome do personagem alterado com sucesso!',
                          category='success')
                else:
                    flash(
                        u'Por favor, selecione o Personagem que deseja alterar o nome.', category='danger')

        return render_template('profile/char_change_name.html', last_logon=last_logon, characters=characters, user=user, form=form)
    else:
        return abort(403)


@app.route('/usuario/senha/alterar', methods=['GET', 'POST'])
def account_change_password():

    if session.get('username'):

        form = forms.UserChangePass()
        last_logon = classes.Login.get_last_logon(session['username'])
        user = classes.User.get_user(session['username'])

        if request.method == 'POST':
            if form.validate_on_submit():
                if classes.Login.check_password(session['username'], form.password.data):
                    classes.User.change_password(
                        session['username'], form.new_password.data)
                    flash(u'Senha alterada com sucesso!', category='success')
                else:
                    flash(u'Senha atual inválida, tente novamente.',
                          category='danger')

        return render_template('profile/account_change_password.html', last_logon=last_logon, user=user, form=form)
    else:
        return abort(403)


@app.route('/usuario/npessoal/alterar', methods=['GET', 'POST'])
def account_change_pid():

    if session.get('username'):
        form = forms.UserChangePID()
        last_logon = classes.Login.get_last_logon(session['username'])
        user = classes.User.get_user(session['username'])

        if request.method == 'POST':
            if form.validate_on_submit():
                if classes.Login.check_personalid(session['username'], form.personalid.data):
                    classes.User.change_personalid(
                        session['username'], form.personalid_new.data)
                    flash(u'Número pessoal alterado com sucesso!',
                          category='success')
                else:
                    flash(
                        u'Número pessoal atual inválido, tente novamente.', category='danger')

        return render_template('profile/account_change_pid.html', last_logon=last_logon, user=user, form=form)
    else:
        return abort(403)


@app.route('/usuario/noticias/')
def account_news():

    if session.get('username'):
        user = classes.User.get_user(session['username'])

        if user[2] > 0:
            last_logon = classes.Login.get_last_logon(session['username'])

            news = classes.News.get_all_news()
            return render_template('profile/news/news.html', last_logon=last_logon, user=user, news=news)
        else:
            return redirect(url_for('profile'))
    else:
        return abort(403)


@app.route('/usuario/noticias/excluir/<int:id>', methods=['GET', 'POST'])
def account_remove_news(id):
    # verifica se a notícia existe
    data = classes.News.get_new_byid(id)

    if data is not None:
        # verifica se o usuário está logado
        if session.get('username'):
            # obtém os dados do usuário
            user = classes.User.get_user(session['username'])

            # verifica se o usuário é admin
            if user[2] > 0:

                # instancia os objetos que precisam ser enviado a view
                last_logon = classes.Login.get_last_logon(session['username'])

                if request.method == 'POST':
                    classes.News.delete_news_byid(id)
                    flash('Notícia removida com sucesso!', category='success')
                    return redirect(url_for('account_news'))

                return render_template('profile/news/delete_news.html', last_logon=last_logon, user=user, data=data)
            else:
                return redirect(url_for('profile'))
        else:
            return abort(403)
    else:
        return abort(404)


@app.route('/usuario/noticias/editar/<int:id>', methods=['GET', 'POST'])
def account_edit_news(id):
    # verifica se a notícia existe
    data = classes.News.get_new_byid(id)

    if data is not None:
        # verifica se o usuário está logado
        if session.get('username'):

            # obtém os dados do usuário
            user = classes.User.get_user(session['username'])

            form = forms.NewsForm()
            if request.method == 'GET':
                form.title.data = data[2]
                form.description.data = data[3]
                form.message.data = data[4]

            # verifica se o usuário é admin
            if user[2] > 0:

                # instancia os objetos que precisam ser enviado a view
                last_logon = classes.Login.get_last_logon(session['username'])

                if request.method == 'POST':

                    # valida o formulário
                    if form.validate_on_submit():
                        classes.News.update_news_byid(
                            session['username'], data[0], form.title.data, form.description.data, form.message.data)
                        flash(u'Notícia editada com sucesso!',
                              category='success')
                    else:
                        flash(
                            u'Foram encotrados erros no preenchimento do formulário, verifique os campos em vermelho!', category='danger')

                return render_template('profile/news/edit_news.html', last_logon=last_logon, user=user, form=form, data=data)
            else:
                return redirect(url_for('profile'))
        else:
            return abort(403)
    else:
        return abort(404)


@app.route('/usuario/noticias/adicionar/', methods=['GET', 'POST'])
def account_add_news():

    # verifica se o usuário está logado
    if session.get('username'):

        # obtém os dados do usuário
        user = classes.User.get_user(session['username'])

        form = forms.NewsForm()
        # verifica se o usuário é admin
        if user[2] > 0:

            # instancia os objetos que precisam ser enviado a view
            last_logon = classes.Login.get_last_logon(session['username'])

            if request.method == 'POST':

                # valida o formulário
                if form.validate_on_submit():
                    classes.News.create_news(
                        form.title.data, form.description.data, form.message.data, session['username'])
                    flash(u'Notícia adicionada com sucesso!', category='success')
                else:
                    flash(
                        u'Foram encotrados erros no preenchimento do formulário, verifique os campos em vermelho!', category='danger')

            return render_template('profile/news/add_news.html', last_logon=last_logon, user=user, form=form)
        else:
            return redirect(url_for('profile'))
    else:
        return abort(403)


@app.route('/launcher/update/', defaults={'req_path': ''})
@app.route('/launcher/update/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = os.path.join(app.root_path, 'static/launcher/update')

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('update.html', files=files)


@app.route('/launcher/')
def launcher_home():
    return render_template('launcher.html', news=classes.News.get_news())


if __name__ == '__main__':
    app.run(debug=config.WEB_DEBUG, host=config.WEB_HOST, port=config.WEB_PORT)
