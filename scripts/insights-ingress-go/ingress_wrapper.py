import json
import os
from base64 import b64encode
from urllib.parse import urljoin
from uuid import uuid4

import requests
from flask import Flask
from flask import Response as FlaskResponse
from flask import request as flask_request

DEFAULT_RH_IDENTITY = {
    "identity": {
        "account_number": "00001",
        "auth_type": "cert-auth",
        "internal": {"org_id": "00001"},
        "system": {"cert_type": "system", "cn": str(uuid4())},
        "type": "System",
    }
}
DEFAULT_RH_REQUEST_ID = "test"

INGRESS_URL = os.getenv("INGRESS_URL", "http://localhost:8080")

app = Flask("ingress-wrapper")


@app.route("/api/ingress/v1/upload", methods=["POST"])
def ingress_wrapper():
    """Add internal RH headers to a request and make a call to ingress."""
    app.logger.info("Preparing request for ingress...")
    headers = _prepare_headers(flask_request.headers)
    files = _convert_flask_files_to_requests_files(flask_request.files)

    app.logger.info(f"Pushing data to ingress url {INGRESS_URL}")
    ingress_response = requests.post(
        urljoin(INGRESS_URL, flask_request.path),
        headers=headers,
        files=files,
    )
    app.logger.info(f"Response from ingress: {ingress_response.text}")
    app.logger.info(f"Status code: {ingress_response.status_code}")
    return FlaskResponse(
        ingress_response.content,
        status=ingress_response.status_code,
        headers=dict(ingress_response.headers),
    )


def _encode_rh_identity(data: dict):
    return b64encode(json.dumps(data).encode())


def _convert_flask_files_to_requests_files(request_files):
    return {
        file_key: (
            file_object.filename,
            file_object.stream,
            file_object.mimetype,
        )
        for file_key, file_object in request_files.items()
    }


def _prepare_headers(original_headers):
    x_rh_headers = {
        "x-rh-identity": _encode_rh_identity(DEFAULT_RH_IDENTITY),
        "x-rh-request_id": DEFAULT_RH_REQUEST_ID,
    }
    headers = dict(original_headers, **x_rh_headers)
    # flask host - let requests fill with the appropriate value
    headers.pop("Host")
    # requests will create content-type/length based on files dict
    headers.pop("Content-Type")
    headers.pop("Content-Length")
    return headers
