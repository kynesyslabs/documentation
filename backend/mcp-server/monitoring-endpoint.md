# Monitoring Endpoint

The node provides a dedicated `/mcp` endpoint to check MCP server status:

{% code title="MCP Status Endpoint" overflow="wrap" lineNumbers="true" %}
```bash
# Check MCP server status
curl http://localhost:53550/mcp

# Example response:
{
  "enabled": true,
  "transport": "sse",
  "status": "running"
}
```
{% endcode %}
