# Client Usage

### Connecting to the MCP Server

#### Remote Access (SSE Transport)

The node starts the MCP server with SSE transport by default, making it accessible remotely:

{% code title="MCP Server Connection" overflow="wrap" lineNumbers="true" %}
```typescript
// Connect to your running Demos Network node's MCP server
const serverUrl = "http://localhost:3001"  // Use your node's MCP port

// For SSE (remote) connections:
// SSE endpoint: http://localhost:3001/sse
// Message endpoint: POST http://localhost:3001/message
```
{% endcode %}

#### Local Access (stdio Transport)

For local development, you can also create a separate stdio MCP server:

{% code title="Local MCP Development" overflow="wrap" lineNumbers="true" %}
```typescript
import { createDemosMCPServer, createDemosNetworkTools } from "@/features/mcp"

// Create a separate stdio server for development
const devServer = createDemosMCPServer({
    transport: "stdio"  // For local development tools
})

const tools = createDemosNetworkTools()
tools.forEach(tool => devServer.registerTool(tool))

await devServer.start()
```
{% endcode %}
