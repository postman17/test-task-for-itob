import enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from werkzeug.security import generate_password_hash,  check_password_hash

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '3f4n934f9834fn99f4j983jf98j3fj9834f98j34fj9j98jg989898g9898g98g98g89g89'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class Occupation(db.Model):
    """Occupation table."""

    __tablename__ = 'occupation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f'<occupation {self.id}>'


class Purse(db.Model):
    """Purse table for carriers."""

    __tablename__ = 'purse'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=2))

    def __repr__(self):
        return f'<purse {self.id}>'


class Commission(db.Model):
    """Commission for carrier tasks."""

    __tablename__ = 'commissions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=2))

    def __repr__(self):
        return f'<commission {self.id}>'


class User(db.Model):
    """Users model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500))
    occupation_id = db.Column(db.Integer, db.ForeignKey('occupation.id'))
    occupation = db.relationship('Occupation', backref='occupation_user')
    purse_id = db.Column(db.Integer, db.ForeignKey('purse.id'))
    purse = db.relationship('Purse', backref='purse_user')

    def __repr__(self):
        return f'<user {self.id}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            'email': self.email
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_carrier(self):
        return True if self.occupation.name == 'Carrier' else False

    def is_consignor(self):
        return True if self.occupation.name == 'Consignor' else False

    def get_id(self):
        return str(self.id)


class TaskStatusEnum(enum.Enum):
    awaiting = 'awaiting'
    in_progress = 'in progress'
    success = 'success'


class Task(db.Model):
    """Tasks table."""

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    status = db.Column(
        db.Enum(TaskStatusEnum),
        default=TaskStatusEnum.awaiting,
        nullable=False
    )
    price = db.Column(db.Numeric(precision=2))
    is_work = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return f'<task {self.id}>'


class CarrierTask(db.Model):
    """Keep carriers in progress ans success tasks."""

    __tablename__ = 'carriers_tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='carrier_task_user')
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task = db.relationship('Task', backref='carrier_task')

    def __repr__(self):
        return f'<carrier_task {self.id}>'


class ConsignorTask(db.Model):
    """Keep carriers in progress ans success tasks."""

    __tablename__ = 'consignors_tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='consignor_task_user')
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task = db.relationship('Task', backref='consignor_task')

    def __repr__(self):
        return f'<consignor_task {self.id}>'


if __name__ == "__main__":
    manager.run()
