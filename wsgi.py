import os

import requests
import json

from string import Template

from flask import Flask, request, current_app, abort
from kafka import KafkaProducer

application = Flask(__name__)

TOKEN_URL = (
    "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
)
CVES_FOR_SYSTEM = Template(
    "https://cloud.redhat.com/api/vulnerability/v1/systems/$inventory_id/cves"
)


producer = KafkaProducer(
    api_version_auto_timeout_ms=10000,
    sasl_mechanism="PLAIN",
    security_protocol="SASL_SSL",
    bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVER")],
    sasl_plain_username=os.getenv("KAFKA_USERNAME"),
    sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
)


def get_short_token(long_token):
    payload = {
        "grant_type": "refresh_token",
        "client_id": "rhsm-api",
        "refresh_token": long_token,
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    short_token = response.json().get("access_token")
    return short_token


def get_cves_for_system(st, inventory_id):
    headers = {"Authorization": f"Bearer {st}"}
    response = requests.get(
        CVES_FOR_SYSTEM.substitute(inventory_id=inventory_id), headers=headers
    )
    response.raise_for_status()
    return response.json().get("data")


def publish_data(data):
    binary_data = json.dumps(data).encode()
    producer.send("myevents", binary_data)


@application.route("/")
def hello():
    return "XHello World!X"


@application.route("/endpoint", methods=["POST"])
def endpoint():
    token = os.getenv("SECRET_TOKEN")
    short_api_token = get_short_token(os.getenv("LONG_TOKEN"))
    header_token = request.headers["X-Insight-Token"]
    current_app.logger.warn(request.headers)
    if token != header_token:
        current_app.logger.warn(
            "token %s does not match header %s" % (token, header_token)
        )
        abort(403)
    if not request.is_json:
        abort(500)

    json_data = request.get_json()
    inv_id = json_data.get("context").get("inventory_id")

    short_token = get_short_token(os.getenv("LONG_TOKEN"))
    cves = get_cves_for_system(short_token, inv_id)

    publish_data(cves)

    return "XHello World!X"


if __name__ == "__main__":
    application.run()
