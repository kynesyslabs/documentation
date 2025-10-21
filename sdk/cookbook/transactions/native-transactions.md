---
icon: money-check-dollar
---

# Native Transactions

You can send DEM using the Demos sdk as shown below:

### 1. Connect to the network

```javascript
import { Demos } from "@/websdk"

// Connect to the network
const rpc = "https://demosnode.discus.sh"
const demos = new Demos()
await demos.connect(rpc)

// Create and connect your wallet
const mnemonic = demos.newMnemonic()
await demos.connectWallet(mnemonic)
```

### 2. Create a transaction

You can now create a transaction by passing the address and the amount to `demos.transfer`.

```javascript
// 2. Create a transaction
const tx = await demos.transfer(
    "0x6690580a02d2da2fefa86e414e92a1146ad5357fd71d594cc561776576857ac5",
    100,
)
```

The transcation returned by `demos.transfer` is signed using the wallet connected to the `demos` object.

{% hint style="info" %}
`demos.transfer` is an alias to `demos.pay`
{% endhint %}

### 3. Broadcasting the transaction

```typescript
// Confirm the transaction
const validityData = await demos.confirm(tx)
console.log("Validity data", validityData)

// Broadcast the transaction
const broadcastRes = await demos.broadcast(validityData)
console.log("Broadcast result", broadcastRes)
```
