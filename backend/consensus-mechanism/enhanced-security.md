# Enhanced Security

#### Byzantine Fault Tolerance (BFT)

* **Why:** Traditional consensus mechanisms can be vulnerable to attacks from malicious nodes.
  * **Example:** PoW blockchains like Bitcoin are susceptible to 51% attacks where a majority of mining power could manipulate the blockchain. BFT ensures that even if some nodes act maliciously, the system can continue operating correctly by mathematically verifying node integrity through pseudorandom seeds.

#### Forced Exclusion of Malicious Nodes

* **Why:** Continuous evaluation of nodes based on pseudorandom seed verification actively mitigates potential threats.
  * **Example:** In a cryptocurrency network where double-spending attacks are common, PoR-BFT’s dynamic shard composition helps in removing compromised nodes by continuously evaluating the blockchain status mathematically through pseudorandom seeds.
