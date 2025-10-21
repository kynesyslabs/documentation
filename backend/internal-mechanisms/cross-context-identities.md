---
description: >-
  Cross-Context Identities are the specifications utilized by the Demos network
  to identify and capitalize on accounts situated across diverse chains and
  protocols, including the Web2 protocol.
icon: face-viewfinder
---

# Cross Context Identities

Demos Network employs a variety of techniques for different chains and protocols, which is a core aspect of numerous Demos protocol mechanisms, including the Gas Tanks mechanism and the overall reputation score for a node or user.

The primary mechanism for achieving this is known as Cross Context Identities (CCI).

Within the blockchain, specifically in the StatusNative table of the database, each address is associated with a JSON object called "identities." This serves as a registry for the user's various identities in different contexts.

The json structure is as follows:

````
```typescript

    @Column("json", { name: "identities", nullable: true })
    identities: StoredIdentities | null = new Map() // NOTE This is a map of the public identifiers and the context
```
````

The `StoredIdentities` type is defined as follows:

````
```typescript
type Identity = { // NOTE This supports both chains and web2 contexts
    public_identifier: string
    context: "xm" | "web2"
}

type StoredIdentities = Map<string, Identity> // NOTE The key is the network name or the web2 context name

```
````

Upon each user transaction on a different chain or context (e.g., a [cross-chain](../../sdk/cross-chain/ "mention") transaction or a Web2 transaction involving an API key), the public portion of that identity is saved inside the aforementioned table.

It should be noted that the private key or API key is not stored on the blockchain. Instead, it is stored locally, if specified, through the use of wallets or dApps that utilize the Demos SDK.

### Leveraging identities

This approach offers a significant advantage in managing multiple identities. To illustrate, consider a scenario where User A wishes to execute a Demos transaction, paying gas with their Solana native tokens.

As the user has already interacted with Demos using Solana (e.g., a [cross-chain](../../sdk/cross-chain/ "mention") transaction), the blockchain is aware of its Solana public key. The RPC will then request a Solana payment from A to one of our designated gas tanks and will verify that A's public key has successfully completed the transaction. Once this is confirmed, the RPC can proceed with the execution.

#### It's all SDK

It is important to note that the process described can and should ideally be automatic. Once A has its local Demos wallet with its Solana identity loaded (so without sharing the private key with the blockchain but keeping it locally), the wallet is perfectly able to execute the transaction autonomously after a quick confirmation by the user. This allows for a seamless and easy cross-context system to be applied and executed without hassle.

#### Example Schema

<figure><img src="../../.gitbook/assets/CCI_gas_tanks.png" alt=""><figcaption><p>Leveraging CCI for Gas Tanks</p></figcaption></figure>
