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
actor_system = ActorSystem()
your_actor = await actor_system.actor_of(YourActor)
```

### Sending and Publishing Messages

```python
# Direct message to a specific actor
await actor_system.send(your_actor.actor_id, YourMessageType(...))

# Broadcast message to all actors
await actor_system.publish(YourMessageType(...))
```

### Error Handling and System Invariants

The framework supports robust error handling and the maintenance of system invariants. Actors can catch exceptions during message processing and the `ActorSystem` can broadcast error events, ensuring the system remains responsive and resilient:

```python
class FaultyActor(Actor):
    async def receive(self, message: Message):
        # Implementation that might raise an exception
```

The `ActorSystem` detects exceptions, broadcasting an `Event` with error details, which can be tested and verified through the framework's testing capabilities.

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
