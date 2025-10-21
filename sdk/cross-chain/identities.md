---
icon: fingerprint
---

# Identities

### Adding an Identity

You can associate a crosschain identity with a DEMOS address by creating a signature using your private key and sending it to the DEMOS network.

{% hint style="info" %}
DEMOS network supports linking Web2 identities too (for example, login with Twitter or with Github).\
\
See web2 [identities](../web2/identities/ "mention")
{% endhint %}

{% hint style="info" %}
Check out how to create a signature on the "**Signing Messages**" section of the respective crosschain SDK documentation. eg. [EVM](evm.md#signing-messages)
{% endhint %}

#### 0. Imports

```typescript
import { Demos } from "@kynesyslabs/demosdk/websdk"
import { Identities } from "@kynesyslabs/demosdk/abstraction"
import { InferFromSignaturePayload } from "@kynesyslabs/demosdk/types/abstraction"
```

#### 1. Creating the signature

Connect your wallet to the XM instance and create a signature

```javascript
// connect your 
const xmAddress = instance.getAddress()
const message = `Link ${instance.name} address ${address} to Demos`
const signature = await instance.signMessage(message)
```

{% hint style="info" %}
The signature will be verified on the network to prevent adding identities not owned by you
{% endhint %}

#### 2. Creating the DEMOS payload

The payload to add a Sepolia address would look like this:

```javascript
const payload: InferFromSignaturePayload = {
    method: "identity_assign_from_signature",
    target_identity: {
        chain: "eth",
        chainId: instance.chainId,
        subchain: "sepolia",
        isEVM: true,
        signature: signature,
        signedData: message,
        targetAddress: instance.getAddress(),
    },
}
```

#### 3. Connecting to the network

Create a new `Demos` object and connnect the RPC and your private key.

```typescript
const rpc = "https://demosnode.discus.sh"

// connect to the DEMOS rpc
const demos = new Demos()
await demos.connect(rpc)

// connect private key
await demos.connectWallet(mnemonic)
```

#### 4. Sending the payload

Then send the identity payload to the network using the `identities` instance as shown:

Use `identities.inferIdentity` to create a transaction that adds your identity to the blockchain. Then broadcast the transaction using `demos.broadcast`.

```typescript
const identities = new Identities()
const validityData = await identities.inferXmIdentity(demos, payload)

const res = await demos.broadcast(validityData)
console.log(res)

// {
//   result: 200,
//   response: { message: 'Signature verified. Transaction applied.' },
//   require_reply: false,
//   extra: { confirmationBlock: 3 }
// }

```

### Getting Identities

After the `confirmationBlock` has been forged, you can retrieve all the identities associated with your DEMOS address as shown:

```typescript
const res = await identities.getIdentities(demos)
console.log(res)

// {
//   "result": 200,
//   "response": {
//     "xm": {
//       "evm": {
//         "sepolia": [
//           "0x4298A9D2A573dA64102255d11d6908b7e3d89b02"
//         ]
//       }
//     },
//     "web2": {}
//   },
//   "require_reply": false,
//   "extra": null
// }
```

### Removing an Identity

You can remove your crosschain identity from DEMOS as shown:

```typescript
const validityData = await identities.removeXmIdentity(demos, {
    chain: "evm",
    subchain: "sepolia",
    targetAddress: instance.getAddress(), // the address to remove
})

const res = await demos.broadcast(validityData)
console.log(res)

// {
//   result: 200,
//   response: { message: 'Transaction applied, waiting for confirmation' },
//   require_reply: false,
//   extra: { confirmationBlock: 25 }
// }
```
