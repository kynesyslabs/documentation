# EVM Contract Write Transactions

The `contract_write` operation enables interaction with smart contracts on EVM-compatible blockchains through the Demos Network. This functionality allows you to prepare, sign, and execute contract method calls with custom parameters and options.

### Workflow

```typescript
// 1. Get contract instance
const contract = await instance.getContractInstance(contractAddress, abi)

// 2. Write to contract (generates signed transaction)
const signedTx = await instance.writeToContract(contract, methodName, args, options)

// 3. Prepare XM script for Demos Network
const xmscript = prepareXMScript({
    chain: "eth",
    signedPayloads: [signedTx],
    subchain: "sepolia",
    type: "contract_write",
    is_evm: true,
})

// 4. Prepare and broadcast through Demos Network
const signedDemosTx = await prepareXMPayload(xmscript, demos)
const validityData = await demos.confirm(signedDemosTx)
const result = await demos.broadcast(validityData)
```

### API Reference

#### `writeToContract(contract, functionName, args, options?)`

Prepares and signs a smart contract transaction for execution.

**Parameters:**

* `contract`: Contract instance (obtained via `getContractInstance`)
* `functionName`: Name of the contract method to call
* `args`: Array of arguments for the method
* `options` (optional): Transaction options object

**Options Object:**

```typescript
{
    gasLimit?: number;  // Custom gas limit for the transaction
    value?: string;     // ETH value to send (in ETH units, for payable functions)
}
```

**Returns:** Promise\<string> - Signed transaction hex string

#### `prepareXMScript(params)`

Creates an XM script for contract write operations.

**Parameters:**

```typescript
{
    chain: string;           // Target blockchain (e.g., "eth")
    subchain: string;        // Network (e.g., "sepolia", "mainnet")
    signedPayloads: string[]; // Array of signed transactions
    type: "contract_write";   // Operation type
    is_evm: boolean;         // Whether target chain is EVM-compatible
}
```

### Examples

#### Basic ERC20 Token Transfer

```typescript
import { parseEther } from "ethers"
import { EVM } from "@kynesyslabs/demosdk/xm-websdk"
import { prepareXMScript, prepareXMPayload, Demos } from "@kynesyslabs/demosdk/websdk"

// Initialize EVM instance and Demos
const instance = new EVM(chainProviders.eth.sepolia)
const demos = new Demos()

// Connect wallet and Demos
await instance.connect()
await instance.connectWallet(evmPrivateKey)
await demos.connect(rpc)
await demos.connectWallet(mnemonic)

// ERC20 ABI for transfer function
const erc20ABI = [
    {
        constant: false,
        inputs: [
            { name: "dst", type: "address" },
            { name: "wad", type: "uint256" },
        ],
        name: "transfer",
        outputs: [{ name: "", type: "bool" }],
        payable: false,
        stateMutability: "nonpayable",
        type: "function",
    },
]

// Get contract instance
const tokenAddress = "0x1234567890123456789012345678901234567890"
const contract = await instance.getContractInstance(tokenAddress, JSON.stringify(erc20ABI))

// Prepare transfer
const recipient = "0xa2f64eec3E69C0B2E9978AB371A16eaA3a1Cf793"
const amount = parseEther("1.0")

// Sign transaction
const signedTx = await instance.writeToContract(contract, "transfer", [recipient, amount])

// Prepare XM script
const xmscript = prepareXMScript({
    chain: "eth",
    signedPayloads: [signedTx],
    subchain: "sepolia",
    type: "contract_write",
    is_evm: true,
})

// Execute through Demos Network
const signedDemosTx = await prepareXMPayload(xmscript, demos)
const validityData = await demos.confirm(signedDemosTx)
const result = await demos.broadcast(validityData)
```

#### Payable Contract with Custom Options

```typescript
// Payable contract ABI (e.g., deposit function)
const payableABI = [
    {
        constant: false,
        inputs: [],
        name: "deposit",
        outputs: [],
        payable: true,
        stateMutability: "payable",
        type: "function",
    },
]

const contractAddress = "0x1234567890123456789012345678901234567890"
const contract = await instance.getContractInstance(contractAddress, JSON.stringify(payableABI))

// Call payable function with ETH value and custom gas
const signedTx = await instance.writeToContract(
    contract,
    "deposit",
    [], // No arguments for this function
    {
        gasLimit: 100000, // Custom gas limit
        value: "1"        // Send 1 ETH with the transaction
    }
)

// Create XM script and execute
const xmscript = prepareXMScript({
    chain: "eth",
    signedPayloads: [signedTx],
    subchain: "sepolia",
    type: "contract_write",
    is_evm: true,
})

const signedDemosTx = await prepareXMPayload(xmscript, demos)
const validityData = await demos.confirm(signedDemosTx)
const result = await demos.broadcast(validityData)
```
