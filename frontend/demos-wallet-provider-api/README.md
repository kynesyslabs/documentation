# Demos Wallet Provider API

### Provider Interface

The injected provider exposes a small surface:

* `provider.request({ method, params? })`: Generic RPC-style method. Preferred for all interactions.
* `provider.accounts() → Promise<{ code: 404|401|200, data: string|null }>`: Returns account status/address, used primarily for discovery gating.

The provider posts messages into the page. Internally, they are forwarded to the extension background and resolved back into a unified response:

```typescript
export default interface DemosProviderResponse {
    id: string;
    type: "demosProviderResponse";
    method: string;        // echoes requested method
    success: boolean;
    data?: any;
    error?: {
        code: string;
        message: string;
        details?: any;
    }
}
```

### Supported Methods

See all supported methods here: [wallet-provider-api-methods.md](wallet-provider-api-methods.md "mention")

### Usage Examples

Connect and get xM addresses:

```javascript
window.dispatchEvent(new Event('demosRequestProvider'));
window.addEventListener('demosAnnounceProvider', async (evt) => {
  const provider = evt.detail.provider;

  // Optional: discover account status
  const accounts = await provider.accounts();
  if (accounts.code !== 200) {
    const res = await provider.request({ method: 'connect' });
    if (!res.success) throw new Error(res.error?.message ?? 'Connect failed');
  }

  const result = await provider.request({ method: 'getXmIdentities' });
  console.log(result.success ? result.data : result.error);
});
```

Send a transaction:

```javascript
const tx = await provider.request({
  method: 'nativeTransfer',
  params: [{ amount: 1, recipientAddress:"0x..." }],
});
if (!tx.success) {
  // handle tx.error.code/message
}
```

Add a Twitter identity (shape defined by SDK `TwitterProof`):

```javascript
const proof = /* obtain TwitterProof via your backend/SDK */
const res = await provider.request({ method: 'addTwitterIdentity', params: [proof] });
```

### Error Semantics

Common error codes surfaced in `response.error.code`:

* `TIMEOUT`: popup not resolved before timeout
* `POPUP_ERROR`: could not open popup
* `...Cancelled`: user closed popup (`validationCancelled`, `addTwitterIdentityCancelled`, etc.)
* Method-specific errors (e.g., `addGithubIdentityError`, `sendTransactionError`) include `details` when available

### Notes

* The extension only announces the provider after `provider.accounts()` indicates a non-404 status.
* Always prefer `provider.request` with the methods above for forward-compatibility.
