---
icon: circle-3
---

# Signing and broadcasting

To convert a Demoswork object to a transaction, use the `prepareDemosWorkPayload` function.

```ts
import { prepareDemosWorkPayload } from "@kynesyslabs/demosdk/demoswork"

const demos = new Demos()
await demos.connect("https://demosnode.discus.sh")
await demos.connectWallet(mnemonic)

// Creating a transaction
const tx = await prepareDemosWorkPayload(work, demos)
```

### Broadcasting the transaction

You can broadcast the transaction using the `confirm` and `broadcast` methods of the `demos` object.

```ts
// Confirming the transaction
const validityData = await demos.confirm(tx)

// Broadcasting the transaction
const res = await demos.broadcast(validityData)
console.log("res:", res)
```

{% hint style="warning" %}
**Important**\
\
The execution of a demoscript is not available at the moment as the DemosWork spec is still in development.
{% endhint %}

