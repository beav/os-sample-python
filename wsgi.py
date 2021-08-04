from flask import Flask, request, current_app
application = Flask(__name__)

@application.route("/")
def hello():
    return "XHello World!X"

@application.route("/endpoint", methods=['POST'])
def endpoint():
    current_app.logger.warn(request.headers) 
    if request.is_json:
        json_data = request.get_json()
        current_app.logger.warn(json_data)
    return "XHello World!X"

if __name__ == "__main__":
    application.run()
