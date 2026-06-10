# Data Model: Phase D Data Strategy Experiment

## Entity: Data Strategy Candidate

| Field | Description | Validation |
| --- | --- | --- |
| `candidate_id` | Stable short name such as `gamma_1p1_1p5` | Unique within Phase D |
| `changed_semantic` | Data behavior being changed | One of gamma range, blur sigma range, reflection strength/opacity, color perturbation, curriculum |
| `parameter_values` | Candidate-specific values | Explicit numeric ranges or staged schedule |
| `expected_signal` | Dataset/metric behavior expected to improve | Must name target benchmark groups |
| `risk` | Known failure or regression mode | Must be documented before training |
| `rollback` | How to return to default behavior | Must preserve old data path |

## Entity: Screening Run

| Field | Description | Validation |
| --- | --- | --- |
| `name` | Training run name and checkpoint directory | Distinct from baseline/Phase B/Phase C |
| `candidate_id` | Candidate under test | Links to a Data Strategy Candidate |
| `epochs` | Short screening length | Usually 10 or 20 before full training |
| `command` | Exact training command | Reproducible from `ERRNet/` |
| `status` | Training exit status | `0` required before evaluation |
| `checkpoint` | Selected checkpoint path | Must tensor-scan finite |
| `logs` | Training/tensor/eval/custom logs | Must be preserved under run-logs |

## Entity: Benchmark Alignment Record

| Field | Description | Validation |
| --- | --- | --- |
| `datasets` | Six benchmark dataset keys | Must include `ceilnet_table2`, `real20`, `postcard`, `objects`, `wild`, `sir2_withgt` |
| `metrics` | PSNR, SSIM, NCC, LMSE | Existing implementation only |
| `output_counts` | PNG counts per result directory | Must match prior triplet-count expectations |
| `custom_outputs` | Qualitative `5pictures/` outputs | No full-reference metrics |
| `comparison_refs` | Baseline, aligned epoch60, Phase C epoch30 | Required for decision |

## Entity: Decision Record

| Field | Description | Validation |
| --- | --- | --- |
| `technical_status` | Whether training/eval completed and tensors are finite | Required before quality decision |
| `quality_status` | Improved, mixed, or rejected | Based on benchmarks first |
| `next_action` | Continue, adjust candidate, or stop | Must cite evidence |
| `residual_risk` | Known caveats | Must include small-epoch uncertainty when applicable |
