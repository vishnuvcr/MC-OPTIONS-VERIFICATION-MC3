# MC-RQ6-v1 Identity Test Protocol

1. Construct or retrieve the exact ordered 756-return historical vector for a signal date.
2. Record its first and last dates and a SHA-256 hash of the ordered float representation.
3. Record S0, horizon, paths, seed and software versions.
4. Generate the terminal array.
5. Hash the binary terminal array.
6. Compare the result with the predecessor MC1 implementation.
7. If a mismatch occurs, stop downstream interpretation and log the mismatch before any parameter optimization.
