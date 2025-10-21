---
icon: phone
---

# NodeCalls

In DEMOS, a NodeCall is a request that reads the blockchain state. NodeCall methods on the WebSDK are denoted by the "get" prefix. eg. `getLastBlockNumber`

## Blocks

### Get last block number

Retrieves the number of the latest block in the blockchain.

```typescript
const blockNo = await demos.getLastBlockNumber()
console.log("Last block No: ", blockNo)
```

### Get last block hash

Retrieves the hash of the latest block in the blockchain.

```typescript
const latestBlockHash = await demos.getLastBlockHash();
console.log("Latest block hash:", latestBlockHash);
```

### Get block by number

Retrieves a block by its number.

```typescript
const blockNumber = 1000;
const blockData = await demos.getBlockByNumber(blockNumber);
console.log("Block data:", blockData);
```

### Get block by hash

Retrieves a block by its hash.

```typescript
const blockHash = "0x1234...";
const blockData = await demos.getBlockByHash(blockHash);
console.log("Block data:", blockData);
```



## Transactions

### Get transaction by hash

Retrieves a transaction by its hash.

```typescript
const txHash = "0xabcd...";
const txData = await demos.getTxByHash(txHash);
console.log("Transaction data:", txData);
```

### Get all transactions

Retrieves all transactions in the blockchain.

```typescript
const allTransactions = await demos.getAllTxs();
console.log("All transactions:", allTransactions);
```



## Addresses

### Get address info

Retrieves information about a specific address on the blockchain.

```typescript
const address = "0x1234...";
const addressInfo = await demos.getAddressInfo(address);
console.log("Address info:", addressInfo);
```



## Peer information

### Get node identity

Retrieves the identity information of the connected node.

```typescript
const peerIdentity = await demos.getPeerIdentity();
console.log("Peer identity:", peerIdentity);
```

### Get peer list

Retrieves the list of peers connected to the RPC node.

```typescript
const peerList = await demos.getPeerlist();
console.log("Peer list:", peerList);
```

### Get Mempool

Retrieves the current mempool (pending transactions) of the node.

```typescript
const mempool = await demos.getMempool();
console.log("Mempool:", mempool);
```

### API Reference

[https://kynesyslabs.github.io/demosdk-api-ref/variables/websdk.demos.html](https://kynesyslabs.github.io/demosdk-api-ref/variables/websdk.demos.html)
