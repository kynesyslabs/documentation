---
icon: question
---

# FAQ

This page addresses most of the commonly asked questions about the current status of the Demos Network.

***

### What Can you Do

#### How is Demos being rolled out?

Demos is being rolled out in 4 phases with a number of releases per phase.  You will find the most recent release note in the release note section.  For an outline of the 4 phases please review our [Road to the Omniweb](https://mirror.xyz/0x6C1c06BCBb5BB1Ebd3790c11069Dbd5712314512/xA4F_WBy17mjX0PEMh1y4vf1tz8xdTlvNU4j_ZqgEiE) article

#### How do I check the network status?

You can check the network status by heading to the [status page](https://status.demos.sh/).  You can view block and transaction data on our [explorer](https://explorer.demos.sh).

#### How can I create a Demos wallet?

TBD

#### How do I download the SDK?

To download the SDK, you can use either `yarn`or `npm`. Please note that `bun`is supported too but is still experimental.&#x20;

With yarn:

`yarn add @kynesyslabs/demosdk`

With npm:

`npm i @kynesyslabs/demosdk`

#### How do I download the node software?

In this release, the node software is not yet publicly available. This is by design, as we are carefully assessing the network capabilities, adding more nodes in a controlled environment.

#### How can I become a validator?

Once the node software is released, you can become a validator by simply following the instructions. Staking will be required in a later phase, initially no staking is required to enable faster onboarding and testing.

#### What are the requirements for running a Demos node?

To run a Demos node the minimum requirements are:

* 8GB RAM
* 100mbps Download/Upload network bandwidth (dedicated)
* 200gb SSD space
* 4 cores (physical cores)
* root access

The suggested requirements are the same, with 200mbps Download/Upload bandwidth.

#### How can I make a transaction?

You can refer to the [Broken link](broken-reference "mention") section on how to build transactions. At this stage you cannot forward transactions to public nodes, you are able to use the SDK locally and use the very same code once public RPCs are available.

#### Is there a Faucet? How can I get DEM tokens?

You can request Demos tokens at the [Demos Faucet](https://faucet.demos.sh/).

### What you Cannot Do (yet)

* XM and Web2 transactions are brittle as they are being constantly upgraded and improved
* The node software is not yet public, thus new validators and node maintainers aren't allowed yet (this to carefully test and ensure the network is ready for a bigger number of nodes)
