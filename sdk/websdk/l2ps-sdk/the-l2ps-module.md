---
icon: key-skeleton-left-right
---

# The l2ps module

To standardize this guide, it is advised to always import the `l2ps`module with:

```typescript
import { l2ps } from "@kynesyslabs/demosdk"
```

Once you have done this, you will be able to access the module classes and methods.

### Creating a new L2PS

You can easily create a new L2PS instance with:

```typescript
var instance = new l2ps.L2PS()
```

Which will generate the keys for the Subnet and return an instance of it.

### Using a pre-existing L2PS

To use a pre-existing L2PS, one must first obtain the RSA Private Key for the Subnet. This acts like a certification of participation to the Subnet.

{% hint style="warning" %}
This private key won't be sent to the node and will remain completely offline for the whole time.
{% endhint %}

Once obtained, you can create an instance of that L2PS with:

```typescript
var instance = new l2ps.L2PS(RSAPrivateKey)
```

Where `RSAPrivateKey`is the above-mentioned secret.
