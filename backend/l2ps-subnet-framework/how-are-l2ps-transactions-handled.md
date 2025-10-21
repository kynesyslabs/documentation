---
description: >-
  This page describes in details how Demos network stores, manages and serves
  encrypted transactions within a L2PS (or subnet).
---

# How are L2PS transactions handled?

The Demos specification includes a table in the Demos blockchain database, which, as part of the Global Change Registry, is synchronised across nodes and certified by consensus.

The table is structured as follows:

```typescript

@Entity("global_change_registry_subnets_txs")
export class GCRSubnetsTxs {
    @PrimaryColumn("text", { name: "tx_hash" })
    tx_hash: string

    @Column("text", { name: "subnet_id" })
    subnet_id: string

    @Column("text", { name: "status" })
    status: string

    @Column("text", { name: "block_hash" })
    block_hash: string

    @Column("integer", { name: "block_number" })
    block_number: number

    @Column("json", { name: "tx_data"})
    tx_data: EncryptedTransaction
}
```

As we saw in the previous chapter, each block contains a list of encrypted transactions that are part of one or more subnets. This list is used as a reference to quickly locate L2PS transactions within a block. To actually retrieve an encrypted transaction, the SDK provides methods to retrieve them from the table above.

You can quickly retrieve L2PS transactions by searching for the block number, block hash, status, subnet ID (aka public key) or tx hash. As always, the demo network only stores encrypted transactions to ensure privacy and confidentiality. However, it is easy to actually attest and verify that a transaction has been validated with a particular hash and therefore its content.

### User Experience

From a user's point of view, this means that using any dApp or program that uses the SDK to make use of subnets will cause its own transactions to be applied in the table above. This concept is particularly useful for visualising how the demo network guarantees L2PS functionality.

### Node Experience

As discussed in the previous chapter, nodes that participate in a L2PS will be the ones that actually store the txs in the status\_subnets\_txs table. A node not participating in a L2PS will only be able to provide hash references through the usual block content.
