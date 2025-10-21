---
icon: signature-lock
---

# Signing a transaction

To sign a transaction, you need to connect your master seed to a `Demos` instance.

```typescript
const demos = new Demos()

const mnemonic = "river cat ..."
const publicKey = await demos.connectWallet(mnemonic)
```

Then sign your transaction as shown:

```typescript
const signedTx = await demos.sign(tx)
console.log("signed tx: ", signedTx)
```
