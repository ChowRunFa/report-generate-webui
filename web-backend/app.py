from flask import Flask
from flask_docs import ApiDoc

from gevent import pywsgi

from flask_cors import CORS
from db.models import *
from db.dbServer import MySQLConfig
app = Flask(__name__)
ApiDoc(
    app,
    title="Sample App",
    version="1.0.0",
    description="A simple app API",
)

app.config.from_object(MySQLConfig)
# app.config['SECRET_KEY']
with app.app_context():
    db.init_app(app)
    db.create_all()


from api.api_upload import api_upload
from api.api_report import api_report
from api.api_llm import api_llm
from api.api_relatedwork import api_relatedwork
app.register_blueprint(api_upload, url_prefix="")
app.register_blueprint(api_report, url_prefix="")
app.register_blueprint(api_llm, url_prefix="")
app.register_blueprint(api_relatedwork, url_prefix="")


cors = CORS(app, resources={r"/*": {"origins": "*"}}) # 注册CORS, "/*" 允许访问所有api


if __name__ == "__main__":
    app.run()


