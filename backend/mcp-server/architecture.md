# Architecture

The MCP server is integrated into the main node process following the same patterns as the signaling server:

{% code title="Node Integration Pattern" overflow="wrap" lineNumbers="true" %}
```typescript
// From src/index.ts - MCP server startup
if (indexState.MCP_ENABLED) {
    try {
        const { createDemosMCPServer, createDemosNetworkTools } = await import("./features/mcp")
        
        // Get available port
        indexState.MCP_SERVER_PORT = await getNextAvailablePort(indexState.MCP_SERVER_PORT)
        
        // Create server with SSE transport for remote access
        const mcpServer = createDemosMCPServer({
            transport: "sse",
            port: indexState.MCP_SERVER_PORT,
            host: "localhost"
        })
        
        // Add all Demos Network tools
        const tools = createDemosNetworkTools()
        tools.forEach(tool => mcpServer.registerTool(tool))
        
        await mcpServer.start()
        
        // Track in state
        indexState.mcpServer = mcpServer
        getSharedState.isMCPServerStarted = true
        console.log(`[MAIN] MCP server started on port ${indexState.MCP_SERVER_PORT}`)
    } catch (error) {
        console.log("[MAIN] Failed to start MCP server:", error)
        getSharedState.isMCPServerStarted = false
        // Continue without MCP (failsafe)
    }
}
```
{% endcode %}
