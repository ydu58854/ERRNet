# Baseline Results

## Status

- Status: `completed; environment blocker rerun on 2026-05-25`
- Method: ERRNet baseline
- Checkpoint: `ERRNet/checkpoints/errnet/errnet_060_00463920.pt`
- Environment reference: `environment.md`
- Run logs: `ERRNet/experiments/run-logs/`

## Metric Semantics

| Field | Policy / Status |
| --- | --- |
| Prediction/target alignment | Existing `ERRNet/engine.py` and `ERRNet/models/errnet_model.py` evaluation path |
| Crop policy | Current eval crops output/target to shared minimum height/width when aligned |
| Pixel range | Images are converted to clipped `[0, 255]` arrays through `tensor2im` before metrics |
| Ground-truth requirement | Full-reference metrics require paired target images |
| Mask or valid-pixel policy | No explicit mask in current ERRNet eval; metrics use finite aligned pixels |
| NaN/inf handling | Run-log scan found no `nan` or `inf` tokens in the rerun logs |

## Baseline Smoke: `ceilnet_table2`

| Field | Value |
| --- | --- |
| Command | `conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python test_errnet.py --name errnet_benchmark_ceilnet_table2 --dataset ceilnet_table2 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --nThreads 0` |
| Working directory | `ERRNet/` |
| Status | `completed` |
| Output path | `ERRNet/results/CEILNet_table2/*/errnet_benchmark_ceilnet_table2.png` |
| Output count | `100` PNG outputs |
| Metrics | `LMSE 0.0048`, `NCC 0.9808`, `PSNR 27.8766`, `SSIM 0.9407` |
| Log | `ERRNet/experiments/run-logs/baseline_ceilnet_table2_20260525.log`, status `0` |

## CPU Fallback Smoke

| Field | Value |
| --- | --- |
| Command | `conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python test_errnet.py --name errnet_cpu_fallback_20260525 --dataset ceilnet_table2 -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --nThreads 0` |
| Working directory | `ERRNet/` |
| Status | `completed` |
| Output path | `ERRNet/results/CEILNet_table2/*/errnet_cpu_fallback_20260525.png` |
| Output count | `100` PNG outputs |
| Metrics | `LMSE 0.0048`, `NCC 0.9808`, `PSNR 27.8767`, `SSIM 0.9407` |
| Log | `ERRNet/experiments/run-logs/cpu_fallback_ceilnet_table2_20260525.log`, status `0` |

## Baseline Reproduction Summary

| Field | Value |
| --- | --- |
| Checkpoint path | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` |
| Dataset key | `ceilnet_table2` |
| Environment reference | `environment.md` |
| Command status | completed on GPU and CPU fallback |
| Metric status | measured |
| Result path status | generated under `ERRNet/results/CEILNet_table2/` |
| README sync | No baseline command change required; existing `test_errnet.py` contract remains valid |

## Full Benchmark Results

Benchmark command pattern:

```bash
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python test_errnet.py --name errnet_benchmark_<dataset> --dataset <dataset> -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --nThreads 0
```

| Method | Dataset | Samples | PSNR | SSIM | NCC | LMSE | Metric Status | GT Status | Crop/Alignment | Valid Pixels | NaN/inf | Output Path | Log |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| ERRNet baseline | `ceilnet_table2` | 100 | 27.8766 | 0.9407 | 0.9808 | 0.0048 | measured | paired target available | shared min H/W crop when aligned | finite aligned pixels, no explicit mask | none observed | `ERRNet/results/CEILNet_table2/*/errnet_benchmark_ceilnet_table2.png` | `baseline_ceilnet_table2_20260525.log` |
| ERRNet baseline | `real20` | 20 | 23.5531 | 0.8285 | 0.8877 | 0.0201 | measured | paired target available | shared min H/W crop when aligned | finite aligned pixels, no explicit mask | none observed | `ERRNet/results/real20/*/errnet_benchmark_real20.png` | `baseline_real20_20260525.log` |
| ERRNet baseline | `postcard` | 179 | 22.0710 | 0.8773 | 0.9463 | 0.0044 | measured | paired target available | shared min H/W crop when aligned | finite aligned pixels, no explicit mask | none observed | `ERRNet/results/postcard/*/errnet_benchmark_postcard.png` | `baseline_postcard_20260525.log` |
| ERRNet baseline | `objects` | 200 | 24.8530 | 0.8980 | 0.9817 | 0.0029 | measured | paired target available | shared min H/W crop when aligned | finite aligned pixels, no explicit mask | none observed | `ERRNet/results/objects/*/errnet_benchmark_objects.png` | `baseline_objects_20260525.log` |
| ERRNet baseline | `wild` | 101 | 25.1761 | 0.8861 | 0.9359 | 0.0083 | measured | paired target available | shared min H/W crop when aligned | finite aligned pixels, no explicit mask | none observed | `ERRNet/results/wild/*/errnet_benchmark_wild.png` | `baseline_wild_20260525.log` |
| ERRNet baseline | `sir2_withgt` | 480 | 23.8836 | 0.8878 | 0.9589 | 0.0046 | measured | paired target available | shared min H/W crop when aligned | finite aligned pixels, no explicit mask | none observed | `ERRNet/results/sir2_withgt/*/errnet_benchmark_sir2_withgt.png` | `baseline_sir2_withgt_20260525.log` |

All benchmark logs ended with status `0`.

## Custom Image Baseline

Command:

```bash
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 python test_errnet.py --name errnet_custom_baseline --dataset custom --input_dir ../5pictures --max_long_edge 1024 --save_subdir custom_baseline -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --nThreads 0
```

| Image | Input Path | Output Path | GT Status | Visual Notes | Status |
| --- | --- | --- | --- | --- | --- |
| p1 | `5pictures/p1.jpg` | `ERRNet/results/custom_baseline/p1/errnet_custom_baseline.png` | unavailable | qualitative only; output generated | completed |
| p2 | `5pictures/p2.jpg` | `ERRNet/results/custom_baseline/p2/errnet_custom_baseline.png` | unavailable | qualitative only; output generated | completed |
| p3 | `5pictures/p3.jpg` | `ERRNet/results/custom_baseline/p3/errnet_custom_baseline.png` | unavailable | qualitative only; output generated | completed |
| p4 | `5pictures/p4.jpg` | `ERRNet/results/custom_baseline/p4/errnet_custom_baseline.png` | unavailable | qualitative only; output generated | completed |
| p5 | `5pictures/p5.jpg` | `ERRNet/results/custom_baseline/p5/errnet_custom_baseline.png` | unavailable | qualitative only; output generated | completed |

Log: `ERRNet/experiments/run-logs/custom_baseline_20260525.log`, status `0`.

## Limitations

- Custom images remain qualitative because paired reflection-free ground truth is
  not available.
- Metric values should not be compared without matching environment,
  checkpoint, data preprocessing, alignment, and valid-pixel policy.
- The previous missing-`torch` blocker is resolved for this workspace through
  the `errnet` conda environment, but portability still depends on restoring the
  documented environment or packed archive.
- Success/failure case selection still requires human visual review of the
  generated custom-image outputs.
