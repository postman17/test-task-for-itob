from flask import render_template, request, redirect, Response
from flask_login import (
    current_user,
    LoginManager,
    login_user,
    logout_user,
    login_required
)
from forms import LoginForm, RegistrationForm, ConsignorTaskForm
from app import (
    app,
    db,
    User,
    Purse,
    Task,
    CarrierTask,
    ConsignorTask,
    Commission
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Start and login page."""
    if current_user.is_authenticated and current_user.is_carrier():
        return redirect('/carrier')
    elif current_user.is_authenticated and current_user.is_consignor():
        return redirect('/consignor')

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            login_user(user)

        if user.is_carrier():
            return redirect('/carrier')
        elif user.is_consignor():
            return redirect('/consignor')

    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        purse = Purse(amount=0)
        user = User(
            email=request.form.get('email'),
            occupation_id=request.form.get('occupation'),
            purse=purse
        )
        user.set_password(request.form.get('password'))
        db.session.add(purse)
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Logout view."""
    logout_user()

    return redirect('/')


@app.route('/carrier', methods=['GET', 'POST'])
@login_required
def carrier():
    """Carrier view."""
    if not current_user.is_carrier():
        return redirect('/')

    if request.method == 'POST':
        response_data = request.json
        task = Task.query.filter_by(id=response_data.get('task_id')).first()
        task.is_work = True
        carrier_task = CarrierTask(
            user_id=current_user.id,
            task_id=task.id
        )
        commissions = Commission.query.order_by(Commission.id.desc()).first()
        purse = current_user.purse
        purse.amount += task.price - commissions.amount
        db.session.add(task)
        db.session.add(purse)
        db.session.add(carrier_task)
        db.session.commit()

        return Response('OK', 200)

    carrier_tasks = CarrierTask.query.filter_by(user_id=current_user.id)
    free_tasks = Task.query.filter_by(is_work=False).all()

    return render_template('carrier.html', carrier_tasks=carrier_tasks, free_tasks=free_tasks)


@app.route('/consignor', methods=['GET', 'POST'])
@login_required
def consignor():
    """Consignor view."""
    if not current_user.is_consignor():
        return redirect('/')

    form = ConsignorTaskForm()
    if request.method == 'POST' and form.validate_on_submit():
        comment = request.form.get('comment')
        price = request.form.get('price')
        task = Task(
            comment=comment,
            price=price
        )
        consignor_task = ConsignorTask(
            user=current_user,
            task=task
        )
        db.session.add(task)
        db.session.add(consignor_task)
        db.session.commit()

    consignor_tasks = ConsignorTask.query.filter_by(user_id=current_user.id)
    return render_template('consignor.html', form=form, consignor_tasks=consignor_tasks)


if __name__ == "__main__":
    app.run()
