# FAQ

## Frequently Asked Questions (FAQ)

### General Questions

#### What is the Instant Messaging Protocol?

The Instant Messaging Protocol is a secure, efficient, and scalable protocol for building real-time messaging applications on the Demos network. It provides end-to-end encryption, peer discovery, and reliable message delivery for developers creating messenger applications.

#### What are the main features of the Instant Messaging Protocol?

The protocol offers several key features:

* End-to-end encryption using state-of-the-art cryptographic algorithms
* Built-in peer discovery mechanisms
* Low-latency real-time communication
* Reliable message delivery with acknowledgment
* Scalable architecture for handling many concurrent connections
* Cross-platform support

#### What platforms does the Instant Messaging Protocol support?

The protocol is designed to work across different platforms and devices. It can be used to build applications for:

* Web browsers (using JavaScript/TypeScript)
* Mobile devices (iOS, Android)
* Desktop applications
* IoT devices

### Technical Questions

#### How does the encryption work?

The protocol uses end-to-end encryption with public-key cryptography. Each peer has a public/private key pair, and messages are encrypted using the recipient's public key. Only the recipient with the corresponding private key can decrypt the messages.

#### What cryptographic algorithms are used?

The protocol uses the ML-KEM-AES algorithm for encryption, which provides strong security guarantees. The implementation is based on modern cryptographic standards and best practices.

#### How does peer discovery work?

Peer discovery is facilitated by the signaling server. When a peer connects to the server, it registers its presence. Other peers can then request a list of all connected peers from the server.

#### How reliable is message delivery?

The protocol includes mechanisms to ensure reliable message delivery. Messages are queued if the recipient is offline and delivered when they reconnect. The protocol also includes acknowledgment mechanisms to confirm message receipt.

#### How does the protocol handle network issues?

The protocol includes automatic reconnection with exponential backoff. If the connection to the signaling server is lost, the MessagingPeer will attempt to reconnect automatically, with increasing delays between attempts to avoid overwhelming the server.

### Implementation Questions

#### How do I set up a signaling server?

Setting up a signaling server is automatically managed when running a Demos Node.

#### How do I create a MessagingPeer instance?

To create a MessagingPeer instance, you need to provide a configuration object with the server URL, a unique client ID, and a public key:

```javascript
import {
    MessagingPeer
} from "@kynesyslabs/demosdk/instant_messaging"
import { unifiedCrypto } from "@kynesyslabs/demosdk/encryption/unifiedCrypto"

// NOTE: Be sure to either set up unifiedCrypto as defined in the
// quickstart or use an already defined unifiedCrypto instance
// with identities generated

mlKemAes = await unifiedCrypto.getIdentity("ml-kem-aes")


const peer = new MessagingPeer({
    serverUrl: "ws://your-signaling-server:3005",
    clientId: "your-unique-id",
    publicKey:  mlKemAes.publicKey,
})
```

#### How do I send a message to another peer?

To send a message to another peer, you need to know their ID. You can discover available peers using the `discoverPeers` method, and then send a message using the `sendMessage` method:

```javascript
// Discover available peers
const peers = await peer.discoverPeers()

// Send a message to the first available peer
if (peers.length > 0) {
    await peer.sendMessage(peers[0], "Hello from me!")
}
```

#### How do I handle incoming messages?

You can register a message handler using the `onMessage` method:

```javascript
peer.onMessage((message, fromId) => {
    console.log(`Message from ${fromId}:`, message)
})
```

#### How do I handle errors?

You can register an error handler using the `onError` method:

```javascript
peer.onError(error => {
    console.error(`Error: ${error.type} - ${error.details}`)
})
```

#### How do I handle peer disconnection events?

You can register a peer disconnected handler using the `onPeerDisconnected` method:

```javascript
peer.onPeerDisconnected(peerId => {
    console.log(`Peer disconnected: ${peerId}`)
})
```

### Security Questions

#### Is the protocol secure?

Yes, the protocol is designed with security as a top priority. It uses end-to-end encryption to ensure that only the intended recipient can read messages, even if they are intercepted during transmission.

#### How does the protocol handle authentication?

Peers are authenticated using their public keys. When a peer registers with the signaling server, it provides its public key, which is used to verify its identity. Furthermore, the peer needs to sign its public key with a signing key (included in the unifiedCrypto instance) to link its encryption key (ml-kem) to its signing key (ml-dsa).

#### Does the protocol support perfect forward secrecy?

Yes, the protocol supports perfect forward secrecy. Each message uses a unique encryption key, preventing compromise of past messages if a key is compromised. This is obtained by using ml-kem as the encapsulation algorithm on top of AES.

#### Can I implement additional security measures?

Yes, you can implement additional security measures on top of the protocol. For example, you could add user authentication, message signing, or additional encryption layers.

### Performance Questions

#### How scalable is the protocol?

The protocol is designed to be highly scalable. The signaling server can handle a large number of concurrent connections, and the peer-to-peer communication model reduces the load on the server.

#### What is the latency of message delivery?

The protocol is designed for low-latency communication. Message delivery time depends on network conditions, but the protocol minimizes overhead to ensure fast delivery.

#### How does the protocol handle large messages?

The protocol can handle messages of various sizes. Large messages are automatically chunked and reassembled if necessary.

#### How does the protocol handle high message volumes?

The protocol includes mechanisms to handle high message volumes, including message queuing and rate limiting to prevent overwhelming the network or the signaling server.

### Troubleshooting

#### What should I do if I can't connect to the signaling server?

If you can't connect to the signaling server, check the following:

* Ensure the server is running and accessible
* Check your network connection
* Verify that the server URL is correct
* Check if there are any firewall rules blocking the connection
* Ensure your `unifiedCrypto` instance is initialized (aka, identities are generated and available as explained in [quickstart.md](quickstart.md "mention"))

#### What should I do if messages are not being delivered?

If messages are not being delivered, check the following:

* Ensure the recipient is connected to the signaling server
* Check if there are any network issues
* Verify that the recipient's ID is correct
* Check if there are any error messages in the console

#### What should I do if I'm experiencing high latency?

If you're experiencing high latency, check the following:

* Check your network connection
* Ensure the signaling server is not overloaded
* Consider using a signaling server closer to your location
* Check if there are any firewall rules or network configurations affecting performance

#### How do I debug issues with the protocol?

You can enable debug logging to get more information about what's happening:

```javascript
// Enable debug logging
peer.onConnectionStateChange(state => {
    console.log(`Connection state changed: ${state}`)
})

peer.onError(error => {
    console.error(`Error: ${error.type} - ${error.details}`)
})
```

### Additional Resources

* [api-reference.md](api-reference.md "mention"): Detailed documentation of the available methods and interfaces.
* [quickstart.md](quickstart.md "mention"): Step-by-step guide to setting up a basic messenger code.
* [encryption.md](encryption.md "mention"): explanation about the encryption used within the messenger
