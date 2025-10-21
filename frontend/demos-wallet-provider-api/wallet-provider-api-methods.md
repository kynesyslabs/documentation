# Wallet Provider API methods

Call each via `provider.request({ method: '<name>', params: [...] })` unless noted otherwise.

#### Common error codes

* **TIMEOUT**: popup not resolved before timeout
* **POPUP\_ERROR**: could not open popup
* **...Cancelled**: user closed popup (e.g., `validationCancelled`, `addTwitterIdentityCancelled`)
* Method-specific errors (e.g., `nativeTransferError`, `sendTransactionError`), with optional `details`

## Connection

#### connect

* **Params**: none
* **Behavior**: opens a connection popup; user approves/denies.
* **Success data**: `{ address: string }`
* **Errors**: `connectionDenied`, `connectionCancelled`, `TIMEOUT`, `POPUP_ERROR`

Example:

```ts
const res = await provider.request({ method: 'connect' });
if (res.success) {
  console.log('Connected address:', res.data.address);
}
```

## Transactions

These let your dApp construct transactions (or messages) and have the wallet sign and/or broadcast them.

#### sign

* **Params**: `[ message: string ]`
* **Behavior**: opens a sign popup for a plain message.
* **Success data**: `{ signature: string }` (wrapped by the wallet; underlying object includes `{ success: true, signature }`)
* **Errors**: `signError`, `signCancelled`, `TIMEOUT`, `NOT_LOGGED_IN`

Example:

```ts
const res = await provider.request({ method: 'sign', params: ['hello world'] });
```

#### signTransaction

* **Params**: `[ unsignedTransaction: Transaction ]`
* **Behavior**: opens a sign-transaction popup and returns the signed transaction.
* **Success data**: `{ signedTransaction }` (wrapped; underlying object includes `{ success: true, signedTransaction }`)
* **Errors**: `signTransactionError`, `signTransactionCancelled`, `TIMEOUT`, `NOT_LOGGED_IN`

Example:

```ts
const unsignedTx = {/* Transaction from SDK */};
const res = await provider.request({ method: 'signTransaction', params: [unsignedTx] });
```

#### sendTransaction

* **Params**: `[ transaction: Transaction ]`
* **Behavior**: signs the transaction, validates it, opens validation popup; on confirmation, broadcasts.
* **Success data**: `{ result, validityData }`
* **Errors**: `sendTransactionError`, `sendTransactionCancelled`, `TIMEOUT`, `POPUP_ERROR`

Example:

```ts
const tx = {/* Transaction from SDK */};
const res = await provider.request({ method: 'sendTransaction', params: [tx] });
```

#### sendSignedTransaction

* **Params**: `[ signedTransaction: Transaction ]`
* **Behavior**: validates the signed transaction, opens validation popup; on confirmation, broadcasts.
* **Success data**: `{ result, validityData }`
* **Errors**: `sendSignedTransactionError`, `sendSignedTransactionCancelled`, `TIMEOUT`, `POPUP_ERROR`

Example:

```ts
const signedTx = {/* signed Transaction from SDK */};
const res = await provider.request({ method: 'sendSignedTransaction', params: [signedTx] });
```

## Transaction helpers

These will construct, validate and broadcast transactions directly inside the wallet by passing the required parameters.

#### nativeTransfer

* **Params**: `[ { recipientAddress: string, amount: number } ]`
* **Behavior**: creates a transfer, validates it, then opens validation popup for user confirmation and broadcast.
* **Success data**: `{ result, validityData }`
* **Errors**: `nativeTransferError`, `nativeTransferCancelled`, `TIMEOUT`, `POPUP_ERROR`

Example:

```ts
const res = await provider.request({
  method: 'nativeTransfer',
  params: [{ recipientAddress: '0xabc...', amount: 1 }],
});
```

### Identity

#### getXmIdentities

* **Params**: none
* **Success data**: list of identities from SDK
* **Errors**: `getXmIdentitiesError`

Example:

```ts
const res = await provider.request({ method: 'getXmIdentities' });
```

#### addXmIdentity

* **Params**: `[payload: InferFromSignaturePayload]`
* **Behavior**: infers and validates identity, then prompts user in validation popup; upon confirmation broadcasts.
* **Success data**: `{ result, validityData }`
* **Errors**: `addXmIdentityError`, `addXmIdentityCancelled`, `TIMEOUT`

Example:

```ts
const payload = /* build InferFromSignaturePayload */
const res = await provider.request({ method: 'addXmIdentity', params: [payload] });
```

#### removeXmIdentity

* **Params**: `[payload: XMCoreTargetIdentityPayload]`
* **Behavior**: creates removal validity data and prompts user in validation popup; upon confirmation broadcasts.
* **Success data**: `{ result, validityData }`
* **Errors**: `removeXmIdentityError`, `removeXmIdentityCancelled`, `TIMEOUT`

Example:

```ts
const payload = { /* XMCoreTargetIdentityPayload */ };
const res = await provider.request({ method: 'removeXmIdentity', params: [payload] });
```

#### getWeb2Identities

* **Params**: none
* **Success data**: identities list from SDK
* **Errors**: `getWeb2IdentitiesError`

Example:

```ts
const res = await provider.request({ method: 'getWeb2Identities' });
```

#### getWeb2IdentityProofPayload

* **Params**: none
* **Success data**: proof payload to be used for Web2 identity linking
* **Errors**: `getWeb2IdentityProofPayloadError` (also returned if user not logged in)

Example:

```ts
const res = await provider.request({ method: 'getWeb2IdentityProofPayload' });
```

#### addTwitterIdentity

* **Params**: `[payload: TwitterProof]`
* **Behavior**: validates and prompts user in validation popup; upon confirmation broadcasts.
* **Success data**: `{ result, validityData }`
* **Errors**: `addTwitterIdentityError`, `addTwitterIdentityCancelled`, `TIMEOUT`

Example:

```ts
const proof = /* TwitterProof from your backend/SDK */
const res = await provider.request({ method: 'addTwitterIdentity', params: [proof] });
```

#### removeWeb2Identity

* **Params**: `[ { context: string, username: string } ]`
* **Behavior**: constructs validity data and prompts user in validation popup; upon confirmation broadcasts.
* **Success data**: `{ result, validityData }`
* **Errors**: `removeWeb2IdentityError`, `removeWeb2IdentityCancelled`, `TIMEOUT`

Example:

```ts
const res = await provider.request({
  method: 'removeWeb2Identity',
  params: [{ context: 'twitter', username: 'handle' }],
});
```
