# Dynamic Programming: LCS & Constrained LIS Algorithms in Python

An algorithmic suite implementing **Longest Common Subsequence (LCS)** and **Constrained Longest Increasing Subsequence (LIS)** counting, full path enumeration, and deduplicated sequence reconstruction using Dynamic Programming and DAG backtracking.

---

## Features & Algorithms

### 1. Longest Common Subsequence (LCS) — Counting & Enumeration
Given two integer sequences $A$ and $B$ of lengths $n$ and $m$:
* **`number_of_lcs(A, B)`**: Computes the exact number of maximum-length common subsequences.
* **`all_lcs(A, B, teta)`**: Reconstructs up to $\theta$ (`teta`) maximum-length common subsequences (including multiplicity across distinct index paths), sorted lexicographically.
* **`all_unique_lcs(A, B, teta)`**: Reconstructs up to $\theta$ value-unique longest common subsequences.

### 2. Constrained Longest Increasing Subsequence (LIS) with Binary Mask
Given an integer sequence $A$ and a binary mask $C \in \{0, 1\}^n$ restricting valid indices to $c_{i_k} = 1$:
* **`length_of_lis(A, C)`**: Computes the length of the constrained strictly increasing subsequence in optimal $O(n \log n)$ time using binary search (`bisect_left`).
* **`number_of_lis(A, C)`**: Computes the exact number of maximum-length constrained increasing subsequences.
* **`all_lis(A, C, teta)`**: Enumerates up to $\theta$ constrained LIS paths.
* **`all_unique_lis(A, C, teta)`**: Enumerates up to $\theta$ value-unique constrained LIS sequences.

---

## Complexity Analysis

| Function | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| `number_of_lcs` / `all_lcs` | $O(n \cdot m + \text{Paths})$ | $O(n \cdot m)$ | 2D DP table + memoized DAG backtracking |
| `all_unique_lcs` | $O(n \cdot m + \text{Unique Paths})$ | $O(n \cdot m)$ | Deduplicated via set collection |
| `length_of_lis` | $O(n \log n)$ | $O(n)$ | Optimized binary search (Patience Sorting) |
| `number_of_lis` / `all_lis` | $O(n^2)$ | $O(n)$ | 1D DP + predecessor DAG construction |

---

## Usage Example

```python
from LongestSubsequence import (
    number_of_lcs, all_lcs, all_unique_lcs,
    length_of_lis, number_of_lis, all_lis, all_unique_lis
)

# 1. Longest Common Subsequence (LCS)
A = [3, 4, 2, 1, 3, 5]
B = [1, 2, 4, 2, 2]

print("LCS Count:", number_of_lcs(A, B))               # Output: 2
print("All LCS:", all_lcs(A, B, teta=10))              # Output: [[4, 2], [4, 2]]
print("Unique LCS:", all_unique_lcs(A, B, teta=10))    # Output: [[4, 2]]

# 2. Constrained Longest Increasing Subsequence (LIS)
A_lis = [3, 10, 5, 11, 7, 5, 7, 100]
C_mask = [0, 1, 1, 1, 1, 1, 1, 0]

print("LIS Length:", length_of_lis(A_lis, C_mask))            # Output: 2
print("LIS Count:", number_of_lis(A_lis, C_mask))             # Output: 5
print("All LIS:", all_lis(A_lis, C_mask, teta=10))            # Output: [[5, 7], [5, 7], [5, 7], [5, 11], [10, 11]]
print("Unique LIS:", all_unique_lis(A_lis, C_mask, teta=10))  # Output: [[5, 7], [5, 11], [10, 11]]