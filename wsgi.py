from flask import Flask, request, current_app
application = Flask(__name__)

@application.route("/")
def hello():
    return "XHello World!X"

@application.route("/endpoint")
def endpoint():
    current_app.logger.warn("foo") 
    return "XHello World!X"

if __name__ == "__main__":
    application.run()
