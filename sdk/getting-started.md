---
icon: circle-play
---

# Getting Started

### Installation

Install the latest version of the SDK with:

```bash
yarn add @kynesyslabs/demosdk@2.2.35
```

### Polyfills

When working on a browser environment, you need to configure polyfills for `Buffer`.

For a Vite project, this can be done using the [vite-plugin-node-polyfills](https://www.npmjs.com/package/vite-plugin-node-polyfills) plugin.

```bash
yarn add --dev vite-plugin-node-polyfills
```

Then update your `vite.config.ts` to register the plugin and select polyfills.

```typescript
import { defineConfig } from "vite";
import { nodePolyfills } from "vite-plugin-node-polyfills";

export default defineConfig({
  plugins: [
    // ...
    nodePolyfills({
      globals: {
        Buffer: true,
      },
    }),
  ],
});

```

Check out the [plugin documentation](https://www.npmjs.com/package/vite-plugin-node-polyfills) for configuring other polyfills.
