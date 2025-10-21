---
description: >-
  This chapter explains in details how the L2PS (also called Subnet) Framework
  works and what is the principle behind it.
icon: chart-network
---

# L2PS (Subnet) Framework

An L2PS (or Demos Subnet) is a shard of Demos nodes that share a cryptographic secret such as an RSA keypair and is able to exchange private informations across the network.

#### Why subnets

It is called a subnet because only the subnet partecipants are able to decode the messages. On top of this, only the subnet partecipants will store all the l2ps encrypted transactions, while the broader network will only store the hash of each l2ps encrypted transactions array to verify is consistent.

This is ensured by a general Block class for the whole chain:

```typescript
export interface BlockContent {

	[...]

	l2ps_partecipating_nodes: Map<string, Map<string, string>> // ? "l2ps_uid": {"public_key": "connection_string"}
	
	l2ps_banned_nodes: Map<string, string> // ? "l2ps_uid": "public_key" (to implement)
	
	encrypted_transactions_hashes: Map<string, string> // ? "l2ps_uid": "hash"
}
```

And an extension of the class specific for L2PS Partecipants:

```typescript
// Partecipating nodes to the L2PS will have the full transactions (encrypted) of the L2PS

export interface L2PSBlockExtension extends BlockContent {

	l2ps_transactions: EncryptedTransaction[]

}
```

