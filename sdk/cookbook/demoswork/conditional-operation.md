---
icon: circle-2
---

# Conditional Operation

There are two ways to go about creating a conditional operation.

1. Using the `if`, `then` and `else` methods of the `ConditionalOperation` class.
2. Creating `Condition` objects and passing them to the constructor of the `ConditionalOperation` class.

#### 1. Using the `if`, `then` and `else` methods

```ts
import { EVM } from "@kynesyslabs/demosdk/multichain/websdk"
import { prepareXMScript } from "@kynesyslabs/demosdk/websdk/XMTransactions"
import {
    DemosWork,
    prepareWeb2Step,
    prepareXMStep,
    ConditionalOperation,
} from "@kynesyslabs/demosdk/demoswork"

const address = "0x8A6575025DE23CB2DcB0fE679E588da9fE62f3B6"
const isMember = prepareWeb2Step({
    url: `https://api.[redacted].com/v1/eth_sepolia/address/${address}`,
    method: "GET",
})

// Web2 step to do a POST API call
const addMember = prepareWeb2Step({
    url: `https://api.[redacted].com/v1/eth_sepolia/address/${address}?key=ckey_5a044cf0034a43089e6b308b023`,
    method: "POST",
})

// XM step to send ETH
const evm = await EVM.create("https://rpc.ankr.com/eth_sepolia")
await evm.connectWallet(process.env.EVM_KEY)
const payload = await evm.prepareTransfer(address, "0.25")

const xmscript = prepareXMScript({
    chain: "eth",
    subchain: "sepolia",
    type: "pay",
    signedPayloads: [payload],
})
const releaseFunds = prepareXMStep(xmscript)

// Conditional operation

const operation = new ConditionalOperation()
operation
    .if(isMember.output.statusCode, "==", 200)
    .then(releaseFunds)
    .else(addMember)

// Creating a DemosWork object and indexing the operation
const work = new DemosWork()
work.push(operation)
```

#### Using the `Condition` class

The `Condition` class can be used to construct a conditional operation without using the `if`, `then` and `else` methods.

`Condition` objects can be reused and combined to create more complex conditional operations.

A condition looks is implemented as follows:

```ts
import { operators } from "@kynesyslabs/demosdk/types"

class Condition {
    value_a: any
    operator: operators
    value_b: any
    action: WorkStep | DemosWorkOperation
}
```

The `value_a` and `value_b` fields are the operands of the condition. The `operator` field determines the type of condition. The `action` field is the work step or operation that will be executed if the condition is met.

The `value_a` and `value_b` fields can accept any of the following:

1. A work step or operation output
2. Another condition
3. A static value

You can create the same conditional operation as the previous example using the `Condition` class as follows:

```ts
import { EVM } from "@kynesyslabs/demosdk/multichain/websdk"
import { prepareXMScript } from "@kynesyslabs/demosdk/websdk/XMTransactions"
import {
    Condition,
    DemosWork,
    prepareWeb2Step,
    prepareXMStep,
    ConditionalOperation,
} from "@kynesyslabs/demosdk/demoswork"

const address = "0x8A6575025DE23CB2DcB0fE679E588da9fE62f3B6"
const isMember = prepareWeb2Step({
    url: `https://api.[redacted].com/v1/eth_sepolia/address/${address}`,
    method: "GET",
})

// Web2 step to do a POST API call
const addMember = prepareWeb2Step({
    url: `https://api.[redacted].com/v1/eth_sepolia/address/${address}?key=ckey_5a044cf0034a43089e6b308b023`,
    method: "POST",
})

// XM step to send ETH
const evm = await EVM.create("https://rpc.ankr.com/eth_sepolia")
await evm.connectWallet(process.env.EVM_KEY)
const payload = await evm.prepareTransfer(address, "0.25")

const xmscript = prepareXMScript({
    chain: "eth",
    subchain: "sepolia",
    type: "pay",
    signedPayloads: [payload],
})
const releaseFunds = prepareXMStep(xmscript)

// Condition to check if the user is a member
const checkIsMember = new Condition({
    value_a: isMember.output.statusCode,
    operator: "==",
    value_b: 200,
    action: releaseFunds,
})

// Fallback condition (else)
const notMember = new Condition({
    value_a: null,
    operator: null,
    value_b: null,
    action: addMember,
})

// Creating a conditional operation
const operation = new ConditionalOperation(checkIsMember, notMember)

// Creating a DemosWork object and indexing the operation
const work = new DemosWork()
work.push(operation)
```

### Combining conditions

You can combine conditions to create more complex conditions as shown below:

```ts
// equality
const booleanCondition = new Condition({
    value_a: true,
    operator: "==",
    value_b: true,
})

// greater than
const greaterThanCondition = new Condition({
    value_a: 10,
    operator: ">",
    value_b: 5,
})

// and
const combinedCondition = new Condition({
    value_a: booleanCondition,
    operator: "&&",
    value_b: greaterThanCondition,
})

// not
const notCondition = new Condition({
    value_a: booleanCondition,
    operator: "not",
    value_b: null,
})
```

### Referencing web2 payloads in conditions

Web2 requests return various shapes of payload when executed, including plain text or JSON. Let's illustrate how you can reference these payloads using a GET request to read the current BTC price.

```typescript
const getBTCPrice = prepareWeb2Step({
    url: "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
    method: "GET",
})

// {"bitcoin":{"usd":68233}}
```

The value we can use in a condition is nested inside the `bitcoin` object under the `usd` key. We can reference the value as shown below:

```typescript
new Condition({
    value_a: getBTCPrice.output["bitcoin.usd"],
    ...
})
```

When dealing with web2 endpoints that return a single value, eg. a string or number, or when you want to reference the whole payload, you can do the following:

```typescript
new Condition({
    value_a: getBTCPrice.output,
    ...
})
```
