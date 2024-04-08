from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdasdsa'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # no prefox for both
    app.register_blueprint(auth, url_prefix='/')
    return app


