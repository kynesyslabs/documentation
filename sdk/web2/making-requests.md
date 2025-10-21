---
icon: comments-question-check
---

# Making Requests

### GET Requests

```typescript
const response = await dahr.startProxy({
    url: "https://api.example.com",
    method: "GET",
})
```

### POST Requests

```typescript
const response = await dahr.startProxy({
    url: "https://api.example.com",
    method: "POST",
    options: {
        payload: {
            key: "value"
        },
        headers: { 
            Accept: "application/json" 
        }
    }
})
```

### Custom Headers

```typescript
const response = await dahr.startProxy({
    url: "https://api.example.com",
    method: "GET",
    options: {
        payload: {
            key: "value"
        },
        headers: {
            Authorization: "Bearer token",
            "Custom-Header": "value"
        }
    }
})
```
