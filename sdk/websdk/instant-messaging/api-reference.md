# API Reference



The `MessagingPeer` class is the core component of the Instant Messaging Protocol. It handles connection to the signaling server, peer discovery, message exchange, and encryption/decryption.

#### Constructor

```typescript
constructor(config: MessagingPeerConfig)
```

Creates a new MessagingPeer instance.

**Parameters:**

* `config`: Configuration object containing:
  * `serverUrl`: WebSocket URL of the signaling server (the Demos Node managing the messenger instance)
  * `clientId`: Unique identifier for this peer
  * `publicKey`: Public key for encryption/decryption

**Example:**

```typescript
const peer = new MessagingPeer({
    serverUrl: "ws://your-signaling-server:3005",
    clientId: "your-unique-id",
    publicKey: mlKemAes.publicKey,
})
```

#### Methods

**connect**

```typescript
async connect(): Promise<void>
```

Connects to the signaling server and registers the peer.

**Returns:** Promise that resolves when connected and registered

**Example:**

```typescript
await peer.connect()
```

**disconnect**

```typescript
disconnect(): void
```

Disconnects from the signaling server.

**Example:**

```typescript
peer.disconnect()
```

**register**

```typescript
register(): void
```

Registers the peer with the signaling server.

**Example:**

```typescript
peer.register()
```

**registerAndWait**

```typescript
async registerAndWait(): Promise<void>
```

Registers the peer with the signaling server and waits for confirmation.

**Returns:** Promise that resolves when registration is confirmed

**Example:**

```typescript
await peer.registerAndWait()
```

**discoverPeers**

```typescript
async discoverPeers(): Promise<string[]>
```

Discovers all connected peers.

**Returns:** Array of peer IDs

**Example:**

```typescript
const peers = await peer.discoverPeers()
console.log("Available peers:", peers)
```

**sendMessage**

```typescript
async sendMessage(targetId: string, message: string): Promise<void>
```

Sends an encrypted message to a specific peer.

**Parameters:**

* `targetId`: ID of the target peer
* `message`: Message to send

**Example:**

```typescript
await peer.sendMessage("target-peer-id", "Hello from me!")
```

**requestPublicKey**

```typescript
async requestPublicKey(peerId: string): Promise<Uint8Array>
```

Requests a peer's public key.

**Parameters:**

* `peerId`: ID of the peer whose public key to request

**Returns:** The peer's public key as a Uint8Array

**Example:**

```typescript
const publicKey = await peer.requestPublicKey("target-peer-id")
```

**respondToServer**

```typescript
respondToServer(questionId: string, response: any): void
```

Responds to a server question.

**Parameters:**

* `questionId`: ID of the question to respond to
* `response`: Response to send back to the server

**Example:**

```typescript
peer.respondToServer("question-123", { answer: "This is my answer" })
```

**sendToServerAndWait**

```typescript
async sendToServerAndWait<T = any>(
    message: Message,
    expectedResponseType: Message["type"],
    options: {
        timeout?: number
        errorHandler?: (error: any) => void
        retryCount?: number
        filterFn?: (message: Message) => boolean
    } = {},
): Promise<T>
```

Sends a message to the server and waits for a specific response type.

**Parameters:**

* `message`: Message to send
* `expectedResponseType`: Type of response to wait for
* `options`: Additional options:
  * `timeout`: Timeout in milliseconds (default: 10000)
  * `errorHandler`: Custom error handler
  * `retryCount`: Number of retry attempts
  * `filterFn`: Function to filter messages by additional criteria

**Returns:** The response payload

**Example:**

```typescript
// Basic usage
const response = await peer.sendToServerAndWait(
    {
        type: "custom_action",
        payload: { someData: "value" },
    },
    "custom_action_success",
)

// With retry logic
const response = await peer.sendToServerAndWait(
    {
        type: "custom_action",
        payload: { someData: "value" },
    },
    "custom_action_success",
    {
        retryCount: 3,
        timeout: 5000,
    },
)

// With custom error handling
const response = await peer.sendToServerAndWait(
    {
        type: "custom_action",
        payload: { someData: "value" },
    },
    "custom_action_success",
    {
        errorHandler: error => {
            console.error("Custom error handling:", error)
        },
    },
)

// With filtering
const response = await peer.sendToServerAndWait(
    {
        type: "custom_action",
        payload: { someData: "value" },
    },
    "custom_action_success",
    {
        filterFn: message => message.payload.someProperty === expectedValue,
    },
)
```

#### Event Handlers

**onMessage**

```typescript
onMessage(handler: (message: any, fromId: string) => void): void
```

Registers a handler for incoming messages.

**Parameters:**

* `handler`: Function to call when a message is received

**Example:**

```typescript
peer.onMessage((message, fromId) => {
    console.log(`Message from ${fromId}:`, message)
})
```

**onServerQuestion**

```typescript
onServerQuestion(handler: (question: any, questionId: string) => void): void
```

Registers a handler for server questions.

**Parameters:**

* `handler`: Function to call when a server question is received

**Example:**

```typescript
peer.onServerQuestion((question, questionId) => {
    console.log("Server asked:", question)

    // Process the question and prepare a response
    const response = { answer: "This is my answer" }

    // Send the response back to the server
    peer.respondToServer(questionId, response)
})
```

**onError**

```typescript
onError(handler: (error: { type: string; details: string }) => void): void
```

Registers a handler for errors.

**Parameters:**

* `handler`: Function to call when an error occurs

**Example:**

```typescript
peer.onError(error => {
    console.error(`Error: ${error.type} - ${error.details}`)
})
```

**onPeerDisconnected**

```typescript
onPeerDisconnected(handler: (peerId: string) => void): void
```

Registers a handler for peer disconnection events.

**Parameters:**

* `handler`: Function to call when a peer disconnects

**Example:**

```typescript
peer.onPeerDisconnected(peerId => {
    console.log(`Peer disconnected: ${peerId}`)
})
```

**onConnectionStateChange**

```typescript
onConnectionStateChange(handler: (state: "connected" | "disconnected" | "reconnecting") => void): void
```

Registers a handler for connection state changes.

**Parameters:**

* `handler`: Function to call when the connection state changes

**Example:**

```typescript
peer.onConnectionStateChange(state => {
    console.log(`Connection state changed: ${state}`)
})
```

#### Message Types

The Instant Messaging Protocol supports various message types:

* **"register"**: Register a new peer with the server
* **"discover"**: Request a list of all connected peers
* **"message"**: Encrypted peer-to-peer messages
* **"peer\_disconnected"**: Notification when a peer disconnects
* **"request\_public\_key"**: Request a peer's public key
* **"public\_key\_response"**: Response containing a peer's public key
* **"server\_question"**: Question from the server to a peer
* **"peer\_response"**: Response from a peer to a server question
* **"debug\_question"**: Debug message to trigger a server question
* **"error"**: Error notification with details

#### Message Interface

```typescript
export interface Message {
    type:
        | "register"
        | "discover"
        | "message"
        | "peer_disconnected"
        | "request_public_key"
        | "public_key_response"
        | "server_question"
        | "peer_response"
        | "debug_question"
        | "error"
    payload: any
}
```

#### MessagingPeerConfig Interface

```typescript
export interface MessagingPeerConfig {
    serverUrl: string
    clientId: string
    publicKey: Uint8Array

```
