# Joining the testnet using a custom genesis

To add a node to a restored network, you'll need to replace the default genesis file with the genesis file of a peer already in the network. You can get the genesis of a peer at `/genesis`. eg. [https://demosnode.discus.sh/genesis](https://demosnode.discus.sh/genesis).

At the root of the node source, you can run the following command to download and replace the `genesis.json` file:

```sh
curl -o data/genesis.json https://demosnode.discus.sh/genesis
```

Then update `demos_peerlist.json` to locate the remote peer:

```json
{
    "0xpubkey": "https://demosnode.discus.sh"
}
```

{% hint style="info" %}
You can get the remote peer's public key by going to `/info` .eg. [https://demosnode.discus.sh/info](https://demosnode.discus.sh/info).
{% endhint %}

Finally, run the node with the `-c true` flag to delete the database:

```sh
./run -c true #other flags here
```

Before the local node starts to sync blocks with the remote node, the genesis block hash will be checked against the remote node's hash. If the hashes don't match, consensus can never happen so the node will terminate.
