# QWEPDT
The repository for the Qiskit codes that implement the algorithm: "Quantum-Walk Enhanced, Parrondo-Driven Decision Trees"
The file classical_parrondo.py contains the code for the classical analogue of the quantum algorithm QWEPDT.

The bennett folder contains the 3 different circuit versions included in the thesis.

The dirty folder contains the implementation of the version using dirty qubits.

The MCM_RESET folder contains 3 subfolders for 3, 5, and 10 execution steps. The name of each file indicates the execution methodology (RESET for the reset method and MCM for the mid circuit measurements method).

In the case of 10 steps (Reset): The reset-based implementation includes code for parallel execution across 10 CPU threads.

In the case of 10 steps (MCM): The MCM-based implementation includes code for running the algorithm on an NVIDIA GPU (execution in a Linux environment with the qiskit-aer-gpu package is required).
