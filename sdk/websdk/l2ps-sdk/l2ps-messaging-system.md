---
icon: messages
---

# L2PS Messaging System

Within the `L2PS` class, a handful of high level methods are exposed to execute routine operations easily, without code redundancy.

In this chapter, we will see the messaging system enabled by the Subnets logic.

Before diving into the methods, it is useful to take a look at the `Message`type:

```typescript
type Message = { 
    messageId: string 
    sender: string 
    receiver: string 
    message: string 
    timestamp: number 
}
```

The type is mostly handled automatically by the methods below.

### sendMessage

This method compiles and send a `Message` within an `EncryptedTransaction`to the on-chain Subnet.

#### Arguments

* `address: string // The Demos Address of the receiver`
* `message: string // The message to be included in the transaction`

#### Returns

* `Promise<string> // The messageId of the specific Subnet message after being accepted by the network`

### retrieveMessages

This method returns all the messages received by an address in the Subnet.

**NOTE: If the retriever is not authorized to read those messages, they will be denied by the Subnet.**

#### Arguments

* `address: string // The address whose messages we want to retrieve`

#### Returns

* `Promise<MessageMap> // A Map<string Message> object (messageId -> Message)`

### retrieveSingleMessage

This method is used to retrieve a single message pertaining to an address.

#### Arguments

* `address: string // The address whom message we want to retrieve`
* `messageId: string // The messageId of the specific message to fetch`

#### Returns

* `Promise<Message>`
