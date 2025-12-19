# ARQ Protocol Simulator: Implementation of Stop-and-Wait, Go-Back-N, and Selective-Repeat Protocols

**Automatic Repeat Request (ARQ) protocols are essential for ensuring reliable data transmission over noisy and unstable communication channels.** As modern networks require higher accuracy, lower delays, and better energy efficiency, researchers have continuously improved ARQ mechanisms such as Stop-and-Wait, Go-Back-N, and Selective-Repeat. Early work focused on basic error detection and retransmission, while recent studies explore channel-adaptive methods, buffer management, and advanced analytical models like Hidden Markov Models. These advancements aim to enhance throughput and reliability while reducing delay, retransmission overhead, and resource usage. Overall, the literature shows a strong focus on optimizing ARQ protocols to achieve efficient and dependable communication in real-world network environments.

**The Stop-and-Wait ARQ Simulator is designed to demonstrate the working principles, performance, and limitations of the Stop-and-Wait Automatic Repeat reQuest (ARQ) protocol used in reliable data communication systems.** This project models how frames are transmitted one at a time, acknowledged, and retransmitted in case of errors or losses, ensuring ordered and error-free delivery. The simulator incorporates essential mechanisms such as sequence numbering, ACK/NAK handling, timeout-based retransmission, and CRC-based error detection. Through this simulation, users can visualize flow-control and error-control behavior, observe frame loss scenarios, and compare protocol efficiency under different propagation delays and channel conditions. The results validate the protocol's correctness using safety and liveness properties while highlighting its major limitation—low channel utilization due to idle waiting time. The simulator serves as an educational tool to understand fundamental ARQ operations and provides a basis for comparing advanced protocols like Go-Back-N and Selective Repeat.

**Created by:** Aidan Azkafaro, Kemas Rafly Omar Thoriq, and Melchior Natthan V H F H

## Getting Started
To use this program, you will need to have Python 3 installed on your computer. You can download Python 3 from the official website: [Python](https://www.python.org/downloads/)

Once you have Python 3 installed, you can download the program from the GitHub repository: [Github](https://github.com/aidanazkafaro/ARQ-Simulator)

## Running the Program

### GUI Version (Recommended)
The GUI version provides an interactive interface for comparing ARQ protocols with real-time charts and easy parameter adjustment.

**Requirements:**
```bash
pip install -r requirements.txt
```

**Run the GUI:**
```bash
python arq_gui.py
```

### Command Line Version
You can run the program through cloud with relp.it in [this link](https://replit.com/@MelchiorNatthan/ARQ)

or

To run the command-line version, enter the following command:

```py
python arq_sim.py
```
This will start the program and display the main menu.

## ARQ Methods
The program can simulate three ARQ methods:

```
Stop-and-Wait
Go-Back-N
Selective Repeat
```

### GUI Features
The GUI version provides:
- **Interactive Protocol Selection**: Choose which protocols to compare simultaneously (Stop-and-Wait, Go-Back-N, Selective Repeat)
- **Comprehensive Parameter Configuration**:
  - Packet Size (bytes)
  - Number of Packets
  - Bandwidth (bps)
  - Window Size (for sliding window protocols)
  - Round Trip Time (RTT)
  - Timeout Values
- **Real-time Charts**: View throughput and delay comparisons with matplotlib integration
- **Progress Tracking**: Monitor simulation progress with a progress bar
- **Tabbed Results**: Separate tabs for throughput analysis, delay analysis, and statistics
- **Error Probability Range**: Automatic testing from 0% to 90% error rates
- **Protocol-Specific Visualizations**: Compare performance across different network conditions

### Protocol Implementations
- **Stop-and-Wait ARQ**: Demonstrates basic error control with sequence numbering and ACK/NAK handling
- **Go-Back-N ARQ**: Sliding window protocol with cumulative acknowledgments
- **Selective Repeat ARQ**: Advanced sliding window with individual packet retransmission
- **Timeout-Based Retransmission**: Configurable timeout mechanisms for reliable delivery
- **CRC-Based Error Detection**: Frame-level error detection and correction

### Command Line Version
Each method has its own menu, where you can set the parameters for the simulation, such as the number of packets to send and the probability of a packet being lost or corrupted.

## Contributing
If you would like to contribute to this program, feel free to fork the GitHub repository and submit a pull request. You can also open an issue if you find a bug or have a suggestion for a new feature.

## Authors
1. [Aidan Azkafaro](https://github.com/aidanazkafaro/)
2. [Kemas Rafly Omar Thoriq](https://github.com/grandier)
3. [Melchior Natthan V H F H](https://github.com/melchiornatthan)

### Educational Value
This simulator serves as an educational tool to understand:
- **Data Link Layer Protocols**: Fundamental concepts of reliable data transmission
- **Flow Control vs Error Control**: Understanding buffering and retransmission strategies
- **Performance Analysis**: Throughput vs Delay trade-offs in network protocols
- **Protocol Limitations**: Why Stop-and-Wait has low utilization, and how sliding windows improve efficiency
- **Safety and Liveness Properties**: Ensuring reliable and deadlock-free communication

### Keywords
Stop-and-Wait ARQ, Automatic Repeat reQuest, Data Link Layer, Error Control, Flow Control, Acknowledgment (ACK/NAK), Timeout Mechanism, Sequence Numbering, Frame Retransmission, CRC Error Detection, Protocol Efficiency, Propagation Delay, Reliable Communication, Sliding Window Protocols, Go-Back-N, Selective Repeat, Channel Utilization, Retransmission Overhead, Network Simulation, Computer Networks Education.

## License
This program is licensed under the MIT License. See the LICENSE file for more information.
