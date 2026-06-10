# Data Model: Phase C Exclusion-Loss Experiment

## Entity: Exclusion-Loss Option

| Field | Description | Validation |
| --- | --- | --- |
| `lambda_exclusion` | Scalar weight controlling the Phase C term | Float, default `0.0`; active only when greater than `0` |
| Active state | Whether the exclusion term contributes to generator loss | `False` when omitted or `0.0`; `True` when positive |
| Compatibility requirement | Old command behavior when disabled | Existing loss values and logs remain unchanged except option listing |

## Entity: Residual Proxy

| Field | Description | Validation |
| --- | --- | --- |
| Input tensor | Current blended input image | Existing training tensor; no new loader fields |
| Transmission tensor | Current model output | Existing model output |
| Residual tensor | `input - output` proxy for reflection residual | Same shape/device/dtype as input/output |
| Gradient tensors | Horizontal and vertical finite differences | Must remain finite for normal and degenerate tensors |

## Entity: Exclusion Loss

| Field | Description | Validation |
| --- | --- | --- |
| Gradient penalty | Product of normalized transmission/residual gradient magnitudes | Finite and non-negative |
| Epsilon | Denominator clamp for zero-gradient cases | Prevents division by zero |
| Weighted contribution | `lambda_exclusion * loss_exclusion` | Added only when option is active |
| Logged value | Unweighted exclusion loss | Present as `Excl` only when active |

## Entity: Phase C Run Record

| Field | Description | Validation |
| --- | --- | --- |
| Command | Exact training or evaluation command | Reproducible from repo root or `ERRNet/` |
| Status | Exit status file or logged status | `0` for completed smoke/evaluation |
| Checkpoint | Generated smoke or long-run checkpoint | Loadable by existing test command |
| Metrics | Existing PSNR/SSIM/NCC/LMSE for benchmarks | Same metric implementation as prior evidence |
| Custom outputs | Qualitative images for `5pictures/` | No full-reference metric claim |
| Conclusion | Improved, mixed, or rejected | Based on benchmark and custom evidence, not custom-only results |
