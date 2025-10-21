---
icon: square-1
---

# Crosschain Transaction

You can perform a crosschain transaction via the DEMOS network with the help of the DEMOS sdk.&#x20;

Here is how you can send tokens on Sepolia testnet via DEMOS using the sdk:

### 0. Imports

The following imports will be needed to create the transaction.

```typescript
import {
  Demos,
  prepareXMPayload,
  prepareXMScript,
} from "@kynesyslabs/demosdk/websdk";

import { EVM } from "@kynesyslabs/demosdk/xm-websdk";
```

### 1. Creating the EVM payload

You can create the payload for Sepolia via the crosschain module of the sdk as follows:

```typescript
const sepolia_rpc = "https://rpc.ankr.com/eth_sepolia"
const evm = await EVM.create(sepolia_rpc);
await evm.connectWallet(
  "e0a00e307....." // fill in with your sepolia private key
);

const evm_tx = await evm.preparePay(
    "0xda3ea78Af43E6B1c63A08cD0058973F14e5556b0",
    "0.000000001",
)
```

The `evm_tx` will be a signed transaction to move 0.000000001 Sepolia ETH from the connected wallet to`0xda3ea78Af43E6B1c63A08cD0058973F14e5556b0`.

### 2. Converting the payload into an XMScript

The [XMScript](../../cross-chain/the-xmscript.md) contains information that helps a DEMOS node understand what to do with a signed crosschain payload.

```typescript
const xmscript = prepareXMScript({
  chain: "eth",
  subchain: "sepolia",
  signedPayloads: [evm_tx],
  type: "pay",
});
```

The `xmscript` will be embedded into a DEMOS transaction and sent to the DEMOS network in the upcoming sections.

### 3. Creating a DEMOS instance

A DEMOS identity is needed to sign the outgoing DEMOS transaction.

```typescript
const demos = new Demos()

const demos_rpc = "https://demosnode.discus.sh";
await demos.connect(demos_rpc);

const mnemonic = demos.newMnemonic()
await demos.connectWallet(mnemonic)
```

### 4. Converting the XMScript to a Demos transaction

You can convert the `xmscript` into a DEMOS transaction by calling `prepareXMPayload` and passing the `xmscript` and the `Demos` instance.

```typescript
const tx = await prepareXMPayload(xmscript, demos);
```

The `tx` will be a signed Demos transaction containing the Sepolia tx.

### 5. Broadcasting to a Demos node

You can now broadcast the transaction as shown:

```typescript
// confirm tx
const validityData = await demos.confirm(tx);
console.log("validityData", validityData);

// execute
const res = await demos.broadcast(validityData);
console.log("res", res);
```
