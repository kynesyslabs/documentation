---
icon: envelope-circle-check
---

# Broadcasting a transaction

The DEMOS transaction broadcasting system works as a 2 step process.

### Step 1: Gas fee confirmation

The confirmation process starts by a client sending the transaction to the node. The node analyses the workload and returns information on how much gas is needed to execute your transaction.

```typescript
const validityData = await demos.confirm(tx)

console.log("Validity data: ", validityData)
```

The information is wrapped in a validity data object, which looks something like this:

```typescript
{
  valid: true,
  reference_block: 63754,
  message: '[Native Tx Validation] Transaction signature verified\n',
  gas_operation: {
    operator: 'pay_gas',
    actor: '[object Object]',
    params: {
      amount: '10112.6664',
    },
    hash: '1150ffa293be58b3537fbc5c41c97ab3686a0360c85d64903dd0ecc3337ce713',
    nonce: 0,
    timestamp: 1726757110915,
    status: 'pending',
    fees: {
      network_fee: 0,
      rpc_fee: 0,
      additional_fee: 0,
    },
  },
  transaction: {
    // ...
  },
}

```

The response is an object containing the status code, the response or an error message if one occured and your transaction. If you are comfortable with the amount of gas to be used (`gas_operation.params.amount`), you can proceed to broadcasting the tx.

{% hint style="info" %}
Your public key and public key signature are sent along with the request for verification. You need to have your KeyPair connected to the `demos` object.
{% endhint %}

### Step 2: Broadcasting the validity data

To execute your transaction, send back the validity data to the node.

```typescript
const res2 = await demos.broadcast(validityData)
```
