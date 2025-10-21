---
description: >-
  This document specifies how a Demos DApp should discover Demos providers
  injected via browser extension. This solution is inspired by Ethereum's
  EIP-6963.
---

# Demos Providers Discovery Mechanism

## Mechanism

This mechanism allows for the discovery of multiple providers without race conditions. The injected providers communicate with the DApp through window events. When the DApp needs the list of available providers, it sends a "request" event. When a request is triggered, the providers must send an "announce" event. It follows that the DApp and the providers must be listening for, respectively, "announce" and "request" events.

## Request

```typescript
interface DemosRequestProviderEvent extends Event{
    type:"demosRequestProvider",
}
```

## Announce

```typescript
interface DemosAnnounceProviderEvent extends CustomEvent{
    type:"demosAnnounceProvider",
    detail: DemosProviderDetail;
}
```

### DemosProviderDetail

```typescript
interface DemosProviderDetail {
    info: DemosProviderInfo;
    provider: DemosProvider;
}
```

### DemosProviderInfo

```typescript
export default interface DemosProviderInfo {
    uuid: string;
    name: string;
    icon: string;
    url: string;
}
```













