---
icon: messages
---

# Instant Messaging

This chapter will cover the basics of using E2E Post-Quantum messaging capabilities through the Demos SDK.

Demos nodes automatically launch a service called `signalingServer`, which spins up a server responsible for handling private, end-to-end, on-node messages. These messages are then attested on the Demos network.

Each node manages its own messaging service, avoiding network-wide congestion and confirmation delays, while still forwarding attestations of the encrypted communications to the blockchain.

In the next chapter, we will learn how to use the `MessagingPeer` class to implement this type of communication.
