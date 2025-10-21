# Post Quantum Cryptography

Demos support use of the following Quantum safe signing algorithms for transaction and transmission signing:

1. Falcon
2. ML-DSA



You can sign transactions using Falcon by connecting your mnemonic as shown:

```typescript
import { Demos } from "@kynesyslabs/demosdk/websdk"

const demos = new Demos()
const mnemonic = demos.newMnemonic()
await demos.connectWallet(mnemonic, {
    algorithm: "falcon",
    dual_sign: true
})

const rawTx = {...}
const tx = demos.sign(tx)
```

### PQC Identities

You can link your PQC identities to your ed25519 address on the Demos network, to allow you to only include the PQC signature on future transactions.

```typescript
import { Identities } from "@kynesyslabs/demosdk/abstraction"

const identities = new Identities()

// You can also pass a list of pqc algorithms. eg. ["falcon"]
const validityData = await identities.bindPqcIdentity(demos, "all")
const res = await demos.broadcast(validityData)

console.log(res)
```



For future wallet connections, you can connect your wallet without the `dual_sign` option. Transactions will not have the ed25519 signature and your ownership of the ed25519 address will be validated on the network.
