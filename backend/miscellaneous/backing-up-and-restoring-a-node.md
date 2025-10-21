# Backing up and restoring a node

The backup and restore feature can be used to reset the network (remove all blocks & transactions by deleting the database) without deleting GCR accounts.&#x20;

You can do this by executing the `run` script and setting the `-b` flag to `true` :

```sh
./run -b true #other flags here
```

### How it works'

Accounts are dumped into a JSON file in the `output` directory at the node source root by running the dump script and then restarting the node as usual (but with the `-c true` flag). The node scans the output directory and if a dump file is found, it is parsed and converted into the genesis format. All the accounts in the genesis are created when the genesis block is forged.\


{% hint style="info" %}
To add a node to a restored network, please see: [joining-the-testnet-using-a-custom-genesis.md](joining-the-testnet-using-a-custom-genesis.md "mention")
{% endhint %}

