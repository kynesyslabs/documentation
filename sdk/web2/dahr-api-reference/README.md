---
icon: webhook
---

# DAHR API Reference

### DAHR Class

The DAHR (Data Agnostic HTTPS Relay) class handles proxied HTTP requests with attestation. Each instance maintains its own session and provides attestation for requests made through the Demos network.

#### **Methods**

**createDahr()**

Creates a new DAHR instance:

```typescript
const dahr = await demos.web2.createDahr(): Promise<Web2Proxy>
```



**startProxy()**

Each `startProxy` call creates one on-chain web2Request transaction that stores only hashes of the response (body and headers), not the full data. After the transaction is confirmed and broadcast, the SDK returns its `txHash`.

Makes a proxied request:

```typescript
const params: IStartProxyParams {
  url: string
  method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH"
  options?: {
    headers?: OutgoingHttpHeaders
    payload?: unknown
    authorization?: string
  }
}

await dahr.startProxy(params)
```



Returns

All proxy requests return an `IWeb2Result`:

```typescript
export interface IWeb2Result {
  status: number
  statusText: string
  headers: IncomingHttpHeaders
  data: any
  dataHash: string
  headersHash: string
  txHash?: string
}
```
