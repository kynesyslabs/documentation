# Crosschain SWAP

## How to SWAP from one chain to another chain

### 1. Connect to the network

```ts
import { Demos } from "@kynesyslabs/demosdk/websdk"
import RubicService from "@/features/bridges/rubic"
import { WrappedCrossChainTrade } from "rubic-sdk"
import { BridgeTradePayload, SupportedChains } from "@kynesyslabs/demosdk/types"

// Connect to the network
const rpc = "https://demosnode.discus.sh";
const demos = new Demos();
await demos.connect(rpc);
await demos.connectWallet(mnemonic);
```

### 2. Creating the RubicService instance

After connecting the wallet you need to create a Rubic Service instance

```ts
const address = await demos.getEd25519Address()
const rubicService = new RubicService(address, SupportedChains.POLYGON);
```

As you can see here used `SupportedChains.POLYGON`.\
Need to use that chain from which you want to swap tokens.\
In this case used Polygon, because we wanted to swap from the Polygon chain to Ethereum.

Here are the supported chains.

```ts
export const SupportedChains = {
    ETH: "ETH",
    POLYGON: "POLYGON",
    BSC: "BSC",
    AVALANCHE: "AVALANCHE",
    OPTIMISM: "OPTIMISM",
    ARBITRUM: "ARBITRUM",
    LINEA: "LINEA",
    BASE: "BASE",
    SOLANA: "SOLANA",
}
```

### 3. Creating the payload to get trade data

Provided payload for swapping 10 USDT from the Polygon chain to the Ethereum chain

```ts
const payload: BridgeTradePayload = {
                fromToken: "USDT",
                toToken: "USDT",
                amount: 10,
                fromChainId: 137,
                toChainId: 1,
            }
```

### 4. Get trade data

After creating the payload, need to call the `getTrade` method

```ts
const trade = await rubicService.getTrade(payload);
```

### 5. Execute trade method

After successfully getting the trade data, we already can do a swap by calling the `executeTrade` method

```ts
const receipt = await rubicService.executeTrade(trade);
```

The result of the `executeTrade` method will be the receipt of that swap transaction

e.g.

```ts
"0x2342692074a7484f3ac9713d36cd23fdc1c51810d03639e5cf651bfefb62fdc3"
```

[PolygonScan](https://polygonscan.com/tx/0x2342692074a7484f3ac9713d36cd23fdc1c51810d03639e5cf651bfefb62fdc3)
