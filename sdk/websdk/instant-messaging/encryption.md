# Encryption

The Instant Messaging Protocol uses ml-kem-aes for secure communication:

1. Key Generation: Each peer generates a public/private key pair
2. Public Key Exchange: Peers exchange public keys through the signaling server
3. Signatures: peers sign their ml-kem public keys with a ml-dsa signing key from the same unifiedCrypto instance to link their two keys
4. Message Encryption: Messages are encrypted using the recipient's public key through encapsulation of a shared secret
5. Message Decryption: Recipients decrypt messages using their private key to decapsulate the shared secret and perform AES decryption

\
