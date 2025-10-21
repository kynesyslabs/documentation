---
icon: usb-drive
---

# FIDO2 Passkeys

The Demos SDK offers secure methods to generate or recover private keys using a FIDO2 hardware key, which are then usable across the entire Demos network, encompassing various contexts like different blockchains and traditional web2 environments.\
\
In this chapter, we'll delve into the specifics of how this mechanism operates and strategies to utilize it effectively for optimal security.

### The \`hmywallet\` module and it's wrapper

The Demos SDK features a Python module called `hmywallet`, a customized version of [https://github.com/tcsenpai/hmywallet](https://github.com/tcsenpai/hmywallet) designed specifically for integration with the Demos SDK.

The code resides in `sdks/src/wallet/passkeys/hmywallet`, and the module for integrating it into the SDK can be found in `sdks/src/wallet/passkeys/passkeys.ts`.

### Usage and typical use cases

You can test the functionality of the wrapper by executing:

```bash
tsx src/wallet/passkeys/passkeys.ts
```

From the `sdks` repository root.\
\
The test part of the module "just" creates the credentials and print out the private key generated.\
However, the intended usage is:

```typescript
import wallet from "@kynesyslabs/demosdk"

[...]

const privateKey = await wallet.generatePasskey()
```

This method returns a hexadecimal string containing the private key linked to the credentials derived from your FIDO2 device's `hmac_secret`.

You can now use this private key in any way Demos allows it to be used. For example, you could load your Demos credentials directly using this private key.
