# Running the node

If you made it this far, you're just one step away from running your very own Demos node!

***

#### Running a Node (Normal Mode)

To start a Demos node, simply run:

`./run`

This will also spin up a Postgres container alongside the node.\
If you stop the node (e.g., with `CTRL+C` or due to a crash), the Postgres container will shut down too.\
Restarting the node with `./run` will reuse the existing database and continue from where it left off.

***

#### Cleaning Up at Start

To force a full reset of the database, use:

`./run -c true`

This will wipe the Postgres container and restart the database from scratch.

> **Note**: This resets the entire blockchain.
>
> * If you're connected to other peers, your node will resync from them.
> * If you're running solo, the blockchain will restart from the genesis block.

### Other options for the run file

| Flag | Argument           | Description                                                     |
| ---- | ------------------ | --------------------------------------------------------------- |
| `-p` | `<port>`           | Set the RPC port (default: `53550`).                            |
| `-d` | `<pg_port>`        | Set the Postgres port (default: `5332`).                        |
| `-c` | `true/false`       | Clean the Postgres database before starting (default: `false`). |
| `-i` | `<identity_file>`  | Set the identity file to use.                                   |
| `-l` | `<peer_list_file>` | Set the peer list file (default: `demos_peerlist.json`).        |
| `-n` | (no argument)      | Skip `git pull` (disable auto-update).                          |
| `-u` | `<exposed_url>`    | Set the URL to expose externally.                               |
| `-r` | `bun/node`         | Force runtime selection (`bun` is required).                    |
