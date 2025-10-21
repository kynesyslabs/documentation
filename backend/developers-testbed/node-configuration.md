# Node Configuration

#### Environment

Demos nodes use a `.env` file and a few additional configuration files to provide a customizable and replicable setup.\
For convenience, a precompiled `.env` file is already included.

In most cases, you won't need to edit it — just double-check that the listed ports are free on your system.\
Besides the ones listed, Demos nodes also launch a Postgres Docker container that listens by default on port **5332** (you'll see how to change this in the next chapter).

> **Note**: You don't need to configure the Twitter and GitHub sections of the `.env` yet, even if they are present depending on the branch.

***

#### Keys

To generate your initial keypair, simply run:

`./run`

The node will crash due to a missing peerlist (expected at this stage), but it will create a file named like `publickey_1234567890` inside your `node` directory.\
Inside that file, you'll find your **public key**.

***

#### Peerlist

Demos nodes use a `demos_peerlist.json` file to define peers.\
First, create it by copying the example file:

`cp demos_peerlist.example.json demos_peerlist.json`

Then open it with your favorite text editor.

* **Solo mode (local testing)**:\
  Replace the `identity` key with your generated public key.
*   **Connecting to other nodes**:\
    Add lines in the following format:

    `"1234567890...": "http://url:port"`

Replace `1234567890...` with the actual public key of the peer and `http://url:port` with its URL.
