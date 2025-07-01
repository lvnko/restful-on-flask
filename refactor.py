from flask import Flask, jsonify, g, session
from utils.Performance import Performance
from v1 import v1_bp
from v2 import v2_bp
import uuid, time, datetime

app = Flask("myapp", template_folder="./templates")
app.config.from_object('config.DevelopmentConfig')
app.config["SECRET_KEY"] = "wow_unique_key"
# app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(seconds=5)
performance = Performance("logs/performance.csv")

@app.before_request
def preprocess():
    print(session)
    g.uuid = uuid.uuid4()
    g.conn = { "is_connected": True }
    g.start = time.time()

@app.after_request
def postprocess(response):
    g.conn["is_connected"] = False
    g.end = time.time()
    g.status_code = response.status_code
    performance.log(g)
    return response

@app.teardown_request
def teardown_process(error):
    g.conn["is_connected"] = False
    if error is not None:
        app.logger.error(f"user-{g.uuid} has triggered an error: {error}")

app.register_blueprint(v1_bp, url_prefix="/v1")
app.register_blueprint(v2_bp, url_prefix="/v2")

if __name__ == '__main__':
    # print(app.url_map)
    app.run(port=8081)