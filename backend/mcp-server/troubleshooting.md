# Troubleshooting

#### Common Issues

**MCP Server Not Starting**

* Check if port 3001 is available or change `MCP_SERVER_PORT` in your environment
* Verify `MCP_ENABLED=true` in your `.env` file
* Check node logs for MCP startup errors

**Can't Connect to MCP Server**

* Verify the node is running and MCP server started successfully
* Check the `/mcp` status endpoint: `curl http://localhost:53550/mcp`
* Ensure firewall allows connections to the MCP port

**Tools Not Working**

* Verify the node is fully synced and operational
* Check that blockchain data is accessible
* Review MCP server logs for tool execution errors

#### Debug Mode

Enable debug logging for MCP operations:

{% code title="Debug Configuration" overflow="wrap" lineNumbers="true" %}
```bash
# Add to your .env file
DEBUG=mcp:*
MCP_LOG_LEVEL=debug
```
{% endcode %}
