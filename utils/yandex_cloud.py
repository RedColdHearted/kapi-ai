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
    """Represent dataclass of YC service-account credentials."""

    private_key: str
    key_id: str
    service_account_id: str


@dataclasses.dataclass(frozen=True)
class JWTPayload:
    """Represent dataclass of JWT payload for YC se-account."""

    aud: str
    iss: str
    iat: float
    exp: float


def _read_credentials() -> SEAccountCredentials:
    """Read and return se-account keys from json file."""
    with open(YC_SE_ACCOUNT_CREDENTIALS, "r") as credentials_file:
        obj = json.load(credentials_file)
        return SEAccountCredentials(
            private_key=obj["private_key"],
            key_id=obj["id"],
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
    payload = _create_payload(credentials.service_account_id)

    response = requests.post(
        YC_IAM_TOKEN_URL,
        json={
            "jwt": jwt.encode(
                payload={
                    "aud": payload.aud,
                    "iss": payload.iss,
                    "iat": payload.iat,
                    "exp": payload.exp,
                },
                key=credentials.private_key,
                algorithm=JWT_ALGORITHM,
                headers={"kid": credentials.key_id},
            ),
        },
        headers={
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()

    return response.json()["iamToken"]