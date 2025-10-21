---
icon: square-n
---

# NEAR

NEAR is a user-friendly, scalable layer-1 blockchain platform that uses a sharded proof-of-stake consensus mechanism. It features human-readable account names, supports smart contracts in Rust and AssemblyScript, and offers low transaction fees.

### Core Concepts

1. [Account IDs](https://docs.near.org/concepts/protocol/account-id)
2. [Access Keys](https://docs.near.org/concepts/protocol/access-keys)
3. [Anatomy of a Transaction](https://docs.near.org/concepts/protocol/transaction-anatomy)
4. [Lifecycle of a Transaction](https://docs.near.org/concepts/protocol/transaction-execution)

### Setting up your wallet

Use the [Meteor Wallet](https://wallet.meteorwallet.app) to create a Near account. Then go to `Settings > Security and Recovery > Export Private Key` to copy your private key.

Use the [Near Testnet Faucet](https://near-faucet.io) to airdrop fund your testnet wallet.

### Using the SDK

### Initialization

Import the SDK and create a new instance:

```ts
import { NEAR } from "@kynesyslabs/demosdk/xm-websdk"

const rpc_url = "https://rpc.testnet.near.org"
const networkId = "testnet"

const instance = await NEAR.create(rpc_url, networkId)
```

You can then use the instance to do a read operation on near.

```ts
const balance = await instance.getBalance("cwilvx.testnet")
console.log(`Balance: ${balance}Ⓝ`)
```

### Connecting your wallet

To perform token transfers or other transactions, you need to connect your wallet to the SDK. You also need to provide the accountId to be associated with your private key.

```ts
await instance.connectWallet(
    "ed25519:4QRNiJk7A584sU3aV1xhqdbdairYJybjHJq9z78s7ntw2JVeBYybZ4r4Ec",
    {
        accountId: "cwilvx.testnet",
    },
)
```

You can view the address of your connected wallet using the `getAddress` method.

```ts
const address = instance.getAddress()
console.log(`Address: ${address}`)
```

### Token transfer

To create a transaction to transfer Ⓝ on near, you can use the `preparePay` or `prepareTranfer` methods:

```ts
const signedTx = await instance.preparePay("cwilvx.testnet", "1.5")
```

The signed tx is a `Uint8Array` that can be used in a XM work step.

### Signing Messages

```javascript
const message = "Hello, world!"

// Signing
const signature = await instance.signMessage(message)
console.log(signature)

// Verifying signature
const verified = await instance.verifyMessage(
    message,
    signature,
    instance.getAddress(),
)

expect(verified).toBe(true)
```

### Creating accounts

You can call the `createAccount` method to create an account, passing the accountId and the Ⓝ amount to deposit to the created account. You can optionally specify the curve to use when generating the key pair for the new account.

```ts
const { keyPair, signedTx } = await instance.createAccount(
    "other.me.testnet",
    "1",
)

console.log(keyPair.getPublicKey().toString())
```

The method returns the signed transaction for creating the new account on Near, and its key pair.

### Deleting accounts

You can delete the connected account by calling the `deleteAccount` method and passing the NEAR account that will receive the remaining Ⓝ balance from the account being deleted.

```ts
const signedTx = await instance.deleteAccount("cwilvx.testnet")
```

### Hacking

To create custom transactions for the Near blockchain using the Demos Near SDK, you can access the underlying API to create transactions.

<table><thead><tr><th>Method</th><th>Description</th><th data-hidden data-type="number">#</th></tr></thead><tbody><tr><td><code>instance.actions</code></td><td>Transaction Actions</td><td>1</td></tr><tr><td><code>instance.provider</code></td><td>The <a href="https://near.github.io/near-api-js/classes/_near_js_wallet_account.near.Near.html">near class instance</a> provided by <code>near-api-js</code></td><td>2</td></tr><tr><td><code>instance.wallet</code></td><td>Your connected <a href="https://near.github.io/near-api-js/classes/_near_js_crypto.key_pair.KeyPair.html">KeyPair</a></td><td>3</td></tr><tr><td><code>instance.signer</code></td><td>The <a href="https://near.github.io/near-api-js/classes/_near_js_signers.in_memory_signer.InMemorySigner.html">signer</a> for your connected <a href="https://near.github.io/near-api-js/classes/_near_js_crypto.key_pair.KeyPair.html">KeyPair</a></td><td>4</td></tr><tr><td><code>instance.signTransaction(s)</code></td><td>Sign transactions</td><td>5</td></tr></tbody></table>

### Resources

Here's the converted list with markdown links:

* [Near Website](https://near.org)
* [Near Testnet Faucet](https://near-faucet.io)
* [Docs](https://docs.near.org)
* [Meteor Wallet](https://wallet.meteorwallet.app)
* [Near JS API Ref](https://near.github.io/near-api-js/index.html)
* [Near JS Cookbook](https://github.com/near/near-api-js/tree/master/packages/cookbook)
* [Block Explorer](https://testnet.nearblocks.io)
* [The NEAR Protocol Specification](https://nomicon.io)
