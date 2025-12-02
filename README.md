# ElGamal Encryption API

A simple web application to encrypt and decrypt messages using the ElGamal algorithm.

## Features

- Generate public and private keys
- Encrypt messages
- Decrypt messages
- Test the functionality in a web interface

## Tech Stack

- Python 3.12
- FastAPI
- PyCryptodome
- Pydantic
- HTML/JS frontend

## Setup

1. Clone the repository

git clone <repository_url>
cd encrypt_api


## Create and activate virtual environment

python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac


## Install dependencies

pip install -r requirements.txt


## Run the server

python -m uvicorn main:app --reload


## Open in browser

http://127.0.0.1:8000


## Use the web interface to generate keys, encrypt, and decrypt messages.

## Run Python test:

python test_elgamal.py