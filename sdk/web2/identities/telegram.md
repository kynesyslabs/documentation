---
icon: telegram
---

# Telegram

## Telegram Identity Integration (GitBook Page)

You can associate your Telegram account with your DEMOS address by following these steps. This page provides two integration styles:

1. High-level (SDK + helper service approach)
2. Low-level (explicit challenge + bot attestation flow)

The Telegram flow differs from GitHub / Twitter because it involves an authorized Telegram Bot that produces an unsigned on‑chain identity transaction after verifying both the user’s Telegram login payload and a signed wallet challenge.

***

### Telegram Bot Overview

Flow: Telegram Login Widget → dApp → Bot verification endpoint (no deep links or chat commands).

The Telegram bot (or a verification microservice) acts as an attestation authority. It must:

1. Accept a POST containing the Telegram Login Widget auth payload (`telegramUser`) and the `signedChallenge` produced by the user wallet.
2. Verify the Telegram auth payload hash (HMAC) server-side.
3. Verify the user wallet signature embedded in `signedChallenge` (delegated to node during `/api/tg-verify`).
4. Sign an attestation with the bot's Ed25519 key and call the node `/api/tg-verify` endpoint.
5. Return the resulting unsigned identity transaction to the dApp.

Only the widget-based REST flow is covered here.

#### Minimal Bot Environment Variables

| Variable              | Purpose                                 | Example                  |
| --------------------- | --------------------------------------- | ------------------------ |
| `BOT_TOKEN`           | Telegram Bot API token                  | `123456:ABCDEF...`       |
| `GENESIS_PRIVATE_KEY` | Bot Ed25519 private key (hex, 64 bytes) | `0x...`                  |
| `GENESIS_PUBLIC_KEY`  | Bot public key whitelisted in genesis   | `0x...`                  |
| `NODE_URL`            | Demos node base URL                     | `http://127.0.0.1:53550` |
| `WEBHOOK_DOMAIN`      | Public domain (no protocol)             | `abcd.ngrok-free.app`    |
| `WEBHOOK_PATH`        | Webhook path                            | `/telegram-webhook`      |
| `PORT`                | Bot server port                         | `8787`                   |

#### Attestation Signing Logic (Core `attest` Function)

The bot builds an ordered payload then signs it with its private key. Ordering matters to ensure deterministic signature.

```ts
async function attest(telegramId: string, username: string, signedChallenge: string) {
  const payload = { telegram_id: telegramId, username, signed_challenge: signedChallenge, timestamp: Math.floor(Date.now()/1000) }
  // Lexicographic ordering of keys for consistent signing
  const ordered = Object.keys(payload).sort().reduce((a,k)=> (a[k] = (payload as any)[k], a), {} as any)
  const msg = JSON.stringify(ordered)
  const sig = nacl.sign.detached(Buffer.from(msg,'utf8'), Buffer.from(GENESIS_PRIVATE_KEY,'hex'))
  const bot_signature = Buffer.from(sig).toString('hex')
  const body = { ...payload, bot_address: GENESIS_PUBLIC_KEY, bot_signature }
  const r = await fetch(`${NODE_URL}/api/tg-verify`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) })
  const text = await r.text()
  if(!r.ok) throw new Error('node '+r.status+' '+text)
  const j = text ? JSON.parse(text) : {}
  if(!j.success) throw new Error(j.error || 'verify_failed')
  return j // { success:true, unsignedTransaction: {...} }
}
```

Security guarantees enforced by node:

* Bot key (public) must match a whitelisted genesis entry.
* Challenge hash embedded in unsigned transaction prevents reuse.
* User signature inside `signed_challenge` ties Telegram identity to wallet.

#### Telegram Auth Payload HMAC Verification (Server-Side)

Telegram instructs verifying the Login Widget payload like this:

```ts
import crypto from 'node:crypto'

function verifyTelegramAuth(auth: Record<string, any>, botToken: string) {
  const { hash, ...rest } = auth
  // 1. Sort keys alphabetically
  const dataCheckArr = Object.keys(rest)
    .sort()
    .map(k => `${k}=${rest[k]}`)
  const dataCheckString = dataCheckArr.join('\n')
  // 2. Secret key = SHA256(botToken)
  const secretKey = crypto.createHash('sha256').update(botToken).digest()
  // 3. Compute HMAC-SHA256 of dataCheckString with secretKey
  const hmac = crypto
    .createHmac('sha256', secretKey)
    .update(dataCheckString)
    .digest('hex')
  return hmac === hash
}
```

If this returns false, reject the request and DO NOT proceed to attestation.

#### Verification REST Endpoint (Unified) Example

```ts
import express from 'express'
import nacl from 'tweetnacl'
import crypto from 'node:crypto'

const app = express(); app.use(express.json())
const BOT_TOKEN = process.env.BOT_TOKEN!
const GENESIS_PRIVATE_KEY = process.env.GENESIS_PRIVATE_KEY!.replace(/^0x/,'')
const GENESIS_PUBLIC_KEY = process.env.GENESIS_PUBLIC_KEY!
const NODE_URL = process.env.NODE_URL || 'http://127.0.0.1:53550'

function verifyTelegramAuth(auth: any) {
  const { hash, ...rest } = auth
  const dataCheckString = Object.keys(rest).sort().map(k => `${k}=${rest[k]}`).join('\n')
  const secretKey = crypto.createHash('sha256').update(BOT_TOKEN).digest()
  const hmac = crypto.createHmac('sha256', secretKey).update(dataCheckString).digest('hex')
  return hmac === hash
}

async function callVerify(telegramUser: any, signedChallenge: string) {
  const payload = { telegram_id: telegramUser.id, username: telegramUser.username || '', signed_challenge: signedChallenge, timestamp: Math.floor(Date.now()/1000) }
  const ordered = Object.keys(payload).sort().reduce((a,k)=> (a[k]=(payload as any)[k], a), {} as any)
  const msg = JSON.stringify(ordered)
  const sig = nacl.sign.detached(Buffer.from(msg,'utf8'), Buffer.from(GENESIS_PRIVATE_KEY,'hex'))
  const bot_signature = Buffer.from(sig).toString('hex')
  const body = { ...payload, bot_address: GENESIS_PUBLIC_KEY, bot_signature }
  const r = await fetch(`${NODE_URL}/api/tg-verify`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) })
  const text = await r.text(); if(!r.ok) throw new Error(text || r.status.toString())
  const j = text ? JSON.parse(text) : {}
  if(!j.success) throw new Error(j.error || 'verify_failed')
  return j
}

app.post('/webhook/verification', async (req,res) => {
  try {
    const { telegramUser, signedChallenge } = req.body || {}
    if(!telegramUser || !signedChallenge) return res.status(400).json({ success:false, error:'Missing telegramUser or signedChallenge' })
    if(!verifyTelegramAuth(telegramUser)) return res.status(401).json({ success:false, error:'Invalid telegram auth hash' })
    const result = await callVerify(telegramUser, signedChallenge)
    res.json({ success:true, unsignedTransaction: result.unsignedTransaction })
  } catch(e:any){
    res.status(500).json({ success:false, error: e.message })
  }
})

app.listen(8787, () => console.log('Verification service listening on :8787'))
```

This single endpoint now handles HMAC validation, attestation signing, and forwarding to the node.

#### Optional Proxy / Forwarder Pattern (Server Relay)

If you keep the verification service private, expose a thin relay through your main backend (adapted from `examples/BotWebhookForwarder.ts`):

```ts
app.post('/api/telegram/verify', async (req, res) => {
  const { telegramAuth, signedChallenge } = req.body
  if(!telegramAuth || !signedChallenge) return res.status(400).json({ error:'Missing telegramAuth or signedChallenge' })
  const resp = await fetch(`${BOT_INTERNAL_URL}/webhook/verification`, {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ telegramUser: telegramAuth, signedChallenge, timestamp: Math.floor(Date.now()/1000), source:'dapp-server' })
  })
  const data = await resp.json()
  if(!resp.ok) return res.status(resp.status).json({ error: data.error || 'Bot verification failed' })
  res.json(data)
})
```

Benefits:

* Hides internal verification service
* Central HMAC verification & logging
* Add auth / API keys / rate limiting easily

***

### 1. Connect your wallet

Use the DEMOS SDK (web) and obtain (or generate) a wallet/key pair. In production you’d use an existing wallet provider; below we show a mnemonic example only for demonstration.

```ts
import { Demos } from "@kynesyslabs/demosdk/websdk";

// the DEMOS rpc (HTTP endpoint of a node)
const rpc = "https://demosnode.discus.sh";

const demos = new Demos();
await demos.connect(rpc);
await demos.connectWallet(mnemonic); // Replace with secure wallet handling

console.log("Address:", demos.wallet.address);
```

***

### 2. Obtain a one‑time challenge

Request a challenge from the node. This binds a timestamp + nonce to your wallet address and prevents replay attacks.

```ts
async function getChallenge(nodeUrl: string, address: string) {
  const r = await fetch(`${nodeUrl}/api/tg-challenge`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ demos_address: address })
  });
  if(!r.ok) throw new Error('Challenge HTTP ' + r.status);
  const j = await r.json();
  return j.challenge; // Format: DEMOS_TG_BIND_<address>_<timestamp>_<nonce>
}

const challenge = await getChallenge(rpc, demos.wallet.address);
console.log('Challenge:', challenge);
```

***

### 3. Sign the challenge (prove wallet ownership)

```ts
const signature = await demos.wallet.signMessage(challenge);
const signedChallenge = `${challenge}:${signature}`;
console.log('Signed challenge:', signedChallenge.slice(0, 96) + '…');
```

Never reuse a challenge. If the user abandons the flow, discard it and request a new one later.

***

### 4. Authenticate the user with the Telegram Login Widget

Embed the official widget (or open a window) to obtain the user’s Telegram auth payload.

```html
<script async src="https://telegram.org/js/telegram-widget.js?22"
        data-telegram-login="YOUR_BOT_USERNAME"
        data-size="large"
        data-onauth="onTelegramAuth(user)"
        data-request-access="write"></script>
<script>
  function onTelegramAuth(user){
    // Forward 'user' (Telegram auth payload) to your application logic
    window.dispatchEvent(new CustomEvent('telegram-auth', { detail: user }))
  }
</script>
```

In your app (React example):

```ts
useEffect(() => {
  const handler = (e: any) => handleTelegramAuth(e.detail);
  window.addEventListener('telegram-auth', handler);
  return () => window.removeEventListener('telegram-auth', handler);
}, []);
```

Security: The widget payload contains a `hash` you should verify server‑side (HMAC with your bot token) if you do not fully trust the client.&#x20;

### 5. Check telegram channel membership

Ensure the user is a member of a specific Telegram channel to proceed with the identity attestation.

```ts
export async function checkMembership(
  botWebhook: string,
  telegramUser: TelegramUserAuth,
): Promise<boolean> {
  const r = await fetch(
    `${botWebhook.replace(/\/$/, "")}/webhook/check-membership`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "User-Agent": "YourAppNameAndVersion/1.0",
      },
      body: JSON.stringify({
        telegramUser: telegramUser,
        timestamp: Date.now(),
        source: "your-app-name",
      }),
    },
  );
  if (!r.ok) throw new Error(`Challenge HTTP ${r.status}`);
  const j = await r.json();
  if (j.error) throw new Error(j.error);
  return j.isMember;
}

const isMember = await checkMembership(botUrl, telegramUser);
if (!isMember) throw new Error('User is not a channel member');
```

This function checks if the user is a member of the specified channel using Telegram's `getChatMember` API method. If the user is not a member, an error is thrown, preventing further steps in the attestation process.

***

### 6. Send an identity attestation request to your Telegram Bot

Your bot exposes an internal HTTPS endpoint (e.g. `/webhook/verification`). Send it:

```ts
async function submitAttestationRequest(botUrl: string, telegramUser: any, signedChallenge: string) {
  const r = await fetch(`${botUrl}/webhook/verification`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ telegramUser, signedChallenge, timestamp: Math.floor(Date.now()/1000) })
  });
  if(!r.ok) throw new Error('Bot HTTP ' + r.status);
  const j = await r.json();
  if(!j.success) throw new Error(j.error || 'Bot attestation failed');
  return j.unsignedTransaction; // Opaque unsigned identity tx
}

const unsignedTx = await submitAttestationRequest(botUrl, telegramUserPayload, signedChallenge);
console.log('Unsigned identity tx:', unsignedTx);
```

Bot responsibilities:

1. Verify Telegram auth payload (hash + expiry)
2. Validate wallet signature over challenge
3. Ensure challenge not reused
4. Call node `/api/tg-verify` to obtain unsigned identity transaction
5. Return unsigned transaction to dApp

***

### 7. Sign & broadcast the identity transaction

```ts
// Sign with wallet, confirm with node, then broadcast
const signedTx = await demos.wallet.signTransaction(unsignedTx);
const validity = await demos.confirm(signedTx);
const broadcastRes = await demos.broadcast(validity);
console.log('Broadcast result:', broadcastRes);

const txHash = broadcastRes.hash || broadcastRes.tx_hash;
console.log('Telegram identity linked. Tx hash:', txHash);
```

Successful broadcast response (example):

```json
{
  "result": 200,
  "response": { "message": "Verified telegram proof. Transaction applied." },
  "require_reply": false,
  "extra": { "confirmationBlock": 42 }
}
```

***

### 8. Getting linked web2 (Telegram) accounts

After the confirmation block has been forged you can query all linked web2 identities (includes `telegram` array if present):

```ts
import { Identities } from "@kynesyslabs/demosdk/abstraction";

const identities = new Identities();
const web2Ids = await identities.getWeb2Identities();
console.log(web2Ids);
```

Example response snippet:

```json
{
  "result": 200,
  "response": {
    "telegram": [
      {
        "username": "example_user",
        "telegramId": 123456789,
        "proofHash": "ab3f...c901",
        "challengeHash": "7ff2...19d0"
      }
    ]
  },
  "require_reply": false,
  "extra": null
}
```

***

### 9. Removing linked Telegram identity

Create a removal transaction using the web2 abstraction (context = `telegram`):

```ts
const payload = {
  context: 'telegram',
  username: 'example_user' // Or other unique handle stored during linking
};

const validityData = await identities.removeWeb2Identity(demos, payload);
if (validityData.result === 200) {
  const res = await demos.broadcast(validityData);
  console.log(res);
}
```

Successful removal response:

```json
{
  "result": 200,
  "response": { "message": "Identity removed. Transaction applied." },
  "require_reply": false,
  "extra": { "confirmationBlock": 57 }
}
```

***

### End-to-End (Headless Helper)

If you prefer a single orchestrator call, adapt the following (mirrors `examples/flowFunctions.ts`):

```ts
import { runTelegramIdentityFlow } from './examples/flowFunctions';

const result = await runTelegramIdentityFlow({
  nodeUrl: rpc,
  botUrl,
  wallet: demos.wallet,
  demos,
  telegramUser: telegramUserPayload,
  onStage: (s, d) => console.log('[stage]', s, d)
});
console.log('Flow complete:', result.hash);
```

Stages emitted:

* `challenge:request` → `challenge:received` → `challenge:signed` → `tx:unsigned` → `tx:broadcasted`

***

### Architecture Summary

| Step              | Actor         | Purpose                  | Security Aspect                 |
| ----------------- | ------------- | ------------------------ | ------------------------------- |
| getChallenge      | Node          | One-time challenge       | Timestamp + nonce (anti replay) |
| signChallenge     | Wallet        | Prove address ownership  | Ed25519 signature               |
| Telegram auth     | User + Widget | Prove Telegram control   | HMAC hash w/ bot token          |
| Attestation (bot) | Bot           | Build unsigned tx        | Bot key authorized in genesis   |
| Sign & broadcast  | Wallet + Node | Record identity on-chain | Node validates all proofs       |

#### Verification Service Endpoint Summary

| Endpoint                            | Purpose                                                     |
| ----------------------------------- | ----------------------------------------------------------- |
| `POST /webhook/verification`        | Accept Telegram auth + signed challenge, return unsigned tx |
| `POST /api/telegram/verify` (proxy) | Public backend relay to internal verification service       |
| `GET /health` (optional)            | Liveness / monitoring                                       |

***

### Environment Variables (Frontend Example)

| Variable                       | Description                    | Example                        |
| ------------------------------ | ------------------------------ | ------------------------------ |
| `VITE_DEMOS_NODE_URL`          | Demos node base URL            | `https://demosnode.discus.sh`  |
| `VITE_TELEGRAM_BOT_SERVER_URL` | Your bot verification endpoint | `https://your-bot.example.com` |
| `VITE_TELEGRAM_BOT_USERNAME`   | Bot username (for widget)      | `demos_prod_bot`               |
| `VITE_FRONTEND_URL`            | Public origin hosting widget   | `https://app.example.com`      |
| `VITE_BOT_URL`                 | (Optional) Bot deep link       | `https://t.me/demos_prod_bot`  |

Widget & webhook endpoints must be HTTPS and publicly reachable. Register your domain with BotFather (`/setdomain`) and set a webhook via the Bot API if you process updates server-side.

***

### Common Errors & Remedies

| Error Pattern            | Likely Cause                             | Suggested Handling                                    |
| ------------------------ | ---------------------------------------- | ----------------------------------------------------- |
| `Challenge HTTP 4xx/5xx` | Node unreachable or malformed address    | Retry / show maintenance message                      |
| `Bot HTTP 5xx`           | Bot offline / network issue              | Exponential backoff retry                             |
| `Bot attestation failed` | Invalid Telegram auth or stale challenge | Force new Telegram login + new challenge              |
| `BroadcastFailure`       | Network congestion                       | Retry with fresh nonce (re-fetch challenge if needed) |
| User cancels sign        | Wallet rejection                         | Offer retry; do not reuse challenge                   |

***

### Security Notes

* Never trust the Telegram auth payload hash solely on the client; verify server-side where possible.
* Expire unused challenges (e.g. 5–10 minutes) and reject reuse server-side.
* Rate limit challenge requests per address/IP.
* Log stage transitions with a correlation ID (address or session) for auditing.

***

### Minimal UI Flow (Conceptual)

1. User clicks “Link Telegram” → fetch + sign challenge
2. Telegram widget opens → returns auth payload
3. Send (telegramUser + signedChallenge) to bot → receive unsignedTx
4. Prompt user to sign identity transaction → broadcast
5. Show confirmation (tx hash + linked username)

***

### Complete Flow Diagram

```
Wallet (User)      dApp Frontend          Telegram Bot            Demos Node
     |                   |                      |                      |
     |  connectWallet    |                      |                      |
     |------------------>|                      |                      |
     |                   | POST /api/tg-challenge                      |
     |                   |---------------------->|                      |
     |                   |<----- challenge ------|                      |
 sign challenge          |                      |                      |
     |                   |                      |                      |
     |  Telegram Widget auth (user)             |                      |
     |------------------>(payload)              |                      |
     |                   | POST /webhook/verification (user,payload,signedChallenge)
     |                   |------------------------------------------->|
     |                   |                      |  /api/tg-verify     |
     |                   |                      |-------------------->|
     |                   |                      |<-- unsigned tx -----|
     |                   |<-- unsigned tx ------|                      |
     |  signTransaction  |                      |                      |
     |------------------>| demos.confirm + broadcast ----------------->|
     |                   |                      |<-- success/receipt --|
     |<-- tx hash -------|                      |                      |
```

***

### Cleanup / Removal

To unlink, use `removeWeb2Identity` with `context: 'telegram'` (see removal step). The chain state will reflect the removal in a new block.

***

### Next Steps

* Integrate server-side Telegram HMAC validation
* Replace mnemonic demo wallet with production wallet provider
* Add UI states for: waiting bot, signing, broadcast pending, final confirmation
* Implement telemetry on each stage for monitoring

***

This completes the Telegram identity linking guide.
