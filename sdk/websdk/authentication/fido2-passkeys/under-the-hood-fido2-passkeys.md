# Under the Hood: FIDO2 Passkeys

This chapter provides a detailed explanation of how `hmywallet`, along with its Demos wrapper, securely leverages a FIDO2 device to accurately derive valid private keys.

### The Python module: hmywallet

#### fido2

The `fido2` module allows `hmywallet` to interact with your FIDO2 device.

#### Main module

The script initiates by creating a client through the detection of the FIDO2 device. Afterward, the `cred_manager` submodule verifies the presence of `data/credential.pkl` and generates it if it is not found.

Creating the credential file requires interacting with the FIDO2 device to generate an appropriate `hmac_secret` based on predefined user and rp fields, along with a random 16-byte challenge. Additionally, this process encrypts the credential file using a password that the user must enter each time to unlock the wallet.

Storing the file along with the password ensures that the key remains deterministic, consistently generating the same key given the correct credentials. Note that entering an incorrect password will not raise any errors but will yield a completely different private key.

Finally, the credentials are retrieved using the password hash as a salt. This results in a secret that, once hashed, represents the private key of the user.

### The Typescript Wrapper: passkeys.ts

This file is a very simple wrapper that manages safe execution and output retrieval from the `hmywallet` module.

The wrapper exports a `PasskeyGenerator` class that contains a `.generate()` method. This async method calls the `generate.sh` script inside the hmywallet folder, which automatically manages the module dependencies and kickstart the process above.

By reading the output of `hmywallet` module, the `.generate()` method returns the above mentioned private key.
