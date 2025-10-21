# Architecture Overview

The Instant Messaging Protocol consists of three main components:

1. Signaling Server: A central hub that facilitates peer discovery and message routing. It runs automatically on every Demos node and it's part of the backend
2. MessagingPeer: A client-side class that handles connection and message exchange. It's the SDK part we are focusing on.
3. Encryption System: A cryptographic layer that ensures secure communication, leveraging Post Quantum Cryptography through the robust Demos SDK features.
