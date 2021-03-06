#coding=utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import flask_excel as excel

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
photos = UploadSet('photos', IMAGES)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    # 前面的storybook是项目中 的 文件路径的上级目录  后面的是文件目录的名称
    app = Flask(__name__,static_folder='storybook', static_url_path='/storybook')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    excel.init_excel(app)
    db.init_app(app)
    login_manager.init_app(app)

    configure_uploads(app, photos)
    patch_request_class(app)  # set maximum file size, default is 16MB

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/myflask/auth')

    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint, url_prefix='/storybook/search')

    from .story import story as story_blueprint
    app.register_blueprint(story_blueprint, url_prefix='/storybook/story')

    return app
