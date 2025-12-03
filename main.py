from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from typing import List

from models import (
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
    PublicKey,
    EncryptedChunk
)

from elgamal_utils import generate_keys, encrypt_message, decrypt_message


app = FastAPI(
    title="ElGamal Encryption API",
    description="Fast and optimized chunked ElGamal encryption service",
    version="1.0.0"
)

# Статика (фронтенд)
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------------
# Отдаём index.html (главная страница)
# -------------------------------------
@app.get("/")
def root():
    return FileResponse("static/index.html")


# -----------------------------
# Generate keys
# -----------------------------
@app.get("/generate_keys", response_model=dict)
def api_generate_keys(bits: int = 128):
    public_key, private_key = generate_keys(bits)

    return {
        "public_key": {
            "p": str(public_key["p"]),
            "g": str(public_key["g"]),
            "y": str(public_key["y"])
        },
        "private_key": str(private_key)
    }


# -----------------------------
# Encrypt
# -----------------------------
@app.post("/encrypt", response_model=EncryptResponse)
def api_encrypt(request: EncryptRequest):

    message_bytes = request.message.encode()

    encrypted = encrypt_message(
        message_bytes,
        {
            "p": int(request.public_key.p),
            "g": int(request.public_key.g),
            "y": int(request.public_key.y),
        }
    )

    encrypted_chunks = [
        EncryptedChunk(c1=str(c1), c2=str(c2))
        for c1, c2 in encrypted
    ]

    return EncryptResponse(
        encrypted_chunks=encrypted_chunks,
        public_key=request.public_key,
        private_key="HIDDEN"
    )


# -----------------------------
# Decrypt
# -----------------------------
@app.post("/decrypt", response_model=DecryptResponse)
def api_decrypt(request: DecryptRequest):

    encrypted_chunks = [(int(c.c1), int(c.c2)) for c in request.encrypted_chunks]

    decrypted_bytes = decrypt_message(
        encrypted_chunks,
        {
            "p": int(request.public_key.p),
            "g": int(request.public_key.g),
            "y": int(request.public_key.y),
        },
        int(request.private_key)
    )

    return DecryptResponse(message=decrypted_bytes.decode("utf-8"))
