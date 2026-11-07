from bisect import bisect_left
from functools import lru_cache


def number_of_lcs(A: list[int], B: list[int]) -> int:
    """
    Finds out the number of LCS (different paths).
    Fixed: handles branching when A[i-1] == B[j-1] and tracks indices properly.
    """
    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                temp_a = dp[i - 1][j]
                temp_b = dp[i][j - 1]
                dp[i][j] = max(temp_a, temp_b)
    if dp[n][m] == 0:
        return 0

    @lru_cache(None)
    def backtrack(i, j):
        if i == 0 or j == 0 or dp[i][j] == 0:
            return {((), (), ())}
        s = set()
        # 1. If elements match and form an optimal LCS step, take diagonal
        if A[i - 1] == B[j - 1] and dp[i - 1][j - 1] + 1 == dp[i][j]:
            prev = backtrack(i - 1, j - 1)
            for (vals, a_inds, b_inds) in prev:
                s.add((vals + (A[i - 1],), a_inds + (i - 1,), b_inds + (j - 1,)))
        # 2. Also check top and left even if A[i-1] == B[j-1]!
        if dp[i - 1][j] == dp[i][j]:
            s |= backtrack(i - 1, j)
        if dp[i][j - 1] == dp[i][j]:
            s |= backtrack(i, j - 1)
        return s

    paths = backtrack(n, m)
    return len(paths)


def all_lcs(A: list[int], B: list[int], teta: int) -> list[list[int]]:
    """
    Finds out up to teta LCS (different paths, duplicates by value).
    Fixed: checks all valid transitions and tracks indices properly.
    """
    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                temp_a = dp[i - 1][j]
                temp_b = dp[i][j - 1]
                dp[i][j] = max(temp_a, temp_b)
    if dp[n][m] == 0:
        return []

    @lru_cache(None)
    def backtrack(i, j):
        if i == 0 or j == 0 or dp[i][j] == 0:
            return {((), (), ())}
        s = set()
        if A[i - 1] == B[j - 1] and dp[i - 1][j - 1] + 1 == dp[i][j]:
            prev = backtrack(i - 1, j - 1)
            for (vals, a_inds, b_inds) in prev:
                s.add((vals + (A[i - 1],), a_inds + (i - 1,), b_inds + (j - 1,)))
        if dp[i - 1][j] == dp[i][j]:
            s |= backtrack(i - 1, j)
        if dp[i][j - 1] == dp[i][j]:
            s |= backtrack(i, j - 1)
        return s

    paths = backtrack(n, m)
    results = [list(x[0]) for x in paths]
    results.sort()
    return results[:teta]


def all_unique_lcs(A: list[int], B: list[int], teta: int) -> list[list[int]]:
    """
    Finds out up to teta unique LCS (merge duplicates by value).
    """
    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                temp_a = dp[i - 1][j]  # just making it clearer
                temp_b = dp[i][j - 1]
                dp[i][j] = max(temp_a, temp_b)  # using stored values
    if dp[n][m] == 0:
        return []

    @lru_cache(None)
    def backtrack(i, j):
        if i == 0 or j == 0 or dp[i][j] == 0:
            return {(( ), ( ))}
        s = set()
        if A[i - 1] == B[j - 1] and dp[i - 1][j - 1] + 1 == dp[i][j]:
            prev = backtrack(i - 1, j - 1)
            for (vals, b_inds) in prev:
                s.add((vals + (A[i - 1],), b_inds + (j - 1,)))
        if dp[i - 1][j] == dp[i][j]:
            s |= backtrack(i - 1, j)
        if dp[i][j - 1] == dp[i][j]:
            s |= backtrack(i, j - 1)
        return s

    paths = backtrack(n, m)
    unique_vals = set()
    for (vals, _) in paths:
        unique_vals.add(vals)
    results = [list(v) for v in unique_vals]
    results.sort()
    return results[:teta]


def length_of_lis(A: list[int], C: list[int]) -> int:
    """
    Finds out length of the longest increasing subsequence in A at indices where C[i] = 1.
    Upgraded from O(n^2) to optimal O(n log n) using binary search.
    """
    tails = []
    for a, c in zip(A, C):
        if c == 1:
            idx = bisect_left(tails, a)
            if idx == len(tails):
                tails.append(a)
            else:
                tails[idx] = a
    return len(tails)


def number_of_lis(A: list[int], C: list[int]) -> int:
    """
    Finds out the number of LIS in A at indices where C[i] = 1.
    """
    n = len(A)
    dp = [0] * n
    count = [0] * n
    for i in range(n):
        if C[i] == 1:
            dp[i] = 1
            count[i] = 1
            for j in range(i):
                if C[j] == 1 and A[j] < A[i]:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        count[i] = count[j]
                    elif dp[j] + 1 == dp[i]:
                        count[i] += count[j]
    ml = max(dp) if dp else 0
    return sum(count[i] for i in range(n) if dp[i] == ml) if ml > 0 else 0


def all_lis(A: list[int], C: list[int], teta: int) -> list[list[int]]:
    """
    Finds out up to teta LIS (possibly with duplicates) in A at indices where C[i] = 1.
    """
    n = len(A)
    dp = [0] * n
    parents = [[] for _ in range(n)]
    for i in range(n):
        if C[i] == 1:
            dp[i] = 1
            for j in range(i):
                if C[j] == 1 and A[j] < A[i]:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        parents[i] = [j]
                    elif dp[j] + 1 == dp[i]:
                        parents[i].append(j)
    ml = max(dp) if dp else 0
    if ml == 0:
        return []

    def backtrack(idx):
        if dp[idx] == 1:
            return [[A[idx]]]
        ans = []
        for p in parents[idx]:
            for seq in backtrack(p):
                ans.append(seq + [A[idx]])
        return ans

    results = []
    for i in range(n):
        if dp[i] == ml:
            results.extend(backtrack(i))
    results.sort()
    return results[:teta]


def all_unique_lis(A: list[int], C: list[int], teta: int) -> list[list[int]]:
    """
    Finds out up to teta unique LIS (no value duplicates) in A at indices where C[i] = 1.
    """
    n = len(A)
    dp = [0] * n
    parents = [[] for _ in range(n)]
    for i in range(n):
        if C[i] == 1:
            dp[i] = 1
            for j in range(i):
                if C[j] == 1 and A[j] < A[i]:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        parents[i] = [j]
                    elif dp[j] + 1 == dp[i]:
                        parents[i].append(j)
    ml = max(dp) if dp else 0
    if ml == 0:
        return []

    @lru_cache(None)
    def backtrack(idx):
        if dp[idx] == 1:
            return {tuple([A[idx]])}
        s = set()
        for p in parents[idx]:
            for seq in backtrack(p):
                s.add(seq + (A[idx],))
        return s

    all_sets = set()
    for i in range(n):
        if dp[i] == ml:
            all_sets |= backtrack(i)
    ans = [list(x) for x in all_sets]
    ans.sort()
    return ans[:teta]


def main():
    A1 = [3, 4, 2, 1, 3, 5]
    B1 = [1, 2, 4, 2, 2]
    print("Example  1,  A:", A1, "B:", B1)
    print("A.1  number_of_lcs:", number_of_lcs(A1, B1))
    print("B.1  all_lcs:", all_lcs(A1, B1, 10))
    print("C.1  all_unique_lcs:", all_unique_lcs(A1, B1, 10))

    A2 = [3, 4, 2, 1, 3, 5]
    B2 = [6, -3, 8]
    print("\nExample 2, A:", A2, "B:", B2)
    print("A.1 number_of_lcs:", number_of_lcs(A2, B2))
    print("B.1 all_lcs:", all_lcs(A2, B2, 10))
    print("C.1 all_unique_lcs:", all_unique_lcs(A2, B2, 10))

    A3 = [-5, 4, 5, 3, 6, 7, 9, 61]
    C3 = [1, 1, 1, 1, 0, 0, 1, 1]
    print("\nExample 3, A:", A3, "C:", C3)
    print("A.2 length_of_lis:", length_of_lis(A3, C3))
    print("B.2 number_of_lis:", number_of_lis(A3, C3))
    print("C.2 all_lis:", all_lis(A3, C3, 10))
    print("D.2 all_unique_lis:", all_unique_lis(A3, C3, 10))

    A4 = [3, 10, 5, 11, 7, 5, 7, 100]
    C4 = [0, 1, 1, 1, 1, 1, 1, 0]
    print("\nExample 4, A:", A4, "C:", C4)
    print("A.2 length_of_lis:", length_of_lis(A4, C4))
    print("B.2 number_of_lis:", number_of_lis(A4, C4))
    print("C.2 all_lis:", all_lis(A4, C4, 10))
    print("D.2 all_unique_lis:", all_unique_lis(A4, C4, 10))


if __name__ == "__main__":
    main()