---
icon: play
---

# Quick Start

The Web2 proxy system enables HTTP requests through the Demos network, providing privacy and attestation capabilities through DAHR (Data Agnostic HTTPS Relay).

### Basic Setup

```typescript
import { Demos } from "@kynesyslabs/demosdk/websdk"

// Connect to demos
const demos = new Demos()
await demos.connect("https://demosnode.discus.sh")
await demos.connectWallet(mnemonic)
```

### Making Your First Request

```typescript
// Create DAHR instance
const dahr = await demos.web2.createDahr()

// Make request
const response = await dahr.startProxy({
    url: "https://api.example.com",
    method: "GET",
})

// Do something with the response
console.log("Response:", response)
```
