from pydantic import BaseModel
from typing import List


class PublicKey(BaseModel):
    p: str
    g: str
    y: str


class EncryptedChunk(BaseModel):
    c1: str
    c2: str


class EncryptRequest(BaseModel):
    message: str
    public_key: PublicKey


class EncryptResponse(BaseModel):
    encrypted_chunks: List[EncryptedChunk]
    public_key: PublicKey
    private_key: str


class DecryptRequest(BaseModel):
    encrypted_chunks: List[EncryptedChunk]
    public_key: PublicKey
    private_key: str


class DecryptResponse(BaseModel):
    message: str
