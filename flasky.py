import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role
import platform
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)




@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


sysstr = platform.system()
if(sysstr =="Windows"):
    app.run(host='127.0.0.1',port=8085,debug=True)
if(sysstr == "Linux"):
    pass