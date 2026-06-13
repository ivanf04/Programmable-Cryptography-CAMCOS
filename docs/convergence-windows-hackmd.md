### How error % is calculated

For each input `x` and steepness `k`, the FHE routine returns an approximation
$\hat{y}(x)$ of the true sign. The true target is encoded on a **0/1 scale** (to
match the sigmoid/tanh output range):

$$
\text{sign}_\text{real}(x) =
\begin{cases}
1 & x > 0 \\
0.5 & x = 0 \\
0 & x < 0
\end{cases}
$$

The error at a point is the absolute distance from the approximation to that target,
reported as a percentage:

$$
\text{error\%}(x) = 100 \times \bigl|\, \hat{y}(x) - \text{sign}_\text{real}(x) \,\bigr|
$$

So on the right side (`x > 0`) it measures how far $\hat{y}$ is from **1**, and on the
left side (`x < 0`) how far it is from **0**. A point is counted as accurate when

$$
\text{error\%}(x) \le 100 \times \text{ACC\_TOL} = 10\%.
$$

The **bands** in the tables below are the contiguous ranges of `x` (searched inside
each function's convergence radius) where this 10% condition holds. The window width
is `outer − inner` of that range.

> **Why 10%?** The approximation's accuracy ceiling is ~8.3% — its best value is
> ≈0.917, never quite reaching 1 — so a 10% band is just wide enough to admit a
> usable window near the convergence radius.

---

### Tanh — ≤10% accuracy windows

| `k` | Left band | Right band | Window width |
|----:|:---------:|:----------:|:------------:|
|  1  | [-1.272, -1.105] | [1.105, 1.272] | 0.167 |
|  2  | [-0.636, -0.553] | [0.553, 0.636] | 0.083 |
|  4  | [-0.318, -0.277] | [0.277, 0.318] | 0.041 |
|  8  | [-0.159, -0.139] | [0.139, 0.159] | 0.020 |
| 16  | [-0.079, -0.070] | [0.070, 0.079] | 0.009 |
| 32  | [-0.040, -0.035] | [0.035, 0.040] | 0.005 |
| 64  | [-0.020, -0.018] | [0.018, 0.020] | 0.002 |

### Sigmoid — ≤10% accuracy windows

| `k` | Left band | Right band | Window width |
|----:|:---------:|:----------:|:------------:|
|  1  | [-2.543, -2.210] | [2.210, 2.543] | 0.333 |
|  2  | [-1.272, -1.105] | [1.105, 1.272] | 0.167 |
|  4  | [-0.636, -0.553] | [0.553, 0.636] | 0.083 |
|  8  | [-0.318, -0.277] | [0.277, 0.318] | 0.041 |
| 16  | [-0.159, -0.139] | [0.139, 0.159] | 0.020 |
| 32  | [-0.079, -0.070] | [0.070, 0.079] | 0.009 |
| 64  | [-0.040, -0.035] | [0.035, 0.040] | 0.005 |

