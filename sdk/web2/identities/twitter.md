---
icon: twitter
---

# Twitter

You can associate your Twitter account with your DEMOS address by following these steps:

### 1. Connect your wallet

```typescript
import { Demos } from "@kynesyslabs/demosdk/websdk"
import { Identities } from "@kynesyslabs/demosdk/abstraction";

// the DEMOS rpc
const rpc = "https://demosnode.discus.sh"

const demos = new Demos();
await demos.connect(rpc);
await demos.connectWallet(mnemonic);
```

### 2. Generate the Proof Payload

To link your Twitter account to your DEMOS address, you need to create a public tweet containing a proof on your twitter account. The proof is a string that contains a message, a signature and your public key.

You can generate a proof as shown below:

```typescript
const identities = new Identities();

const proofPayload = await identities.createWeb2ProofPayload(demos)
console.log("Tweet this:", proofPayload)
```

The proof looks like this:

```
demos:dw2p:ed25519:e9dd684a031e142ce312b695275b226ab8824f2fd3674db52f28be6c3e9fe027f88a8a9509563....
```

Open Twitter and create a public tweet containing only the proof string.

### 3. Send an Identity request

After tweeting the proof, copy the tweet url and use it to create an identity transaction as shown below:

```typescript
const proof = "https://x.com/cwilvxi/status/1905612827840196726"

const validityData = await identities.addTwitterIdentity(demos, proof)
console.log("validity data: ", validityData)

if (validityData.result == 200){
    const res = await demos.broadcast(validityData)
    console.log(res)
}
```

A successful transaction response should look like this:

```json
{
  "result": 200,
  "response": {
    "message": "Verified twitter proof. Transaction applied."
  },
  "require_reply": false,
  "extra": {
    "confirmationBlock": 9
  }
}
```

### 4. Getting linked web2 accounts

After the confirmation block has been forged, you can retrieve all your linked accounts as shown:

```typescript
const web2Ids = await identities.getWeb2Identities()
```

The response should look like this:

```json
{
  "result": 200,
  "response": {
    "twitter": [
      {
        "proof": "https://x.com/cwilvxi/status/1905612827840196726",
        "username": "cwilvxi",
        "proofHash": "d1ebcb162c3d5c7d...a6078a90ee56fb21652"
      }
    ]
  },
  "require_reply": false,
  "extra": null
}
```

### 5. Removing Twitter identity

You can create a transaction to remove your linked Twitter account as shown:

```typescript
const payload = {
    context: "twitter",
    username: "cwilvxi"
}

const validityData = await identities.removeWeb2Identity(demos, payload);

if (validityData.result == 200) {
    const res = await demos.broadcast(validityData);
    console.log(res);
}
```

A successful transaction response should look like this:

```json
{
  "result": 200,
  "response": {
    "message": "Identity removed. Transaction applied."
  },
  "require_reply": false,
  "extra": {
    "confirmationBlock": 25
  }
}
```

