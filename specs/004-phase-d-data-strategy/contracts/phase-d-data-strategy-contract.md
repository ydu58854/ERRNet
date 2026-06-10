# Contract: Phase D Data Strategy Experiment

## Planning Contract

Phase D must not change data semantics until the plan identifies:

- Candidate name
- Data semantic being changed
- Exact parameter values or schedule
- Default behavior preservation mechanism
- Smoke validation command
- Rollback rule
- Benchmark and custom evaluation commands

## Candidate Matrix Contract

Initial candidates:

| Candidate | Data Semantic | Values | Purpose |
| --- | --- | --- | --- |
| `gamma_1p1_1p5` | Synthetic gamma range | `low_gamma=1.1`, `high_gamma=1.5` | Add mild exposure variation |
| `gamma_1p0_1p8` | Synthetic gamma range | `low_gamma=1.0`, `high_gamma=1.8` | Stress wider exposure variation |
| `sigma_1_3` | Reflection blur sigma range | `low_sigma=1`, `high_sigma=3` | Test sharper reflections |
| `sigma_3_7` | Reflection blur sigma range | `low_sigma=3`, `high_sigma=7` | Test smoother/broader reflections |
| `curriculum_weak_to_strong` | Training schedule | early weak reflection, later stronger reflection | Test staged synthetic-to-real adaptation |

Implementation may run a smaller subset first, but it must explain which
candidates were deferred.

## Evaluation Contract

Every Phase D screening checkpoint must run:

```text
ceilnet_table2
real20
postcard
objects
wild
sir2_withgt
```

and custom qualitative inference on:

```text
../5pictures
```

Required health checks:

- Training status `0`
- Tensor scan reports `nonfinite=0`
- Six benchmark status files are `0`
- Custom inference status is `0`
- Output counts match prior expectations
- Log anomaly scan has no failure keywords

## Decision Contract

Improvement may be claimed only when benchmark evidence supports it. A
candidate is rejected if it has non-finite tensors, failed benchmark/custom
status, or broad regression relative to Phase C epoch 30 without compensating
dataset-specific evidence.
