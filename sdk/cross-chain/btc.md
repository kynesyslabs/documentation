---
icon: bitcoin
---

# BTC

The Bitcoin SDK provides an interface to interact with Bitcoin blockchains using SegWit (P2WPKH) transactions. It supports wallet connectivity, transaction preparation, and balance checking, using the bitcoinjs-lib library for core functionality.

## Wallet setup

To generate new Bitcoin WIF (Wallet Import Format) private keys for **P2WPKH** wallets, you can use the following tools:

* [Bitcoin Tools](https://bitcoin-tools-blond.vercel.app/) (testnet)
* [Bitaddress.org](https://bitaddress.org/)

## Get tokens on the testnet

For testing process, you can use following links to get token on the testnet&#x20;

* [Coinfaucet](https://coinfaucet.eu/en/btc-testnet/)
* [Testnet Faucet](https://testnet-faucet.com/)

## Initialization

Import the SDK and create a new instance:

```typescript
import { BTC } from "@kynesyslabs/demosdk/xm-websdk"

const rpc_url = "https://blockstream.info/testnet/api";
const network = BTC.networks.testnet;

const instance = await BTC.create(rpc_url, network);
```

## Wallet connect

Connect your wallet using a private key in WIF format:

```typescript
const privateKeyWIF = "cTb..."; // Your WIF private key
await instance.connectWallet(privateKeyWIF);
```

You can view the connected wallet’s address using the `getAddress` method:

```typescript
const address = instance.getAddress();
console.log(`Address: ${address}`);
```

## Create payload for the token transfer

Prepare a signed transaction to transfer BTC using `preparePay` method:

```typescript
const receiverAddress = "tb1q...";
const amount = "560"; // Amount in satoshis

const signedTx = await instance.preparePay(receiverAddress, amount);
```

The `signedTx` is a hex-encoded signed transaction ready for use in a DEMOS transaction.

## Create payload for the multiple transfers

You can create multiple Bitcoin transfer payloads by using the `preparePays` method as shown:

```typescript
const transfers = [
    { address: "tb1q...", amount: "550" },
];
const signedTxs = await instance.preparePays(transfers);
```

The `signedTxs` is an array of hex-encoded signed transaction payloads.

## Checking Balance

You can check the balance of the connected wallet, including change addresses as shown:

```typescript
const balance = await instance.getBalance();
console.log(`Balance: ${balance} satoshis`);
```

## Resources

* [Bitcoin Website](https://bitcoin.org/)
* [BitcoinJS Documentation](https://github.com/bitcoinjs/bitcoinjs-lib)
* [Blockstream Explorer](https://blockstream.info/)
* [Testnet Explorer](https://blockstream.info/testnet)
