# Storage Program Operations

> **Warning**: Storage Programs are still being developed; this documentation is a preview and might not work correctly.

This guide explains how each Storage Program operation fits into an end-to-end workflow. For method signatures, payload schemas, and error codes, rely on the [API Reference](./api-reference.md). For concrete implementation patterns, see the [Storage Program Cookbook](../cookbook/storage-programs/examples.md).

## Operation Overview

| Operation | Transaction? | Who Can Execute | Typical Use |
|-----------|--------------|-----------------|-------------|
| `create` | ✅ Yes | Any deployer | Provision a new storage namespace with optional data |
| `write` | ✅ Yes | Deployer + allowed addresses | Merge updates into existing data |
| `granularWrite` | ✅ Yes | Deployer + allowed addresses | Field-level modifications (set, append, delete) |
| `read` | ❌ No (RPC) | According to access mode | Fetch storage content or metadata |
| `granularRead` | ❌ No (RPC) | According to access mode | Field-level queries (get field, check exists, get type) |
| `updateAccessControl` | ✅ Yes | Deployer only | Change access mode and/or allowlist |
| `delete` | ✅ Yes | Deployer only | Remove a storage program and its data |

## Create

**Goal**: Materialise a deterministic `stor-` address on-chain and (optionally) seed initial state.

**Workflow**
1. Derive the address client-side (reuse salts if you need different versions).
2. Validate payload size (`<128KB`) and nesting before submitting a transaction.
3. Submit `create` with the desired access mode and optional `allowedAddresses`.
4. Wait for consensus confirmation if the caller depends on the program immediately.

**Pre-flight checks**
- Restricted mode must include at least one allowlisted address.
- Decide whether to encrypt sensitive fields up front; the network stores JSON as-is.

**References**: [API Reference – create](./api-reference.md#sdk-methods), [Cookbook – provisioning flows](../cookbook/storage-programs/examples.md).

## Write

**Goal**: Merge new key/value pairs or nested data into the existing JSON document.

**Workflow**
1. Fetch current state if you need to apply deltas (reads are free).
2. Construct a payload that only includes the keys you intend to update.
3. Submit a `write` transaction; consensus will merge it with the existing document.
4. Optionally re-read to confirm the write and update caches or UI state.

**Pre-flight checks**
- Combined data size after merge must remain under 128KB.
- Callers must satisfy access control (deployer or allowlisted address).
- Consider optimistic UI updates paired with a rollback path for failures.

**References**: [API Reference – write](./api-reference.md#sdk-methods), [Cookbook – update patterns](../cookbook/storage-programs/examples.md).

## Granular Write

**Goal**: Perform field-level modifications without replacing the entire dataset.

**Workflow**
1. Choose the appropriate operation type for your use case:
   - `setField`: Set or update a top-level field value
   - `setItem`: Update a specific array element by index
   - `appendItem`: Add a new item to an array field
   - `deleteField`: Remove a top-level field entirely
   - `deleteItem`: Remove an array element by index
2. Build an array of operations to execute atomically.
3. Submit a `granularWrite` transaction; operations apply in order.
4. Optionally re-read to confirm changes.

**Pre-flight checks**
- All field names must be top-level keys (nested paths not supported).
- Array indices must be within bounds for `setItem` and `deleteItem`.
- Combined data size after modifications must remain under 128KB.
- Callers must satisfy access control (deployer or allowlisted address).

**Operation Types**

| Type | Required Fields | Description |
|------|-----------------|-------------|
| `SET_FIELD` | `field`, `value` | Set a top-level field value |
| `SET_ITEM` | `field`, `index`, `value` | Update array element at index |
| `APPEND_ITEM` | `field`, `value` | Append item to array field |
| `DELETE_FIELD` | `field` | Remove a top-level field |
| `DELETE_ITEM` | `field`, `index` | Remove array element at index |

**When to use Granular Write vs Write**

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Update single field | `granularWrite` | Less bandwidth, atomic |
| Add item to array | `granularWrite` | No need to send entire array |
| Replace all data | `write` | Full replacement simpler |
| Multiple field updates | Either | Depends on change percentage |

**References**: [API Reference – granularWrite](./api-reference.md#granular-write-methods), [Cookbook – granular patterns](../cookbook/storage-programs/examples.md).

## Read

**Goal**: Retrieve storage variables or metadata over RPC with no transaction cost.

**Workflow**
1. Use `read(address)` for the full document or `read(address, key)` for scoped lookups.
2. Cache aggressively—responses include `metadata.lastModified` so you can detect changes.
3. Parallelise reads across addresses using `Promise.all` when fetching many programs.

**Pre-flight checks**
- Ensure the caller has read permission under the current access mode.
- Treat responses as eventually consistent; pair with webhooks/polling if you need freshness.

**References**: [RPC Queries guide](./rpc-queries.md), [API Reference – read](./api-reference.md#sdk-methods).

## Granular Read

**Goal**: Query specific fields, check field existence, or get field types without fetching the entire document.

**Workflow**
1. Choose the appropriate granular read method:
   - `getFields()`: List all top-level field names
   - `getValue(field)`: Get a specific field's value
   - `getItem(field, index)`: Get an array element by index
   - `hasField(field)`: Check if a field exists
   - `getFieldType(field)`: Get the type of a field's value
   - `getAll()`: Get all data (equivalent to `read()`)
2. Use the appropriate method based on what information you need.
3. Cache results using field names and types for efficient subsequent queries.

**Pre-flight checks**
- Ensure the caller has read permission under the current access mode.
- For array operations, verify the field is actually an array first using `getFieldType()`.

**Available Methods**

| Method | Returns | Use Case |
|--------|---------|----------|
| `getFields()` | `string[]` | Discover available data structure |
| `getValue(field)` | `any` + `type` | Read single field efficiently |
| `getItem(field, index)` | `any` | Access array elements directly |
| `hasField(field)` | `boolean` | Check before accessing |
| `getFieldType(field)` | `StorageFieldType` | Type validation before operations |
| `getAll()` | Full data | When you need everything |

**Field Types**

| Type | Description |
|------|-------------|
| `string` | Text value |
| `number` | Numeric value (integer or float) |
| `boolean` | True or false |
| `array` | Ordered list of values |
| `object` | Key-value mapping |
| `null` | Null value |
| `undefined` | Field exists but value is undefined |

**When to use Granular Read vs Read**

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Need one field | `getValue()` | Reduced bandwidth |
| Check field exists | `hasField()` | Lightweight check |
| Iterate array | `getItem()` | No need to fetch entire array |
| Full document | `read()` | Single request for everything |
| Explore structure | `getFields()` | Discover available data |

**References**: [RPC Queries guide](./rpc-queries.md), [API Reference – granularRead](./api-reference.md#granular-read-methods).

## Update Access Control

**Goal**: Switch access modes or adjust the allowlist for restricted programs.

**Workflow**
1. Read `metadata` to confirm deployer address and current configuration.
2. Build the desired change:
   - `accessControl: "private" | "public" | "restricted" | "deployer-only"`
   - `allowedAddresses: string[]` (complete list, not patches)
3. Submit the `updateAccessControl` transaction.
4. Notify affected clients (e.g., flush caches, inform collaborators).

**Pre-flight checks**
- Only the deployer may call this method.
- Restricted mode requires a non-empty allowlist.
- When opening data (restricted → public), review contents to avoid leaking secrets.

**References**: [Access Control guide](./access-control.md), [API Reference – updateAccessControl](./api-reference.md#sdk-methods).

## Delete

**Goal**: Remove an entire Storage Program, including variables and metadata.

**Workflow**
1. Confirm that no downstream systems rely on the existing data (deletion is irreversible).
2. Submit a `delete` transaction from the deployer address.
3. Update any application indexes or caches that referenced the storage address.

**Pre-flight checks**
- Only the deployer can delete.
- Communicate the removal to collaborators or users to prevent dangling references.

**References**: [API Reference – delete](./api-reference.md#sdk-methods), [Cookbook – teardown routines](../cookbook/storage-programs/examples.md).