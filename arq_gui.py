import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import threading
import numpy as np

class ARQSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ARQ Protocol Simulator")
        self.root.geometry("1200x900")
        self.root.resizable(True, True)

        # Default parameters
        self.default_params = {
            'packet_size': 512,
            'num_packets': 100,
            'bandwidth': 1e6,
            'window_size': 10,
            'rtt': 0.1,  # Round Trip Time in seconds
            'timeout': 0.2,  # Timeout value in seconds (typically 2 * RTT)
            'error_range': (0, 0.9, 0.1)  # start, end, step
        }

        # Simulation results storage
        self.results = {
            'stop_and_wait': {'throughput': [], 'delay': []},
            'go_back_n': {'throughput': [], 'delay': []},
            'selective_repeat': {'throughput': [], 'delay': []}
        }

        self.setup_ui()
        self.create_plots()

    def setup_ui(self):
        """Setup the main UI components"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="ARQ Protocol Comparison Simulator",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Simulation Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Protocol Selection
        protocol_frame = ttk.LabelFrame(control_frame, text="Select Protocols to Compare", padding="5")
        protocol_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.stop_wait_var = tk.BooleanVar(value=True)
        self.go_back_n_var = tk.BooleanVar(value=True)
        self.selective_repeat_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(protocol_frame, text="Stop-and-Wait", variable=self.stop_wait_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(protocol_frame, text="Go-Back-N", variable=self.go_back_n_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(protocol_frame, text="Selective Repeat", variable=self.selective_repeat_var).grid(row=2, column=0, sticky=tk.W)

        # Parameters Frame
        params_frame = ttk.LabelFrame(control_frame, text="Simulation Parameters", padding="5")
        params_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Parameter inputs
        ttk.Label(params_frame, text="Packet Size (bytes):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.packet_size_var = tk.StringVar(value=str(self.default_params['packet_size']))
        ttk.Entry(params_frame, textvariable=self.packet_size_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(params_frame, text="Number of Packets:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.num_packets_var = tk.StringVar(value=str(self.default_params['num_packets']))
        ttk.Entry(params_frame, textvariable=self.num_packets_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(params_frame, text="Bandwidth (bps):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.bandwidth_var = tk.StringVar(value=str(self.default_params['bandwidth']))
        ttk.Entry(params_frame, textvariable=self.bandwidth_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(params_frame, text="Window Size:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.window_size_var = tk.StringVar(value=str(self.default_params['window_size']))
        ttk.Entry(params_frame, textvariable=self.window_size_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(params_frame, text="RTT (seconds):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.rtt_var = tk.StringVar(value=str(self.default_params['rtt']))
        ttk.Entry(params_frame, textvariable=self.rtt_var).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(params_frame, text="Timeout (seconds):").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.timeout_var = tk.StringVar(value=str(self.default_params['timeout']))
        ttk.Entry(params_frame, textvariable=self.timeout_var).grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)

        # Configure column weights for params_frame
        params_frame.columnconfigure(1, weight=1)

        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        self.run_button = ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=0, column=0, padx=(0, 5))

        self.reset_button = ttk.Button(button_frame, text="Reset Parameters", command=self.reset_parameters)
        self.reset_button.grid(row=0, column=1, padx=(5, 0))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        self.status_label = ttk.Label(control_frame, text="Ready to simulate")
        self.status_label.grid(row=4, column=0, sticky=tk.W, pady=(5, 0))

        # Right panel - Results
        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results", padding="10")
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Results notebook for different views
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Throughput tab
        self.throughput_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.throughput_frame, text="Throughput Comparison")

        # Delay tab
        self.delay_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.delay_frame, text="Delay Comparison")

        # Statistics tab
        self.stats_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.stats_frame, text="Statistics")

        # Configure results frame grid weights
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def create_plots(self):
        """Create matplotlib plots for results display"""
        # Throughput plot
        self.fig_throughput, self.ax_throughput = plt.subplots(figsize=(8, 6))
        self.canvas_throughput = FigureCanvasTkAgg(self.fig_throughput, master=self.throughput_frame)
        self.canvas_throughput.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Delay plot
        self.fig_delay, self.ax_delay = plt.subplots(figsize=(8, 6))
        self.canvas_delay = FigureCanvasTkAgg(self.fig_delay, master=self.delay_frame)
        self.canvas_delay.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure plot frames
        for frame in [self.throughput_frame, self.delay_frame, self.stats_frame]:
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)

    def reset_parameters(self):
        """Reset parameters to default values"""
        self.packet_size_var.set(str(self.default_params['packet_size']))
        self.num_packets_var.set(str(self.default_params['num_packets']))
        self.bandwidth_var.set(str(self.default_params['bandwidth']))
        self.window_size_var.set(str(self.default_params['window_size']))
        self.rtt_var.set(str(self.default_params['rtt']))
        self.timeout_var.set(str(self.default_params['timeout']))

    def get_parameters(self):
        """Get simulation parameters from GUI inputs"""
        try:
            params = {
                'packet_size': float(self.packet_size_var.get()),
                'num_packets': int(self.num_packets_var.get()),
                'bandwidth': float(self.bandwidth_var.get()),
                'window_size': int(self.window_size_var.get()),
                'rtt': float(self.rtt_var.get()),
                'timeout': float(self.timeout_var.get())
            }
            return params
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid parameter values: {str(e)}")
            return None

    def run_simulation(self):
        """Run the ARQ protocol simulations"""
        # Get parameters
        params = self.get_parameters()
        if not params:
            return

        # Check which protocols to run
        protocols_to_run = []
        if self.stop_wait_var.get():
            protocols_to_run.append('stop_and_wait')
        if self.go_back_n_var.get():
            protocols_to_run.append('go_back_n')
        if self.selective_repeat_var.get():
            protocols_to_run.append('selective_repeat')

        if not protocols_to_run:
            messagebox.showwarning("Selection Error", "Please select at least one protocol to simulate.")
            return

        # Disable run button during simulation
        self.run_button.config(state='disabled')
        self.status_label.config(text="Running simulation...")

        # Run simulation in a separate thread to avoid freezing GUI
        simulation_thread = threading.Thread(target=self._run_simulation_thread,
                                           args=(protocols_to_run, params))
        simulation_thread.daemon = True
        simulation_thread.start()

    def _run_simulation_thread(self, protocols_to_run, params):
        """Run simulation in background thread"""
        try:
            # Clear previous results
            for protocol in self.results:
                self.results[protocol]['throughput'] = []
                self.results[protocol]['delay'] = []

            # Error probabilities to test (0% to 90%)
            error_probs = np.arange(0, 0.91, 0.01)
            total_steps = len(error_probs) * len(protocols_to_run)
            current_step = 0

            # Run simulations for each protocol
            for protocol in protocols_to_run:
                throughputs = []
                delays = []

                for i, error_prob in enumerate(error_probs):
                    if protocol == 'stop_and_wait':
                        throughput, delay = self.simulate_stop_and_wait(
                            params['packet_size'], error_prob,
                            params['num_packets'], params['bandwidth'],
                            params['rtt'], params['timeout'])
                    elif protocol == 'go_back_n':
                        throughput, delay = self.simulate_go_back_n(
                            params['packet_size'], error_prob,
                            params['num_packets'], params['bandwidth'],
                            params['window_size'], params['rtt'], params['timeout'])
                    elif protocol == 'selective_repeat':
                        throughput, delay = self.simulate_selective_repeat(
                            params['packet_size'], error_prob,
                            params['num_packets'], params['bandwidth'],
                            params['window_size'], params['rtt'], params['timeout'])

                    throughputs.append(throughput)
                    delays.append(delay)

                    # Update progress
                    current_step += 1
                    progress = (current_step / total_steps) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))

                self.results[protocol]['throughput'] = throughputs
                self.results[protocol]['delay'] = delays

            # Update plots
            self.root.after(0, self.update_plots, error_probs)

            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Simulation completed"))
            self.root.after(0, lambda: self.run_button.config(state='normal'))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Simulation Error", f"An error occurred: {str(e)}"))
            self.root.after(0, lambda: self.run_button.config(state='normal'))
            self.root.after(0, lambda: self.status_label.config(text="Simulation failed"))

    def simulate_stop_and_wait(self, packet_size, error_probability, num_packets, bandwidth, rtt, timeout):
        """Simulate Stop-and-Wait ARQ protocol"""
        total_time = 0
        success_transmission = 0

        for i in range(num_packets):
            send_time = time.time()
            if random.random() > error_probability:
                # Successful transmission: data + ACK
                transmission_time = packet_size / bandwidth + rtt
                time.sleep(transmission_time * 0.001)  # Scale down for faster simulation
                total_time += time.time() - send_time
                success_transmission += 1
            else:
                # Timeout and retransmission
                total_time += timeout + packet_size / bandwidth + rtt

        throughput = success_transmission / total_time if total_time > 0 else 0
        delay = total_time / num_packets if num_packets > 0 else 0
        return throughput, delay

    def simulate_go_back_n(self, packet_size, error_probability, num_packets, bandwidth, window_size, rtt, timeout):
        """Simulate Go-Back-N ARQ protocol"""
        total_time = 0
        success_transmission = 0
        i = 0

        while i < num_packets:
            window = []

            # Send window
            for j in range(window_size):
                if i + j >= num_packets:
                    break
                send_time = time.time()
                window.append((i + j, send_time))

                if random.random() > error_probability:
                    transmission_time = packet_size / bandwidth
                    time.sleep(transmission_time * 0.001)
                    success_transmission += 1
                else:
                    # Error detected, will retransmit entire window
                    break

            # Receive ACKs
            error_occurred = False
            for seq_num, send_time in window:
                if seq_num >= num_packets:
                    break
                if random.random() > error_probability:
                    # Successful ACK
                    transmission_time = packet_size / bandwidth + rtt
                    time.sleep(transmission_time * 0.001)
                    total_time += time.time() - send_time
                else:
                    # NAK or timeout - retransmit entire window
                    total_time += timeout + packet_size / bandwidth + rtt
                    i = seq_num  # Go back to this packet
                    error_occurred = True
                    break

            if not error_occurred:
                i += window_size

        throughput = success_transmission / total_time if total_time > 0 else 0
        delay = total_time / num_packets if num_packets > 0 else 0
        return throughput, delay

    def simulate_selective_repeat(self, packet_size, error_probability, num_packets, bandwidth, window_size, rtt, timeout):
        """Simulate Selective Repeat ARQ protocol"""
        total_time = 0
        success_transmissions = 0
        i = 0

        while i < num_packets:
            window = []

            # Send window
            for j in range(window_size):
                if i + j >= num_packets:
                    break
                send_time = time.time()
                window.append((i + j, send_time))

                if random.random() > error_probability:
                    transmission_time = packet_size / bandwidth
                    time.sleep(transmission_time * 0.001)
                    success_transmissions += 1
                else:
                    # Error detected, will retransmit only this packet
                    pass

            # Receive ACKs - Selective Repeat only retransmits erroneous packets
            for seq_num, send_time in window:
                if seq_num >= num_packets:
                    break
                if random.random() > error_probability:
                    # Successful ACK
                    transmission_time = packet_size / bandwidth + rtt
                    time.sleep(transmission_time * 0.001)
                    total_time += time.time() - send_time
                else:
                    # NAK - retransmit only this packet
                    retransmit_time = packet_size / bandwidth + rtt
                    total_time += timeout + retransmit_time
                    success_transmissions += 1  # Count as successful after retransmission

            i += window_size

        throughput = success_transmissions / total_time if total_time > 0 else 0
        delay = total_time / num_packets if num_packets > 0 else 0
        return throughput, delay

    def update_plots(self, error_probs):
        """Update the matplotlib plots with simulation results"""
        # Clear previous plots
        self.ax_throughput.clear()
        self.ax_delay.clear()

        colors = {'stop_and_wait': 'blue', 'go_back_n': 'red', 'selective_repeat': 'green'}
        labels = {
            'stop_and_wait': 'Stop-and-Wait',
            'go_back_n': f'Go-Back-N (W={self.window_size_var.get()})',
            'selective_repeat': f'Selective Repeat (W={self.window_size_var.get()})'
        }

        # Plot throughput
        for protocol, data in self.results.items():
            if data['throughput']:
                self.ax_throughput.plot(error_probs, data['throughput'],
                                      color=colors[protocol], label=labels[protocol], linewidth=2)

        self.ax_throughput.set_xlabel('Error Probability')
        self.ax_throughput.set_ylabel('Throughput (packets/second)')
        self.ax_throughput.set_title('Throughput vs Error Probability')
        self.ax_throughput.legend()
        self.ax_throughput.grid(True, alpha=0.3)

        # Plot delay
        for protocol, data in self.results.items():
            if data['delay']:
                self.ax_delay.plot(error_probs, data['delay'],
                                 color=colors[protocol], label=labels[protocol], linewidth=2)

        self.ax_delay.set_xlabel('Error Probability')
        self.ax_delay.set_ylabel('Average Delay (seconds)')
        self.ax_delay.set_title('Average Delay vs Error Probability')
        self.ax_delay.legend()
        self.ax_delay.grid(True, alpha=0.3)

        # Redraw canvases
        self.canvas_throughput.draw()
        self.canvas_delay.draw()


def main():
    root = tk.Tk()
    app = ARQSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
