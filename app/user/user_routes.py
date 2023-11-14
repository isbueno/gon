from flask import Blueprint, redirect, render_template, request, url_for, flash, session
user_blueprint = Blueprint('user_blueprint', __name__, template_folder="templates")


from app import app, db

from flask_bcrypt import Bcrypt
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

from app.models.User import User
from app.models.Student import Student
from app.models.Address import Address
from app.models.Carpool import Carpool
from app.models.Vehicle import Vehicle
from app.models.Comment import Comment
from app.models.Uploads import Uploads

from app.forms import RegisterUserForm, RegisterAddressForm, RegisterVehicleForm, LoginForm, CommentForm, RegisterZone, RegisterSchool

import os
import base64


# Configurações de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_blueprint.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# passando usuário para a header
@app.context_processor
def inject_user():
    user = current_user
    return dict(user=user)

# Criptografia
bcrypt = Bcrypt(app)


# OPTIONS
@user_blueprint.route('/register-options')
def register_options():
    return render_template("register_options.html")


# REGISTER STUDENT
@user_blueprint.route('/register/student', methods=['GET', 'POST'])
def register_student():
    registerUserForm = RegisterUserForm()
    registerAddressForm = RegisterAddressForm()
    registerSchoolForm = RegisterSchool()

    if registerUserForm.validate_on_submit() and registerAddressForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerUserForm.password.data)

        email_form = registerUserForm.email.data

        new_address = Address(
            zipcode=registerAddressForm.zipcode.data,
            street=registerAddressForm.street.data,
            number=registerAddressForm.number.data,
            neighborhood=registerAddressForm.neighborhood.data,
            city=registerAddressForm.city.data,
            state=registerAddressForm.state.data
        )

        new_student = Student(
            username=registerUserForm.username.data,
            cpf=registerUserForm.cpf.data,
            birth=registerUserForm.birth.data,
            email=email_form,
            whatsapp=registerUserForm.whatsapp.data,
            password=hashed_password,
            address=new_address,
            school=registerSchoolForm.school.data,
            tipo="student"
        )

        # Verifica se o e-mail é único
        if User.verifyEmail(email_form) is not None:
            return redirect(url_for('user_blueprint.register_student'))
        else:
            # Adicionando a idade do usuário
            new_student.age = new_student.get_age(new_student.birth)
            
            # Adicionando usuário: Student
            new_student.registerUser()
            return redirect(url_for('user_blueprint.login'))
        
    return render_template("register_aluno.html", formUser=registerUserForm, formAddress=registerAddressForm, formSchool=registerSchoolForm)


# REGISTER CARPOOL
@user_blueprint.route('/register/carpool', methods=['GET', 'POST'])
def register_carpool():
    registerUserForm = RegisterUserForm()
    registerZoneForm = RegisterZone()
    registerVehicleForm = RegisterVehicleForm()

    if registerUserForm.validate_on_submit() and registerVehicleForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerUserForm.password.data)

        email_form = registerUserForm.email.data

        new_vihicle = Vehicle(
            model=registerVehicleForm.model.data,
            license_plate=registerVehicleForm.license_plate.data,
            type_vehicle=registerVehicleForm.type_vehicle.data,
            color=registerVehicleForm.color.data,
            number_seats=registerVehicleForm.number_seats.data,
            additional_features=registerVehicleForm.additional_features.data,
            notes=registerVehicleForm.notes.data
        )

        new_carpool = Carpool(
            username=registerUserForm.username.data,
            cpf=registerUserForm.cpf.data,
            birth=registerUserForm.birth.data,
            email=email_form,
            whatsapp=registerUserForm.whatsapp.data,
            password=hashed_password,
            zone=registerZoneForm.zone.data,
            vehicle=new_vihicle,
            tipo="carpool"
        )
    
        # Verifica se o e-mail é único
        if User.verifyEmail(email_form) is not None:
            return redirect(url_for('user_blueprint.register_carpool'))
        else:

            # Adicionando a idade do usuário
            new_carpool.age = new_carpool.get_age(new_carpool.birth)

            # Adicionando usuário: Carpool
            new_carpool.registerUser()
            return redirect(url_for('user_blueprint.login'))

    return render_template("register_carpool.html", formUser=registerUserForm, formZone=registerZoneForm, formVehicle=registerVehicleForm)


# LOGIN
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, loginForm.password.data):
                login_user(user)
                session['user_id'] = user.id
                return redirect(url_for('user_blueprint.my_profile', user_id=user.id))
        else:
            flash("User don't exist", 'danger')
            return redirect(url_for('user_blueprint.login'))

                
    return render_template("login.html", form=loginForm)

# LOGOUT
@user_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None) 
    return redirect(url_for('home'))

# DELETE USER
@user_blueprint.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    user = User.query.get(id)    
    if user:
        user.delete_user()
        return redirect(url_for('user_blueprint.login'))
    else:
        return "Usuário não encontrado", 404
    
# PROFILE PAGE
@user_blueprint.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    user = User.query.get(user_id)

    student = Student.query.get(user_id)
    carpool = Carpool.query.get(user_id)
    comments = user.get_comments()
    commentForm = CommentForm()

    if user == current_user:
        return redirect(url_for('user_blueprint.my_profile', user_id=user.id))

    if user is None:
        return render_template('404.html'), 404
    
    return render_template('profile.html', user=user, student=student, carpool=carpool, commentForm=commentForm, comments=comments)


# MY PROFILE PAGE
@user_blueprint.route('/my-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def my_profile(user_id):
    if current_user.id == user_id:

        if current_user.tipo == "student":
            student = Student.query.get(user_id)
            comments = student.get_comments()
            return render_template('profile_student.html', student=student, comments=comments)

        if current_user.tipo == "carpool":
            carpool = Carpool.query.get(user_id)
            comments = carpool.get_comments()
            return render_template('profile_carpool.html', carpool=carpool, comments=comments)
    else:
        return redirect(url_for('user_blueprint.login'))


# COMMENTS 
@user_blueprint.route('/comentar/<int:user_id>', methods=['POST'])
@login_required
def comentar(user_id):
    # Obtendo o ID do usuário logado (current_user)
    user = current_user
    user_id_logado = user.id
    user_nome_logado = user.username

    # Obtendo o ID do usuário NÃO logado
    user_id_perfil = user_id

    user_rating = request.form.get('rating')
    user_comment = request.form.get('comment_text')

    comment = Comment(
        user_docomment_id=user_id_logado,
        user_gotcomment_id=user_id_perfil,
        name=user_nome_logado,
        rating=user_rating,
        comment_text=user_comment
    )

    # Salvando comentário no banco de dados
    comment.doComment()

    return redirect(url_for('user_blueprint.profile', user_id=user_id_perfil))


# UPLOAD PICTURES
@user_blueprint.route('/uploads', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        file = request.files['file']
        
        upload = Uploads(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit() 

    uploads = Uploads.query.all()

    for upload in uploads:
        extension = upload.filename.split('.')[-1]
        data_base64 = base64.b64encode(upload.data).decode('utf-8')
        mime_type = f'image/{extension}'
        upload.data = f'data:{mime_type};base64,{data_base64}'

    return render_template('uploads.html', uploads=uploads)