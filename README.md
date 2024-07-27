# Distributed Systems: Implementing Multicast, Vector Clocks, and Distributed Locking

This repository contains the solutions to three assignments focused on distributed systems. Each assignment demonstrates different concepts and techniques used in distributed computing.

## Table of Contents
- [Assignment 1: Totally Ordered Multicast](#assignment-1-totally-ordered-multicast)
- [Assignment 2: Vector Clock Implementation](#assignment-2-vector-clock-implementation)
- [Assignment 3: Distributed Locking Scheme](#assignment-3-distributed-locking-scheme)
- [Setup and Prerequisites](#setup-and-prerequisites)
- [How to Run](#how-to-run)
- [Acknowledgements](#acknowledgements)

## Assignment 1: Totally Ordered Multicast

This assignment implements a totally ordered multicast using Lamport's logical clock. Each process conducts local operations and multicasts events to other processes, ensuring the events are delivered in a total order.

### Files:
- `server1.py`
- `client1.py`

## Assignment 2: Vector Clock Implementation

This assignment implements a vector clock mechanism to achieve a consistent order of events across distributed processes. Each process maintains a vector clock and multicasts its events, which are delivered in a consistent order based on vector timestamps.

### Files:
- `server2.py`
- `client2.py`

## Assignment 3: Distributed Locking Scheme

This assignment implements a distributed locking scheme using Apache ZooKeeper to manage access to a shared file. The file contains a counter that is incremented by different processes, demonstrating mutual exclusion in a distributed environment.

### Files:
- `server3.py`
- `client3.py`
- `shared_file.txt` (initially contains `0`)

## Setup and Prerequisites

### Prerequisites:
- Python 3.x
- Apache ZooKeeper
- `kazoo` Python library

### Install Apache ZooKeeper:
1. Download and extract the latest stable release from the [Apache ZooKeeper website](https://zookeeper.apache.org/releases.html).
2. Navigate to the extracted directory and start the ZooKeeper server:
    ```sh
    bin/zkServer.sh start
    ```

### Install `kazoo`:
1. Create and activate a Python virtual environment:
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    ```
2. Install the `kazoo` library:
    ```sh
    pip install kazoo
    ```

## How to Run

### Assignment 1
1. Start the server:
    ```sh
    python3 server1.py
    ```
2. Start the client in a separate terminal:
    ```sh
    python3 client1.py
    ```

### Assignment 2
1. Start the servers:
    ```sh
    python3 server2.py
    ```
2. Start the clients in separate terminals:
    ```sh
    python3 client2.py
    ```

### Assignment 3
1. Ensure the ZooKeeper server is running:
    ```sh
    cd ~/Downloads/apache-zookeeper-3.8.4-bin
    bin/zkServer.sh start
    ```
2. Create a file named `shared_file.txt` and initialize it with `0`.
3. Start the server:
    ```sh
    python3 server3.py
    ```
4. Start the clients in separate terminals:
    ```sh
    python3 client3.py
    ```

## Acknowledgements
- The ZooKeeper-based locking mechanism is inspired by distributed coordination recipes provided by Apache ZooKeeper.
- Thanks to the course materials and lectures that provided the foundational knowledge for these assignments.
