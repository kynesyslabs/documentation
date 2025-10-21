---
icon: keyboard
---

# Types

### HTTP Methods

The Web2 proxy supports standard HTTP methods through the `Web2Method` type:

```typescript
type Web2Method = "GET" | "POST" | "PUT" | "DELETE" | "PATCH"
```

### Request Parameters

When making requests through the proxy, use the `IStartProxyParams` interface to structure your request:

```typescript
interface IStartProxyParams {
    url: string                        // Target URL
    method: Web2Method                 // HTTP method to use
    options?: {                        // Optional parameters
        headers?: OutgoingHttpHeaders  // Request headers (string | string[])
        payload?: any                  // Request body (POST/PUT/PATCH)
        authorization?: string         // Bearer token (if required)
    }
}
```

### Response Types

`txHash` is added by the SDK after confirm/broadcast; node responses may omit it. Only hashes (dataHash, headersHash) are stored on-chain; not the full response.

Response type from `startProxy`:

```typescript
interface IWeb2Result {
  status: number                 // HTTP status code
  statusText: string             // Status message
  headers: IncomingHttpHeaders   // Response headers (string | string[])
  data: any                      // Response data
  responseHash: string           // SHA-256 of response body
  responseHeadersHash: string    // SHA-256 of response headers
  requestHash?: string           // Optional SHA-256 of request body
  txHash?: string                // Optional On-chain tx hash (SDK attaches after broadcast)
}
```

### Usage Examples

#### Handling Responses

```typescript
const response = await dahr.startProxy({
  url: "https://postman-echo.com/get?test=1",
  method: "GET",
  options: {
    headers: { Accept: ["application/json", "text/plain"] },
    authorization: "my-token-if-needed",
  },
})

// HTTP response + hashes + tx hash (returned by SDK)
console.log(res.status, res.statusText)
console.log(res.dataHash, res.responseHeadersHash)
console.log(res.txHash) // can be verified on-chain

// Verify on-chain (optional)
if (res.txHash) {
  const tx = await demos.getTxByHash(res.txHash)
  console.log(!!tx ? "On-chain tx found" : "Tx not found")
}
```
