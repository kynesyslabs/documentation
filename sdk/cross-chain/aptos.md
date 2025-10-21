---
icon: circle
---

# APTOS

## Aptos Cross-Chain SDK

The Aptos blockchain uses the Move programming language and provides a powerful environment for smart contracts and decentralized applications. The Demos Network SDK provides seamless integration with Aptos through our XM (Cross-chain Messaging) architecture.

### Key Concepts

**Demos Network Architecture**: Payment and contract operations go through Demos, ensuring network participation and cross-chain compatibility. This relay-first approach provides enhanced security and enables true cross-chain functionality.

**Move Language**: Aptos uses Move, a resource-oriented programming language where smart contracts are organized as modules deployed at specific addresses.

**Type Arguments**: Many Move functions require explicit type arguments, especially when working with generic types like coins.

### Installation

```bash
npm install @kynesyslabs/demosdk @aptos-labs/ts-sdk
```

### Quick Start

```javascript
import { Network } from '@aptos-labs/ts-sdk'
import { APTOS } from '@kynesyslabs/demosdk/xmcore'

// Initialize with network
const aptos = new APTOS("", Network.DEVNET)
// Using a custom RPC endpoint
// new APTOS("https://custom-aptos-rpc.com", Network.DEVNET)
await aptos.connect()

// Connect wallet
const privateKey = "0x..." // Your private key
await aptos.connectWallet(privateKey)
```

### Balance Queries

You can get the coin balance as shown below:

```javascript
// Get APT balance
const balance = await aptos.getBalance(address)
console.log("APT balance", balance)

// Get specific coin balance
const coinBalance = await aptos.getCoinBalance("0x1::aptos_coin::AptosCoin", address)
console.log("AptosCoin balance", coinBalance)
```

### Token Transfer

You can make payments on Aptos via Demos as shown below. Please check out the [authentication](../websdk/authentication/ "mention") docs on how to interact with the Demos network using the `Demos` object.

```typescript
import { XMScript } from "@kynesyslabs/demosdk/types"
import { prepareXMPayload } from "@kynesyslabs/demosdk/websdk"

const recipient = "0x..."

// Amount in octa (1 APT = 100,000,000 Octas)
const amount = "3000"

// Get the signed tx as hex string
const tx = aptos.preparePay(recipient, amount)

// Broadcast the tx
const payload: XMScript = {
    operations: {
        aptos_pay: {
            chain: "aptos",
            subchain: "devnet",
            is_evm: false,
            rpc: null,
            task: {
                signedPayloads: [tx],
                params: null,
                type: "pay",
            }
        }
    },
    operations_order: ["aptos_pay"],
}

// Create the Demos tx
const tx = await prepareXMPayload(payload, demos)
console.log("tx", tx)

// Validate Demos tx
const validityData = await demos.confirm(tx)
console.log("validityData", validityData)
 
// Broadcast
const res = await demos.broadcast(validityData)
console.log("res", JSON.stringify(res, null, 2))
```

When working with Aptos browser extensions use their documentation to create and sign the transaction. Here is some documentation:

* Petra:  [Connect to Petra wallet](https://petra.app/docs/connect-to-petra) and [sign a transaction](https://petra.app/docs/sending-a-transaction#sign-only)
* Martian: [Detecting the provider](https://docs.martianwallet.xyz/docs/integration/detecting-the-provider) and [sign a transaction](https://docs.martianwallet.xyz/docs/methods/aptos/sign-transaction)

Once you have the signed transaction as a `Uint8Array`, convert it into hex and use that to create the `XMScript` from the previous code sample:

For Martian wallet, that would look like this:

```typescript
import { hexToUint8Array } from "@kynesyslabs/demosdk/encryption"

const txBuffer = await window.martian.signTransaction(transaction)
const txHex = uint8ArrayToHex(txBuffer)

const payload: XMScript = {
    operations: {
        aptos_pay: {
            chain: "aptos",
            subchain: "devnet",
            is_evm: false,
            rpc: null,
            task: {
                signedPayloads: [txHex],
                params: [],
                type: "pay",
            }
        }
    },
    operations_order: ["aptos_pay"],
}

// Proceed to create Demos tx, validate and broadcast
```

### Smart Contract Interactions

#### Reading from Contracts

You can read from a contract on Aptos via Demos as shown:

```javascript
// Read the "name" property of a contract
const payload = await instance.readFromContract(
    "0x1",
    "coin",
    "name",
    [],
    ["0x1::aptos_coin::AptosCoin"]
)

// Create Demos tx
const tx = await prepareXMPayload(payload, demos)
console.log("tx", tx)

// Validate Demos tx
const validityData = await demos.confirm(tx)
console.log("validityData", validityData)

// Broadcast
const res = await demos.broadcast(validityData)
console.log("res", JSON.stringify(res, null, 2))
```

#### Writing to Contracts

You can write to a contract on Aptos via Demos as shown:

```javascript
// Write to the "transfer" method on a contract
const payload = await instance.writeToContract(
    "0x1",                                 // module address
    "coin",                                // module name
    "transfer",                            // function name
    [testAddress, "1000"],                 // args: [recipient, amount]
    ["0x1::aptos_coin::AptosCoin"]         // typeArguments: coin type
)
console.log("xmscript", xmscript)

// Create Demos tx
const tx = await prepareXMPayload(payload, demos)
console.log("tx", tx)

// Validate Demos tx
const validityData = await demos.confirm(tx)
console.log("validityData", validityData)

// Broadcast
const res = await demos.broadcast(validityData)
console.log("res", JSON.stringify(res, null, 2))
```

### Signing and Verifying Messages

You can sign and verify messages using the connected Aptos wallet as shown:

```typescript
// Sign message
const signature = await aptos.signMessage("Hello Demos Network")

// Verify message signature
const publicKey = aptos.getPublicKey()
const isVerified = await aptos.verifyMessage(message, signature, publicKey)
```

When working with browser wallet extensions, use their documentation to sign the message:

* Martian: [https://docs.martianwallet.xyz/docs/methods/sign-message](https://docs.martianwallet.xyz/docs/methods/sign-message)
* Petra: [https://petra.app/docs/signing-a-message](https://petra.app/docs/signing-a-message)

The `signMessage` method provided by the injected provider returns an object with a `fullMessage` property which you can use to verify the message as follows:

For Martian wallet, that looks like this:

```typescript
const { fullMessage, signature } = await window.martian.signMessage({
    message,
    nonce,
})

// Verify using the Demos Aptos SDK
const isVerified = aptos.verifyMessage(fullMessage, signature, publicKey)
```

### Utility Methods

```javascript
// Get wallet address
const address = aptos.getAddress()

// Validate Aptos address
const isValid = aptos.isAddress("0x1")

// Wait for transaction confirmation
const txResponse = await aptos.waitForTransaction(txHash)
```
