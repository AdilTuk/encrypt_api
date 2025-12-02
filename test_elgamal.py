from elgamal_utils import generate_keys, encrypt_message, decrypt_message

message = b"Hello, this is a test message!"

print("1) Original:", message)

print("2) Generating keys...")
public_key, private_key = generate_keys()
print("   Public key:", public_key)
print("   Private key:", private_key)

print("3) Encrypting...")
encrypted = encrypt_message(message, public_key)
print("   Encrypted chunks:", encrypted)

print("4) Decrypting...")
decrypted = decrypt_message(encrypted, public_key, private_key)
print("   Decrypted:", decrypted)


if decrypted == message:
    print("\n✅ WORKS! Message decrypted correctly!")
else:
    print("\n❌ ERROR: decrypted message is wrong!")