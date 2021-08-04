from flask import Flask
application = Flask(__name__)

@application.route("/")
def hello():
    return "XHello World!X"

if __name__ == "__main__":
    application.run()
