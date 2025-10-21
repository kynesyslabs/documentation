---
icon: puzzle-piece
---

# Demoswork

DemosWork is a module that helps you create a script (DemosScript) that can be executed on the omniweb.

A `DemosScript` is made up of these components:

1. Work steps - A step is a single action that can be executed on the omniweb.
2. Operations - An operation is a group of steps or a conditional.
3. The operation order - This is an ordered list of operation UIDs. It dictates the order in which the operations in a script are supposed to be executed.

DemosWork is implemented as a class that looks like this:

_@/demoswork/work.ts_

```ts
class DemosWork {
    script: DemoScript = {
        steps: {},
        operations: {},
        operationOrder: new Set<string>(),
    }

    push(operation: DemosWorkOperation)
    toJSON()
}
```

The `push` method adds an operation to the DemoScript.

API Reference: [https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.DemosWork.html](https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.DemosWork.html)

## Work steps

A work step is a single action that can be executed on the omniweb. It can either be a web2, xm or a native transaction. Say for example, sending tokens on Ethereum or calling a web2 API.

A work step is implemented as follows:

```ts
class WorkStep {
    id: string = "step_" + UID
    context: "xm" | "web2" | "native"
    content: WorkStepInput // payload specific to the context
    output: {
        [key: string]: StepOutputKey
    }
    description: string
    timestamp: number = Date.now()
    
    critical: boolean
    depends_on: string[]
}
```

The `critical` property is used to stop the execution of the `DemoScript` if this step fails. The `depends_on` array is a list of work steps or operations that should be executed successfully before this step is executed.



The `output` of a workstep indicated above is not the result of executing the step. Since we don't have that value yet, the output is represented as objects that operations can use to refer to the future/actual output of the step.

The `output` of a workstep indicated above is not the result of executing the step. Since we don't have that value yet, the output is represented as objects that operations can use to refer to the future/actual output of the step.

When executing an operation that needs an output of a step, that step will be executed and its result parsed using the key specified to get the value.

API Reference: [https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.WorkStep.html](https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.WorkStep.html)

## Operations

An operation controls the execution of steps therefore enabling scripting on the omniweb. An operation can be a group of steps or a conditional.

An operation is implemented as follows:

```ts
abstract class DemosWorkOperation {
    id: string = "op_" + UID
    abstract type: string

    steps: Record<string, WorkStep> = {}
    operations: Set<DemosWorkOperation> = new Set()
    output: any // specific to the operation type
    
    operationScript: OperationScript
    critical: boolean
    depends_on: string[]

    addWork(work: WorkStep | DemosWorkOperation): void
}
```

The `critical` property is used to stop the execution of the `DemoScript` if a step fails. The `depends_on` array is a list of worksteps or operations that should be executed successfully before an operation is executed.

The operation class indexes the steps and operations it contains in the `steps` and `operations` fields. The `operationScript` field is specific to the operation type and is copied into the main script when the operation is added to the work instance.

{% hint style="info" %}
The `addWork` method is used to add steps and operations to the operation (where applicable). If the work passed is an operation, its steps and operations are copied into the current operation.
{% endhint %}

### Conditional Operation

A conditional operation now builds on top of that:

_@/demoswork/operations/conditional/index.ts_

```ts
class Condition {
    id: string
    action: WorkStep | DemosWorkOperation = null
    value_a: Condition | Operand = null
    value_b: Condition | Operand = null
    work: Map<string, WorkStep | DemosWorkOperation> = new Map()
}

class ConditionalOperation extends DemosWorkOperation {
    type = "conditional"
    override operationScript: ConditionalOperationScript = {
        id: this.id,
        operationType: "conditional",
        conditions: new Map(),
        order: [],
    }

    constructor(...conditions: Condition[]): void

    if(value_a, operator, value_b)
    then(step: WorkStep | DemosWorkOperation)
    else(step: WorkStep | DemosWorkOperation)
}
```

A conditional operation is created by passing in conditions to the constructor. The `if`, `then` and `else` methods are helpers that can be used to build a conditional operation by chaining them together.

API Reference: [https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.ConditionalOperation.html](https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.ConditionalOperation.html)

### Base Operation

The base operation groups steps and operations together without any additional logic.

The base operation is implemented as follows:

_@/demoswork/operations/baseoperation.ts_

```ts
class BaseOperation extends DemosWorkOperation {
    type = "base"
    operationScript: BaseOperationScript = {
        id: this.id,
        operationType: "base",
        order: [],
    }

    constructor(...work: Array<WorkStep | DemosWorkOperation>)
    override addWork(...work: Array<WorkStep | DemosWorkOperation>): void
}
```

Work can be added to the base operation by passing in the work to the constructor or using the `addWork` method.

API Reference: [https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.BaseOperation.html](https://kynesyslabs.github.io/demosdk-api-ref/classes/demoswork.BaseOperation.html)

## The Operation Order

This is an ordered list of Operation UID strings. It dictates the order in which the operations in a script are supposed to be executed.
