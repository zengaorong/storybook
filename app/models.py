#coding=utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
from . import db, login_manager
from datetime import datetime


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.username

class Manhua(UserMixin,db.Model):
    __tablename__ = 'mhname'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    mhname = db.Column(db.String(64), unique=True)
    pic_url = db.Column(db.String(128), unique=True)
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    pic_base64data = db.Column(db.Text())

    #users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Manhua %r>' % self.mhname

class Chapter(UserMixin,db.Model):
    __tablename__ = 'mhchapter'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    mhname_id = db.Column(db.VARCHAR(36), db.ForeignKey('mhname.id'))
    data = db.Column(db.Text())
    chapter_nums = db.Column(db.Integer)
    pics_nums = db.Column(db.Integer)
    chapter_name = db.Column(db.String(64))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)

    db.UniqueConstraint(mhname_id,chapter_name)
    #users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<mhchapter %r>' % self.chapter_name



class Worker(db.Model):
    __tablename__ = 'worker'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    workername = db.Column(db.String(64))
    account = db.Column(db.VARCHAR(36))
    password = db.Column(db.VARCHAR(36))
    def __repr__(self):
        return '<worker %r>' % self.workername

class Logbook(db.Model):
    __tablename__ = 'Logbook'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    workerid = db.Column(db.VARCHAR(36), db.ForeignKey('worker.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    logbook_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    log_type = db.Column(db.VARCHAR(1))

    def __repr__(self):
        return '<Logbook %r>' % self.work_for


class Watcher(db.Model):
    __tablename__ = 'watcher'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watchernum = db.Column(db.VARCHAR(5))
    watchername = db.Column(db.String(64))
    watchertown = db.Column(db.String(5))
    watchertype = db.Column(db.String(5))
    watcherserverip = db.Column(db.String(64))
    watcherip = db.Column(db.String(64))
    watcherlongitude = db.Column(db.DECIMAL(10,6))
    watcherlatitude = db.Column(db.DECIMAL(10,6))
    account = db.Column(db.VARCHAR(36))
    password = db.Column(db.VARCHAR(36))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

class Wterror(db.Model):
    __tablename__ = 'wterror'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watcher_id = db.Column(db.VARCHAR(36),db.ForeignKey('watcher.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    erro_type = db.Column(db.VARCHAR(5))
    log_type = db.Column(db.VARCHAR(1))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

class Wtdel(db.Model):
    __tablename__ = 'wtdel'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watcher_id = db.Column(db.VARCHAR(36),db.ForeignKey('watcher.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    erro_type = db.Column(db.VARCHAR(5))
    log_type = db.Column(db.VARCHAR(1))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

class Story(db.Model):
    __tablename__ = 'story'
    story_id = db.Column(db.VARCHAR(36), primary_key=True)
    story_url = db.Column(db.String(64), unique=True)
    story_name = db.Column(db.String(128), unique=True)
    story_intro = db.Column(db.Text())
    author = db.Column(db.String(128))
    story_last_chapter_url = db.Column(db.String(128))
    story_last_chapter_name = db.Column(db.String(128))
    story_type = db.Column(db.Integer)
    chapter_num = db.Column(db.Integer)
    image_data = db.Column(db.Text())

    #users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Story %r>' % self.story_name

# 考虑的问题 是否使用ssdb来处理会更好 没有一致性的排序 会使得查询时间非常长 是否隔一段时间 执行排序的操作
#  chapter_id,story_id,chapter_num,chapter_name,chapter_url,chapter_text
class StoryChapter(db.Model):
    __tablename__ = 'storyChapter'
    chapter_id = db.Column(db.VARCHAR(36), primary_key=True)
    story_id = db.Column(db.VARCHAR(36), db.ForeignKey('story.story_id'))
    chapter_num = db.Column(db.Integer)
    chapter_name = db.Column(db.String(128))
    chapter_url = db.Column(db.String(128))
    chapter_text = db.Column(db.Text())
    chapter_order = db.Column(db.Integer)

    def __repr__(self):
        return '<StoryChapter %r>' % self.chapter_name



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
