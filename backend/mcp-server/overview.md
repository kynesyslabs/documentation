# Overview

MCP (Model Context Protocol) is an open standard that allows AI assistants to connect to external data sources and tools. The Demos Network MCP integration provides:

* **Dual Transport Support**: stdio for local applications, SSE for remote network access
* **Comprehensive Tools**: blockchain queries, network monitoring, and peer management
* **Production Ready**: Full error handling, logging, and security considerations
* **Type Safe**: Complete TypeScript support with runtime validation

The MCP server is automatically started when you run your Demos Network node (`src/index.ts`). The integration follows these steps:

1. **Environment Configuration**: Loads MCP settings from environment variables
2. **Port Management**: Automatically selects available ports using the same system as other services
3. **Failsafe Design**: Node continues running even if MCP server fails to start
4. **State Tracking**: MCP server status is tracked in shared state for monitoring
