---
icon: circle-1
---

# Creating work steps

### Creating a web2 workstep

You can create a web2 workstep to performa a `GET` request to `https://icanhazip.com` using the `prepareWeb2Step` function.

```ts
import { prepareWeb2Step } from "@kynesyslabs/demosdk/demoswork"

const getIP = prepareWeb2Step({
    action: "GET",
    url: "https://icanhazip.com",
})
```

### Creating a XM workstep

THe process of creating a cross chain workstep to send some ETH to an address can be described as follows:

1. Generating a payload to send ETH
2. Create a `XMScript` with the payload
3. Create an XM step with the `XMScript`

```ts
import { XMScript } from "@kynesyslabs/demosdk/types"
import { EVM } from "@kynesyslabs/demosdk/multichain/websdk"
import { prepareXMStep } from "@kynesyslabs/demosdk/demoswork"
import { prepareXMScript } from "@kynesyslabs/demosdk/websdk/XMTransactions"


// 1. Getting EVM payload
const evm_rpc = "https://rpc.ankr.com/eth_sepolia"
const evm_key = process.env.EVM_KEY

const evm = await EVM.create(evm_rpc)
await evm.connectWallet(evm_key)

const payload = await evm.prepareTransfer(
    "0x8A6575025DE23CB2DcB0fE679E588da9fE62f3B6",
    "0.25",
)

// 2. Creating a XMScript
const xmscript = prepareXMScript({
    chain: "eth",
    subchain: "sepolia",
    type: "pay",
    signedPayload: payload,
})

// 3. Creating a XM step
const sendEth = prepareXMStep(xmscript)
```
