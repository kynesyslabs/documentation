---
icon: file-xmark
---

# The XMScript

The `XMScript` is a JSON script that dictates how a cross chain should be broadcasted to another blockchain from a DEMOS node.

The `XMScript` contains the following information:

1. Blockchain identifier .eg. `eth`,`solana`, `xrpl`, etc
2. Subchain identifier .eg. `sepolia`
3. Signed payload
4. Task parameters
5. Task type. eg. `pay`, `contract_read`
6. RPC URL (Optional)

A single `XMScript` can contain multiple blockchain payloads. The order of execution of these payloads is controlled using an `operation_order` list.



Here's an example `XMScript`

```typescript
import { XMScript } from "@kynesyslabs/demosdk/types"

const xmscript: XMScript = {
    operations: {
        "0": {
            chain: "eth",
            is_evm: true,
            rpc: null,
            subchain: "sepolia",
            task: {
                params: null,
                signedPayloads: ["0x02f87583aa36a76a84237ef1..."],
                type: "pay",
            },
        },
    },
    operations_order: ["0"],
}
```
