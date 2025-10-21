---
icon: circle-2
---

# Base Operation

The base operation allow you to group work steps and operations for execution without any additional logic.

```ts
import { BaseOperation, prepareXMStep } from "@kynesyslabs/demosdk/demoswork"

// Work steps
const sendEth = prepareXMStep({
    // XMScript here
})

const sendSol = prepareXMStep({
    // XMScript here
})

// Base operation
const base = new BaseOperation()
base.addWork(sendEth, sendSol)

const work = new DemosWork()
work.push(base)

```

Work steps are created and added to the base operation using the `addWork` method.

You can also pass the work steps and operations to the constructor of the `BaseOperation` class.

```ts
const base = new BaseOperation(checkBTCPrice, checkEthPrice)
```

{% hint style="info" %}
You can also use operations (eg. conditional operation) and work steps with the `BaseOperation` class.
{% endhint %}
