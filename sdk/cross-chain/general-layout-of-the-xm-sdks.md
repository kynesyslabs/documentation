---
icon: map
---

# General layout of the XM SDKs

All the crosschain SDKs share the same interface, with a few blockchain-specific methods occuring on some SDKS.



To demonstrate the general layout of the SDKs, let's use the EVM crosschain SDK for the web.

### Creating an SDK instance

Start by instantiating the SDK class using a RPC url.

```typescript
import { EVM } from "@kynesyslabs/demosdk/xm-websdk"

const rpc_url = "https://rpc.ankr.com/eth_sepolia"
const instance = await EVM.create()
```

The create method will ping the RPC and return an instance of the SDK connected to the RPC.

### Changing the RPC URL

You can assign a new rpc url as shown:

```typescript
instance.setRpc("<new_rpc_url>")
await instance.connect()
```

### Reading Blockchain data

You can access now acess Blockchain data using the helper methods provided by the SDK. For example, to read an address balance:

```typescript
const balance = instance.getBalance("0xa5...")
```

You can access additional methods for reading blockchain data by exploring the `provider` object inside the SDK instance.\
\
For example, to get the latest block on Ethereum:

```typescript
const block = await instance.provider.getBlock("latest")
```

{% hint style="info" %}
The shape of the `provider` object is SDK specific. Please find the link to the API reference at the bottom of the specific crosschain SDK documentation page.
{% endhint %}

### Connecting a private key

To create and sign payloads, you need to attach your private key to your SDK instance.

```typescript
const privateKey = "0xaAIf..."
const wallet = await instance.connectWallet(privateKey)
```

The `connectWallet` method returns the `wallet` object that holds your private key inside the SDK instance.

{% hint style="info" %}
The shape of the `wallet` object is SDK specific. Please find the link to the API reference at the bottom of the specific crosschain SDK documentation page.
{% endhint %}

You can now check the public key of your connect wallet.

```typescript
const publicKey = instance.getAddress()
```

### Creating a single transaction

You can create transaction to send funds to addresses using the provided methods.

```typescript
const destination = "0x4d..."
const signedTx = await instance.prepareTransfer(destination, "0.1")
```

The `preparePay` method creates a transaction to transfer funds to a destination address. It also signs the transaction using the connected private key. It returns the payload ready to be used in a DEMOS transaction.

{% hint style="info" %}
The `prepareTransfer` method is an alias of the `preparePay` method.
{% endhint %}

### Creating multiple transactions

You can also create a list of transaction to transfer funds.

```typescript
const transfers = [
    {
        address: "0xf0...",
        amount: "0.1",
    },
    {
        address: "0x4f...",
        amount: "0.25",
    },
]

const signedTxs = await instance.prepareTransfers(transfers)
```

The `prepareTransfers` method creates and signs a list of transaction to transfer funds in the order of appearance.

### Cleaning up

When you no longer need the instance, disconnect the rpc and your wallet.

```ts
await instance.disconnect()
```
