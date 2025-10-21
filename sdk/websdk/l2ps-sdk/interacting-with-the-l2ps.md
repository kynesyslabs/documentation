---
icon: network-wired
---

# Interacting with the L2PS

The `l2ps`module exposes various methods to easily interact with on-chain Subnets.

As Subnets are always registered on the Demos Network, their data is publicly available. Due to the strong encryption, anyway, only their members are able to decrypt and view the content of that data.

This mechanism is crucial to ensure data integrity while not compromising privacy and security.

For this reason, once a Subnet instance is created, it will be able to interact with the on-chain data pertaining to that specific Subnet.

All the following methods are to be called from the `L2PS`class instance you created in the previous step (for example: `await instance.getParticipatingNodes()`).

{% hint style="info" %}
This section mainly explains the primitives to interact with a L2PS Subnet. In the following chapters, we will see more high level modules using this class to expose features in a user-friendly way.
{% endhint %}

### getParticipatingNodes

This method retrieves the members, also called nodes, of the Subnet instance updated to the last block.

_Arguments_: None

_Returns_: `Promise<Map<string, string>>`

### getTx

This method retrieves an encrypted transaction from the on-chain Subnet, decrypts it and returns the plain Transaction.

_Arguments_:`eHash: string // the hash of the encrypted transaction`

_Returns_: `Promise<Transaction>`

### registerTx

This method accepts a standard Demos Transaction, encrypts it using the L2PS Public Key and send it to the on-chain Subnet instance.

_Arguments_: `tx: Transaction // A standard Demos Transaction`

_Returns_: `Promise<string> // The eHash of the encrypted Transaction`
