# Reactive Domain-Driven Design (RDDDY) Framework 

## Overview

The Reactive Domain-Driven Design (RDDDY) Framework is a Python-based solution designed to facilitate the development of reactive, domain-driven systems. At its core, the framework leverages the Actor model to encapsulate state and behavior, allowing for asynchronous message passing and ensuring loose coupling and enhanced system resilience. This README provides insights into the **why**, **what**, and **how** of utilizing the `ActorSystem` and `Actor` within the RDDDY framework.

## Why RDDDY?

In the landscape of modern software development, managing complexity and ensuring system reliability in the face of concurrent operations and distributed system architectures can be challenging. The RDDDY framework addresses these challenges by:

- **Encapsulating State and Behavior**: Each actor in the system manages its own state and behavior, reducing system complexity and enhancing modularity.
- **Facilitating Asynchronous Communication**: Actors communicate through asynchronous message passing, improving system responsiveness and scalability.
- **Promoting Domain-Driven Design**: The framework encourages the integration of domain-specific logic into the system's design, ensuring that software solutions are closely aligned with business requirements.
- **Enhancing Fault Tolerance**: By isolating actors and defining clear interaction patterns, the system improves its ability to recover from failures.

## What is the ActorSystem and Actor?

### ActorSystem

The `ActorSystem` acts as the orchestrator for actor lifecycle management, message passing, and system-wide coordination. It provides functionalities for:

- **Creating and Managing Actors**: Facilitates the instantiation and supervision of actors within the system.
- **Message Dispatching**: Supports both direct and broadcast messaging patterns, enabling actors to communicate asynchronously.
- **Maintaining System Invariants**: Ensures that the system's operational semantics and domain-specific assertions are preserved.

### Actor

`Actor` represents the fundamental unit of computation within the framework. Each actor:

- **Encapsulates its State**: Manages its internal state independently of other actors.
- **Processes Messages Asynchronously**: Handles incoming messages based on defined behaviors, allowing for reactive responses to events.
- **Interacts Through Message Passing**: Communicates with other actors via asynchronous message exchanges, without direct method calls.

## How to Use

### Implementing an Actor

Actors are implemented by subclassing the `Actor` class and defining message handlers for specific message types:

```python
class YourActor(Actor):
    async def handle_your_message(self, event: YourEventType):
        # Process the message.
        pass
```

### Creating Actors in the ActorSystem

```python
from rdddy.actor_system import ActorSystem

actor_system = ActorSystem()
your_actor = await actor_system.actor_of(YourActor)
```

### Publishing Messages

```python
# Broadcast message to all actors
await actor_system.publish(YourMessageType(...))
```

### Error Handling and System Invariants

The framework supports robust error handling and the maintenance of system invariants. Actors can catch exceptions during message processing and the `ActorSystem` can broadcast error events, ensuring the system remains responsive and resilient:

```python
class FaultyActor(AbstractActor):
    async def receive(self, your_command: YourCommand):
        # Implementation that might raise an exception
```

The `ActorSystem` detects exceptions, broadcasting an `Event` with error details, which can be tested and verified through the framework's testing capabilities.

## Abstract Classes

The Reactive Domain-Driven Design (RDDDY) framework offers a comprehensive suite of abstract classes, each serving as a template to guide the development of reactive, domain-driven systems. These classes lay the groundwork for creating domain-specific entities, value objects, and services that operate within an asynchronous, message-driven architecture. Below, we detail the role and purpose of each abstract class within the framework, elucidating how they contribute to building scalable, maintainable, and business-aligned software solutions.

### AbstractActor

`AbstractActor` is the fundamental building block of the RDDDY framework, representing the core unit of computation. It defines a standard interface for actors, encapsulating state management, message handling, and interaction protocols. Developers extend `AbstractActor` to implement domain-specific logic, leveraging asynchronous message passing to foster loose coupling and enhance system resilience.

### AbstractSaga

`AbstractSaga` encapsulates the logic for managing long-running, complex business transactions that span multiple services or bounded contexts. It provides mechanisms for orchestrating sequences of domain events and commands, ensuring transactional consistency and compensating actions in case of failures. By extending `AbstractSaga`, developers can implement coordinated workflows that are robust and aligned with business processes.

### AbstractView

`AbstractView` serves as the foundation for user interface components in a reactive system. It outlines methods for rendering data to the user and reacting to user inputs, enabling the development of dynamic and responsive user interfaces. Subclasses of `AbstractView` are tailored to specific UI requirements, responding to changes in the application's state with real-time updates.

### DomainException

While not prefixed with "Abstract," `DomainException` acts as a base class for defining domain-specific exceptions. These exceptions are used to signal error conditions in a way that is meaningful within the domain context, providing clear and actionable feedback to the system or the end-user. Custom exceptions derived from `DomainException` enhance error handling by incorporating domain-relevant information and context.

### AbstractValueObject

`AbstractValueObject` provides a template for creating value objects, which are immutable objects defined by their attributes rather than a unique identity. Value objects are crucial in domain-driven design for encapsulating and expressing domain concepts through their attributes. Extensions of `AbstractValueObject` ensure attribute-based equality and immutability, reinforcing domain integrity and consistency.

### AbstractTask

`AbstractTask` outlines the structure for tasks, which are discrete units of logic executed as part of the system's operations. Tasks encapsulate specific behaviors or processes, such as validation, computation, or state transitions, facilitating modularity and reuse. By defining tasks as subclasses of `AbstractTask`, the system can orchestrate complex operations while maintaining clarity and separation of concerns.

## Integration with Design for Lean Six Sigma (DFLSS)

Integrating the RDDDY framework with DFLSS principles underscores a commitment to process optimization, efficiency, and quality. The framework's emphasis on asynchronous communication, domain-driven design, and resilient architecture resonates with DFLSS goals of reducing variability, eliminating waste, and fostering continuous improvement. Through this synergy, developers can craft software systems that are not only technically sound but also streamlined and aligned with business excellence.


## Best Practices

Implementing the Reactive Domain-Driven Design (RDDDY) framework in enterprise environments requires careful consideration to fully leverage its benefits while ensuring scalability, maintainability, and alignment with business objectives. Below are best practices to guide enterprises in adopting the RDDDY framework effectively.

### Embrace Domain-Driven Design

1. **Ubiquitous Language**: Develop a common language based on the domain model that is shared among developers, domain experts, and stakeholders. This facilitates clear communication and ensures that software implementations are closely aligned with business concepts and requirements.
2. **Bounded Contexts**: Clearly define the boundaries of different domain contexts within the enterprise. This helps in isolating domain models and reducing complexity by ensuring that models within a context are internally consistent but decoupled from other contexts.

### Leverage Actors Strategically

1. **Actor Granularity**: Carefully consider the granularity of actors. Too fine-grained actors can lead to overhead in message passing, while too coarse-grained actors can decrease system responsiveness. Balance is key, with actors representing logically distinct units of functionality or state.
2. **Asynchronous Communication**: Maximize the use of asynchronous message passing for communication between actors. This enhances system responsiveness and scalability by avoiding blocking operations and enabling concurrent processing.

### Implement Sagas for Business Transactions

1. **Transaction Management**: Use sagas to manage complex, multi-step transactions across bounded contexts or microservices. Design sagas to handle success scenarios and compensate for failures, ensuring consistency and reliability in business operations.
2. **Saga Coordination**: Coordinate saga steps through events and commands, employing asynchronous messaging to orchestrate operations across distributed components without tight coupling.

### Focus on System Resilience

1. **Error Handling**: Implement robust error handling within actors and sagas. Define clear strategies for dealing with exceptions, including logging, compensation actions, and retries, to maintain system stability and integrity.
2. **Supervision Strategies**: Utilize actor supervision strategies to automatically manage actor lifecycle events, including restarts and escalations. This ensures that the system can recover gracefully from failures.

### Optimize for Performance and Scalability

1. **State Management**: Minimize the state held within actors to reduce memory footprint and enhance performance. Consider stateless actors where possible, and employ caching strategies judiciously for frequently accessed data.
2. **Distribute Workloads**: Design the system to distribute workloads evenly across actors and nodes in a cluster. Utilize routers and dispatchers to manage actor deployment and message routing, ensuring balanced utilization of resources.

### Foster Collaboration and Continuous Improvement

1. **Cross-functional Teams**: Encourage close collaboration between development teams, domain experts, and business stakeholders. This cross-functional approach ensures that the software development process is informed by deep domain knowledge and aligned with business goals.
2. **Iterative Development**: Adopt an iterative, incremental development process. Regularly review and refine the domain model, actor implementations, and system architecture to respond to changing requirements and leverage insights gained from ongoing operations.

### Invest in Monitoring and Observability

1. **System Monitoring**: Implement comprehensive monitoring for the actor system, tracking key metrics such as message throughput, processing times, and error rates. This enables proactive management of system performance and health.
2. **Observability**: Enhance system observability by incorporating detailed logging, tracing, and event recording. This aids in debugging, performance tuning, and understanding system behavior under various conditions.

By following these best practices, enterprises can successfully implement the RDDDY framework to build reactive, domain-driven systems that are scalable, resilient, and closely aligned with business needs. This strategic approach facilitates the development of software solutions that deliver tangible business value, fostering agility, efficiency, and competitive advantage.


## Conclusion

The RDDDY framework offers a powerful paradigm for building scalable, resilient, and domain-driven systems in Python. By leveraging the Actor model and embracing asynchronous communication, developers can tackle the complexities of modern software development, ensuring their applications are both robust and closely aligned with business objectives.

## Using

_Python package_: to add and install this package as a dependency of your project, run `poetry add rdddy`.

_Python CLI_: to view this app's CLI commands once it's installed, run `rdddy --help`.

_Python application_: to serve this REST API, run `docker compose up app` and open [localhost:8000](http://localhost:8000) in your browser. Within the Dev Container, this is equivalent to running `poe api`.

## Contributing

<details>
<summary>Prerequisites</summary>

<details>
<summary>1. Set up Git to use SSH</summary>

1. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) and [add the SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
1. Configure SSH to automatically load your SSH keys:
    ```sh
    cat << EOF >> ~/.ssh/config
    Host *
      AddKeysToAgent yes
      IgnoreUnknown UseKeychain
      UseKeychain yes
    EOF
    ```

</details>

<details>
<summary>2. Install Docker</summary>

1. [Install Docker Desktop](https://www.docker.com/get-started).
    - Enable _Use Docker Compose V2_ in Docker Desktop's preferences window.
    - _Linux only_:
        - Export your user's user id and group id so that [files created in the Dev Container are owned by your user](https://github.com/moby/moby/issues/3206):
            ```sh
            cat << EOF >> ~/.bashrc
            export UID=$(id --user)
            export GID=$(id --group)
            EOF
            ```

</details>

<details>
<summary>3. Install VS Code or PyCharm</summary>

1. [Install VS Code](https://code.visualstudio.com/) and [VS Code's Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). Alternatively, install [PyCharm](https://www.jetbrains.com/pycharm/download/).
2. _Optional:_ install a [Nerd Font](https://www.nerdfonts.com/font-downloads) such as [FiraCode Nerd Font](https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/FiraCode) and [configure VS Code](https://github.com/tonsky/FiraCode/wiki/VS-Code-Instructions) or [configure PyCharm](https://github.com/tonsky/FiraCode/wiki/Intellij-products-instructions) to use it.

</details>

</details>

<details open>
<summary>Development environments</summary>

The following development environments are supported:

1. ⭐️ _GitHub Codespaces_: click on _Code_ and select _Create codespace_ to start a Dev Container with [GitHub Codespaces](https://github.com/features/codespaces).
1. ⭐️ _Dev Container (with container volume)_: click on [Open in Dev Containers](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/chatmangpt/rdddy) to clone this repository in a container volume and create a Dev Container with VS Code.
1. _Dev Container_: clone this repository, open it with VS Code, and run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Dev Containers: Reopen in Container_.
1. _PyCharm_: clone this repository, open it with PyCharm, and [configure Docker Compose as a remote interpreter](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#docker-compose-remote) with the `dev` service.
1. _Terminal_: clone this repository, open it with your terminal, and run `docker compose up --detach dev` to start a Dev Container in the background, and then run `docker compose exec dev zsh` to open a shell prompt in the Dev Container.

</details>

<details>
<summary>Developing</summary>

- Run `poe` from within the development environment to print a list of [Poe the Poet](https://github.com/nat-n/poethepoet) tasks available to run on this project.
- Run `poetry add {package}` from within the development environment to install a run time dependency and add it to `pyproject.toml` and `poetry.lock`. Add `--group test` or `--group dev` to install a CI or development dependency, respectively.
- Run `poetry update` from within the development environment to upgrade all dependencies to the latest versions allowed by `pyproject.toml`.

</details>
