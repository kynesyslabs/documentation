---
icon: spider-web
---

# Web2

### What is Web2 Proxy?

The Web2 proxy system allows you to make HTTP requests through the Demos network. Requests are verified by a network of attestation nodes, ensuring data integrity and reliability. The system provides:

* Secure proxy requests through the Demos network
* Session-based request handling
* Support for all standard HTTP methods
* Custom header and payload support

### Basic Example

```typescript
import { Demos } from "@kynesyslabs/demosdk/websdk"

// Connect to demos and set up identity
const demos = new Demos()
await demos.connect("http://localhost:53550")
await demos.connectWallet(mnemonic)

// Create and use proxy
const dahr = await demos.web2.createDahr()
const response = await dahr.startProxy({
    url: "https://api.example.com",
    method: "GET",
})
```

### Key Features

* Session Management: Each proxy request is handled through a dedicated session
* Method Support: GET, POST, PUT, PATCH, DELETE
* Custom Headers: Add your own headers to requests
* Payload Support: Send data with your requests
* Authorization: Include authorization tokens when needed
