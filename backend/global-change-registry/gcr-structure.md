# GCR Structure

The following schema shows the internal database structure of the GCR.

The GCR Is comprised of three tables and a metatable.

<figure><img src="../../.gitbook/assets/GCRStructure.drawio.png" alt=""><figcaption><p>GCR Structure</p></figcaption></figure>

### global\_change\_registry

This is the primary table where the essential properties of a Demos account within the network are stored. Note that the `details` row, which is stored in an optimized JSONB format, contains the foundational properties linked to a Demos address.

The `extended` property simplifies tracking tokens, NFTs, and cross-context properties and operations linked to an address. It is a JSONB field too, allowing for efficient data management and lower overhead.

### global\_change\_registry\_subnets\_txs

This table is responsible for holding and indexing all the transactions that happens in a [Subnet](../l2ps-subnet-framework/). Note that `tx_data` contains the encrypted data for that specific Subnet's tx and can only be decrypted by partecipants of the Subnet itself. See [how-are-l2ps-transactions-handled.md](../l2ps-subnet-framework/how-are-l2ps-transactions-handled.md "mention") for more informations.

### gcr\_tracker

This table contains the hashes of each user's `global_change_registry` entry. Each time a GCR entry is modified, for example after a transaction, its `gcr_tracker` is updated too with the current hash of that table. This allows for fast, efficient and optimized tracking of the changes in the GCR.

### gcr\_hashes

This table is separate from the GCR data. As a metadata table, it stores the combined hashes of the `global_change_registry_subnets_txs` and `gcr_tracker` tables to generate a GCR Status hash. This is crucial for verifying the consistency of GCR statuses during synchronization and consensus processes.
