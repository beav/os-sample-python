import os

from flask import Flask, request, current_app, abort
application = Flask(__name__)


@application.route("/")
def hello():
    return "XHello World!X"

@application.route("/endpoint", methods=['POST'])
def endpoint():
    token = os.getenv("SECRET_TOKEN")
    header_token = request.headers["X-Insight-Token"]
    current_app.logger.warn(request.headers) 
    if token != header_token:
        current_app.logger.warn("token %s does not match header %s" % (token, header_token))
        abort(403)
    if request.is_json:
        json_data = request.get_json()
        current_app.logger.warn(json_data['context']['inventory_id'])
    return "XHello World!X"

if __name__ == "__main__":
    application.run()
