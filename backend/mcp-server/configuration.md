# Configuration

The MCP server is configured through environment variables in your `.env` file:

{% code title="Environment Configuration" overflow="wrap" lineNumbers="true" %}
```bash
# MCP Server Configuration
MCP_ENABLED=true              # Enable/disable MCP server (default: true)
MCP_SERVER_PORT=3001          # Preferred port for MCP server (default: 3001)
# Alternative port override
RPC_MCP_PORT=3001             # Alternative way to set MCP port
```
{% endcode %}
