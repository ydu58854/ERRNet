# Dataset And Weight Readiness

## Status

- Status: `completed`
- Recorded at: 2026-05-24

## Required Paths

| Artifact | Expected Path | Exists | Observed Count / Size | Notes |
| --- | --- | --- | --- | --- |
| Baseline checkpoint | `ERRNet/checkpoints/errnet/errnet_060_00463920.pt` | yes | 346772498 bytes | ready |
| Raw data root | `ERRNet/datasets/raw_data/` | yes | 43561 entries | ready |
| Processed data root | `ERRNet/datasets/processed_data/` | yes | 17651 entries | ready |
| Custom image p1 | `5pictures/p1.jpg` | yes | 308555 bytes | ready |
| Custom image p2 | `5pictures/p2.jpg` | yes | 255088 bytes | ready |
| Custom image p3 | `5pictures/p3.jpg` | yes | 103062 bytes | ready |
| Custom image p4 | `5pictures/p4.jpg` | yes | 262245 bytes | ready |
| Custom image p5 | `5pictures/p5.jpg` | yes | 286833 bytes | ready |

## Benchmark Datasets

| Dataset Key | Processed Path | Expected Use | Has Ground Truth | Observed Count | Status / Notes |
| --- | --- | --- | --- | --- | --- |
| `ceilnet_table2` | `ERRNet/datasets/processed_data/testdata_CEILNET_table2` | benchmark eval | yes | 200 files | ready |
| `real20` | `ERRNet/datasets/processed_data/real20` | benchmark eval | yes | 41 files | ready |
| `postcard` | `ERRNet/datasets/processed_data/postcard` | benchmark eval | yes | 358 files | ready |
| `objects` | `ERRNet/datasets/processed_data/objects` | benchmark eval | yes | 400 files | ready |
| `wild` | `ERRNet/datasets/processed_data/wild` | benchmark eval | yes | 202 files | ready |
| `sir2_withgt` | `ERRNet/datasets/processed_data/sir2_withgt` | benchmark eval | yes | 960 files | ready |

## Training / Finetuning Data

| Dataset | Expected Path | Usage | Observed Count | Status / Notes |
| --- | --- | --- | --- | --- |
| Pascal VOC | `ERRNet/datasets/processed_data/VOCdevkit` | aligned training | 15287 files | ready |
| real89 | `ERRNet/datasets/processed_data/real_train` | unaligned finetuning | 179 files | ready |

## Notes

- Custom images are qualitative by default because paired ground truth is not
  provided by this feature.
- Count discrepancies must be recorded before using results in paper/PPT
  evidence mapping.
- Counts are file counts from local filesystem traversal and include nested
  files under each directory.
