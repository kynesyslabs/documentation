---
icon: github
---

# GitHub

You can associate your GitHub account with your DEMOS address by following these steps:

### 1. Connect your wallet

```typescript
import { Demos } from "@kynesyslabs/demosdk";
import { Identities } from "@kynesyslabs/demosdk/abstraction";

// the DEMOS rpc
const rpc = "https://demosnode.discus.sh"

const demos = new Demos();
await demos.connect(rpc);
await demos.connectWallet(mnemonic);
```

### 2. Generate the proof payload

To link your GitHub account to your DEMOS address, you need to create a public gist containing a proof on your GitHub. The proof is a string that contains a message, a signature and your public key.

You can generate a proof as shown below:

```typescript
const identities = new Identities();

const proofPayload = await identities.createWeb2ProofPayload(demos)
console.log("Upload on GitHub gist: ", proofPayload)
```

The proof looks like this:

```
demos:dw2p:ed25519:e9dd684a031e142ce312b695275b226ab8824f2fd3674db52f28be6c3e9fe027f88a8a/...
```

Open your GitHub and create a new public gist containing only the proof in the first file.

### 3. Send an identity request

After creating the gist, copy the gist url and use it to create an identity transaction as shown below:

```typescript
const proof = "https://gist.github.com/cwilvx/abf8db960c16dfc7f6dc1da840852f79"

const validityData = await identities.addGithubIdentity(demos, proof)
console.log("validity data: ", validityData)

if (validityData.result == 200){
    const res = await demos.broadcast(validityData)
    console.log(res)
}
```

The following proof url formats are also supported:

1. Raw gist url: [https://gist.githubusercontent.com/cwilvx/abf8db960c16dfc7f6dc1da840852f79/raw/224478424c5e6e51f5eb60cb6aeea278d3418742/gistfile1.txt](https://gist.githubusercontent.com/cwilvx/abf8db960c16dfc7f6dc1da840852f79/raw/224478424c5e6e51f5eb60cb6aeea278d3418742/gistfile1.txt)
2. Raw proof file in a GitHub repo url: [https://raw.githubusercontent.com/cwilvx/vonage-draft-images/refs/heads/master/proof.txt](https://raw.githubusercontent.com/cwilvx/vonage-draft-images/refs/heads/master/proof.txt)

A successful transaction response should look like this:

```json
{
  "result": 200,
  "response": {
    "message": "Verified github proof. Transaction applied."
  },
  "require_reply": false,
  "extra": {
    "confirmationBlock": 38
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
    "github": [
      {
        "proof": "https://gist.github.com/cwilvx/abf8db960c16dfc7f6dc1da840852f79",
        "username": "cwilvx",
        "proofHash": "c9bcf4dcb2bdb490...1060ab12b16a7385351"
      }
    ]
  },
  "require_reply": false,
  "extra": null
}
```

### 5. Removing linked GitHub identity

You can create a transaction to remove your linked GitHub account as shown:

```typescript
const payload = {
    context: "github",
    username: "cwilvx"
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
    "confirmationBlock": 47
  }
}
```

