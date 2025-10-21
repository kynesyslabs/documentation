# Message Types

The Instant Messaging Protocol supports various message types:

* "register": Register a new peer with the server
* "discover": Request a list of all connected peers
* "message": Encrypted peer-to-peer messages
* "peer\_disconnected": Notification when a peer disconnects
* "request\_public\_key": Request a peer's public key
* "public\_key\_response": Response containing a peer's public key
* "server\_question": Question from the server to a peer
* "peer\_response": Response from a peer to a server question
* "debug\_question": Debug message to trigger a server question
* "error": Error notification with details

\
