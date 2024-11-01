from flask import Flask, render_template, redirect, url_for, jsonify, request, abort, send_from_directory, current_app
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from PIL import Image
from shutil import copyfile
import json
import logging
import sys
import stripe
import os

application = Flask(__name__)

application.logger.addHandler(logging.StreamHandler(sys.stdout))
application.logger.setLevel(logging.ERROR)

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = ''
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
application.config['STRIPE_PUBLIC_KEY'] = ''
application.config['STRIPE_SECRET_KEY'] = ''
application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_USERNAME'] = ''
application.config['MAIL_PASSWORD'] = ''
application.config['MAIL_PORT'] = 465
application.config['MAIL_USE_SSL'] = True
application.config['MAIL_USE_TLS'] = False
application.config['DOWNLOAD_FOLDER'] = 'static/images/artpieces_original'
application.config['UPLOAD_FOLDER'] = 'static/images/artpieces_original'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

mail = Mail(application)

s = URLSafeTimedSerializer(application.config['SECRET_KEY'])

Bootstrap(application)
db = SQLAlchemy(application)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'index'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    confirmed = db.Column(db.Boolean, unique=False)


class Artpieces(db.Model):
    filename = db.Column(db.String(50), primary_key=True)
    displayname = db.Column(db.String(50), unique=False)
    madeby = db.Column(db.String(50), unique=False)
    ownedby = db.Column(db.String(50), unique=False)
    price = db.Column(db.Integer, unique=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    loginUsername = StringField('username', validators=[
                                InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=24)])
    remember = BooleanField('remember me')


class SignupForm(FlaskForm):
    signupUsername = StringField('username', validators=[
                                 InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=24)])


stripe.api_key = application.config['STRIPE_SECRET_KEY']


@application.route('/', methods=['GET', 'POST'])
def index():
    loginform = LoginForm()
    signupform = SignupForm()

    artpieces = Artpieces.query.all()

    if loginform.loginUsername.data and loginform.validate():

        user = User.query.filter_by(
            username=loginform.loginUsername.data).first()
        if user and check_password_hash(user.password, loginform.password.data):

            login_user(user, remember=loginform.remember.data)
            return redirect(url_for('profilepage'))

        return redirect(url_for('errorpage', info='invalidusrps'))

    if signupform.signupUsername.data and signupform.validate():

        # HASH THE PASSWORD
        hashed_password = generate_password_hash(
            loginform.password.data, method='sha256')

        # TRY ADDING IN DATABASE
        new_user = User(username=signupform.signupUsername.data,
                        email=signupform.email.data, password=hashed_password, confirmed=False)

        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            return redirect(url_for('errorpage', info='cantimport'))

        # SEND CONFIRMATION EMAIL
        emailaddress = signupform.email.data
        token = s.dumps(emailaddress, salt='email-confirm')

        msg = Message(
            'Confirm Email', sender='vineetnitinpatil@gmail.com',  recipients=[emailaddress])

        link = url_for('confirm_email', token=token, _external=True)

        msg.body = 'Your confirmation link is {}'.format(link)

        mail.send(msg)

        # REDIRECT TO INDEX PAGE
        return redirect(url_for('index'))

    return render_template('index.html', loginform=loginform, signupform=signupform, artpieces=artpieces)


@application.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=60 * 60)
    except SignatureExpired:
        return redirect(url_for('errorpage', info='tokenexpired'))

    user = User.query.filter_by(email=email).first()

    user.confirmed = True
    db.session.commit()

    return redirect(url_for('errorpage', info='emailconfirmed'))


@application.route('/sendauthenticationemail')
@login_required
def send_confirm_email():
    emailaddress = current_user.email
    token = s.dumps(emailaddress, salt='email-confirm')

    msg = Message('Confirm Email', sender='vineetnitinpatil@gmail.com',
                  recipients=[emailaddress])

    link = url_for('confirm_email', token=token, _external=True)

    msg.body = 'Your confirmation link is {}'.format(link)

    mail.send(msg)

    print('email sent')

    return {}


@application.route('/profile')
@login_required
def profilepage():
    loginform = LoginForm()
    signupform = SignupForm()
    ownedartpieces = Artpieces.query.filter_by(ownedby=current_user.username)
    createdartpieces = Artpieces.query.filter_by(madeby=current_user.username)

    return render_template('profile.html', loginform=loginform, signupform=signupform, username=current_user.username, ownedartpieces=ownedartpieces, createdartpieces=createdartpieces)


@application.route('/profile/<username>')
def otherprofilepage(username):

    user = User.query.filter_by(username=username).first()

    if(not user):
        return redirect(url_for('errorpage', info='nouser'))

    loginform = LoginForm()
    signupform = SignupForm()

    ownedartpieces = Artpieces.query.filter_by(ownedby=username)
    createdartpieces = Artpieces.query.filter_by(madeby=username)

    return render_template('profile.html', loginform=loginform, signupform=signupform, username=username, ownedartpieces=ownedartpieces, createdartpieces=createdartpieces)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/artworks/<artname>')
def artpage(artname):

    loginform = LoginForm()
    signupform = SignupForm()
    artpiece = Artpieces.query.filter(
        Artpieces.filename.startswith(artname)).first()

    return render_template('artpage.html',
                           artname=artpiece.filename,
                           loginform=loginform,
                           signupform=signupform,
                           artpiece=artpiece
                           )


@application.route('/buyartpiece', methods=['POST'])
@login_required
def buyartpiece():

    if current_user.confirmed == False:
        return {}

    artname = request.form['artname']

    art = Artpieces.query.filter(
        Artpieces.filename.startswith(artname)).first()
    if (art.ownedby):
        url = url_for('artpage', artname=artname)
        print(url)
        return jsonify(url=url)

    print('creating')
    customer = stripe.Customer.create(
        email=current_user.email,
        name=request.form['firstname'] + ' ' + request.form['lastname'],
        address={
            'line1': request.form['addressline1'],
            'postal_code': request.form['postalcode'],
            'city': request.form['city'],
            'state': request.form['state'],
            'country': request.form['country'],
        },
    )

    intent = stripe.PaymentIntent.create(
        amount=art.price * 100,
        currency='usd',
        description='Bought artpiece ' + artname,
        customer=customer,
        metadata={
            'integration-check': 'accept_a_payment',
            'username': current_user.username,
            'artpiecefilename': artname,
        },
    )

    return jsonify(client_secret=intent.client_secret)


@application.route('/infopage/<info>')
def errorpage(info):
    loginform = LoginForm()
    signupform = SignupForm()

    message = ''

    if info == 'emailnotconfirmed':
        message = 'Please confirm your email'
    elif info == 'emailconfirmed':
        message = 'Email confirmed'
    elif info == 'invalidusrps':
        message = 'Invalid username or password'
    elif info == 'nouser':
        message = 'User doesnt exist'
    elif info == 'cantimport':
        message = 'Please enter unique username and email'
    elif info == 'tokenexpired':
        message = 'Email token expired, please get a new one'
    elif info == 'imagenotfound':
        message = 'Image not found'
    elif info == 'error':
        message = 'Something went wrong'

    return render_template('infopage.html', loginform=loginform, signupform=signupform, message=message)


@application.route('/download/<path:imagename>')
@login_required
def downloadimage(imagename):
    art = Artpieces.query.filter(Artpieces.filename.startswith(imagename)).first()

    if not art:
        return redirect(url_for('errorpage', info = 'imagenotfound'))

    if art.ownedby != current_user.username:
        return redirect(url_for('errorpage', info = 'imagenotfound'))

    path = os.path.join(current_app.root_path, application.config['DOWNLOAD_FOLDER'])
    
    return send_from_directory(directory=path, path=art.filename)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/upload', methods=['POST'])
@login_required
def uploadart():
    if not current_user.confirmed:
        return redirect(url_for('errorpage', info='emailnotconfirmed'))
    if not request.files['file']:
        return redirect(url_for('errorpage', info='error'))
    
    file = request.files['file']
    displayname = request.form['displayname']
    price = request.form['price']

    if file.filename == '':
        return redirect(url_for('errorpage', info='error'))
    
    if file and allowed_file(file.filename):

        print(file.filename)
        print(displayname)
        print(price)
        filename = secure_filename(file.filename)

        art = Artpieces(filename=filename, displayname=displayname, madeby=current_user.username, ownedby=None, price=price)
        db.session.add(art)

        try:
            db.session.commit()
        except:
            return redirect(url_for('errorpage', info='error'))
        
        
        print(filename)
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))

        if '.gif' in filename:
            copyfile(application.config['UPLOAD_FOLDER'] + '/' + filename, 'static/images/artpieces_thumb/' + filename)
        else:
            foo = Image.open(application.config['UPLOAD_FOLDER'] + '/' + filename)
            # foo = foo.resize((int(foo.size[0]/2), int(foo.size[1]/2)), Image.LANCZOS)
            # foo.save('static/images/artpieces_thumb/' + filename, optimize=True, quality=90)
            foo = foo.resize((int(foo.size[0]), int(foo.size[1])), Image.LANCZOS)
            foo.save('static/images/artpieces_thumb/' + filename, optimize=True, quality=100)
    
    
    return redirect(url_for('profilepage'))



@application.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object

        artname = payment_intent.metadata.artpiecefilename
        username = payment_intent.metadata.username

        print(artname)
        print(username)

        art = Artpieces.query.filter(
            Artpieces.filename.startswith(artname)).first()
        art.ownedby = username
        db.session.commit()
    
    if event.type == 'payment_intent.requires_action':
        print('WEBHOOK SUCCESSFUL TEST')

    return {}


if __name__ == '__main__':
    application.debug = True
    application.run()
