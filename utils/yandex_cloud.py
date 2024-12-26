import time
import json
import dataclasses

import requests
import jwt

YC_SE_ACCOUNT_CREDENTIALS = "authorized_key.json"
JWT_ALGORITHM = "PS256"
YC_IAM_TOKEN_URL = (
    "https://iam.api.cloud.yandex.net/iam/v1/tokens"
)


@dataclasses.dataclass(frozen=True)
class SEAccountCredentials:
    private_key: str
    key_id: str
    service_account_id: str


@dataclasses.dataclass(frozen=True)
class JWTPayload:
    aud: str
    iss: str
    iat: float
    exp: float


def _read_credentials() -> SEAccountCredentials:
    """Read and return se-account keys from json file."""
    with open(YC_SE_ACCOUNT_CREDENTIALS, "r") as credentials_file:
        obj = credentials_file.read()
        obj = json.loads(obj)
        return SEAccountCredentials(
            private_key=["private_key"],
            key_id = obj["id"],
            service_account_id=obj["service_account_id"],
        )

def _create_payload(service_account_id: str) -> JWTPayload:
    """Create and return payload for jwt to iam token exchange."""
    now = int(time.time())
    return JWTPayload(
        aud=YC_IAM_TOKEN_URL,
        iss=service_account_id,
        iat=now,
        exp=now + 3600
    )

def get_yc_iam_token() -> str:
    """Return Yandex Cloud service-account IAM token.

    Provides IAM token by exchange JWT from encoded credentials of
    service account stored in json file.

    """
    credentials = _read_credentials()

    response = requests.post(
        YC_IAM_TOKEN_URL,
        json={
            "jwt": jwt.encode(
                payload=_create_payload(credentials.service_account_id),
                key=credentials.private_key,
                algorithm=JWT_ALGORITHM,
                headers={"kid": credentials.key_id}
            ),
        },
        headers={
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()

    return response.json()["iamToken"]