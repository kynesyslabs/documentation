# Available Tools

The MCP server automatically provides these tools when started with your node:

**Network Status Tools**

Monitor the health and status of your Demos Network node:

{% code title="Network Status Example" overflow="wrap" lineNumbers="true" %}
```typescript
// Available network tools:
// - get_network_status: Get comprehensive network status
// - get_node_identity: Get node identity and public key info

// Example usage (through MCP client):
const networkStatus = await mcpClient.callTool("get_network_status", {})
console.log("Server port:", networkStatus.serverPort)
console.log("Connection string:", networkStatus.connectionString)
console.log("Last block:", networkStatus.lastBlockNumber)

const nodeIdentity = await mcpClient.callTool("get_node_identity", {})
console.log("Public key:", nodeIdentity.publicKey)
console.log("Public IP:", nodeIdentity.publicIP)
```
{% endcode %}

**Blockchain Query Tools**

Access blockchain data and query block information:

{% code title="Blockchain Tools Example" overflow="wrap" lineNumbers="true" %}
```typescript
// Available blockchain tools:
// - get_last_block: Get the most recent block
// - get_block_by_number: Get a specific block by number
// - get_chain_height: Get current blockchain height

// Example usage (through MCP client):
const lastBlock = await mcpClient.callTool("get_last_block", {})
console.log("Latest block number:", lastBlock.number)
console.log("Block hash:", lastBlock.hash)

const specificBlock = await mcpClient.callTool("get_block_by_number", {
    blockNumber: 100
})
console.log("Block 100 details:", specificBlock)

const chainHeight = await mcpClient.callTool("get_chain_height", {})
console.log("Current chain height:", chainHeight.height)
```
{% endcode %}

**Peer Management Tools**

Monitor and manage network peer connections:

{% code title="Peer Management Example" overflow="wrap" lineNumbers="true" %}
```typescript
// Available peer tools:
// - get_peer_list: Get detailed list of connected peers
// - get_peer_count: Get current number of connected peers

// Example usage (through MCP client):
const peerList = await mcpClient.callTool("get_peer_list", {})
console.log("Connected peers:", peerList.peerCount)
peerList.peers.forEach(peer => {
    console.log(`Peer: ${peer.identity} at ${peer.connectionString}`)
})

const peerCount = await mcpClient.callTool("get_peer_count", {})
console.log("Total peers:", peerCount.peerCount)
```
{% endcode %}
