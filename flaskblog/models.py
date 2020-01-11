from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Stud(db.Model):
    __tablename__ = 'Student'
    __table_args__ = {'sqlite_autoincrement': True}
    ID = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(30))
    student_dob = db.Column(db.DateTime,nullable=False)
    student_address_line1 = db.Column(db.String(100))
    student_address_landmark = db.Column(db.String(30))
    student_date_of_addmission = db.Column(db.DateTime,nullable=False)
    file = db.Column(db.Binary,nullable=False)
    def __init__(self,Id,sname,sdob,saddress,slandmark,saddmission,file):
        # super(Stud, self).__init__(sname,sdob,saddress,slandmark,saddmission,file)
        self.ID=Id
        self.student_name = sname
        self.student_dob = sdob
        self.student_address_line1 = saddress
        self.student_address_landmark = slandmark
        self.student_date_of_addmission = saddmission
        self.file = file