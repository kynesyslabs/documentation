# Quickstart

#### Quick Start Example

```typescript
import { instantMessaging } from "@kynesyslabs/demosdk"
import { encryption } from "@kynesyslabs/demosdk";

const unifiedCrypto = encryption.ucrypto

async function setupMessenger() {
    // Generate identities
    /* NOTE: This part is not necessary when using a SDK instance 
    that has already generated identities */
    const masterSeed = crypto.randomBytes(128)
    await unifiedCrypto.generateAllIdentities(masterSeed)
    const mlKemAes = await unifiedCrypto.getIdentity("ml-kem-aes")
    
    // Create and connect peer
    const peer = new instantMessaging.MessagingPeer({
        serverUrl: "ws://your-signaling-server:3005",
        clientId: "user-" + Date.now(),
        publicKey: mlKemAes.publicKey,
    })
    
    await peer.connect()
    
    // Set up message handler
    peer.onMessage((message, fromId) => {
        console.log(`Message from ${fromId}:`, message)
    })
    
    // Discover available peers
    const peers = await peer.discoverPeers()
    console.log("Available peers:", peers)
    
    return peer
}

// Use the messenger
const messenger = await setupMessenger()
```

Core Concepts

#### Connection Lifecycle

1. Initialization: Create a MessagingPeer instance with configuration
2. Connection: Connect to the signaling server
3. Registration: Register with the server using your client ID and public key (**NOTE:** in this step, an automatic sign-verify mechanism is enforced to link signing and encryption keys for a specific handle)
4. Discovery: Discover other available peers
5. Communication: Exchange messages with other peers
6. Disconnection: Disconnect from the server when done

\
\
