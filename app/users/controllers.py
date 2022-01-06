from flask import Blueprint, json

from app.models import User, UserSchema

# Define the blueprint: 'users', set its url prefix: app.url/users
users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
def get_all_users():
    users = Us
    er.query.all()
    users_schema = UserSchema(many=True)
    return json.dumps(users_schema.dump(users))


@users.route('/<int:id>')
def get_user(id):
    user = User.query.get(id)
    user_schema = UserSchema()
    return user_schema.dump(user)

# @users.route('/new', methods=['POST'])
# def create_user():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form)
#         user.save()
#         # redirect('register')
#     return user

# Set the route and accepted methods
# @users.route('/signin/', methods=['GET', 'POST'])
# def signin():
#     # If sign in form is submitted
#     form = LoginForm(request.form)
#
#     # Verify the sign in form
#     if form.validate_on_submit():
#
#         user = User.query.filter_by(email=form.email.data).first()
#
#         if user and check_password_hash(user.password, form.password.data):
#             session['user_id'] = user.id
#
#             flash('Welcome %s' % user.name)
#
#             return redirect(url_for('auth.home'))
#
#         flash('Wrong email or password', 'error-message')
#
#     return render_template("auth/signin.html", form=form)
