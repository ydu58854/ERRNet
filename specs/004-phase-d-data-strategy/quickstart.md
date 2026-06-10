# Quickstart: Phase D Data Strategy Experiment

This quickstart records the repeatable verification used for Phase D screening
candidates. The first implemented candidate is `gamma_1p1_1p5`.

## 1. Locate Data Strategy Touchpoints

```bash
cd ERRNet
rg -n "low_sigma|high_sigma|low_gamma|high_gamma|reflect|reflection|alpha|opacity|blur|gamma" \
  data options train_errnet.py train_errnet_unaligned.py
```

Expected result: identify existing data generation and option paths before
editing anything.

## 2. Dataset Availability Check

```bash
cd ERRNet
for p in \
  datasets/processed_data/testdata_CEILNET_table2 \
  datasets/processed_data/real20 \
  datasets/processed_data/postcard \
  datasets/processed_data/objects \
  datasets/processed_data/wild \
  datasets/processed_data/sir2_withgt
do
  test -e "$p" && echo "ok $p" || echo "missing $p"
done
```

Expected result: all benchmark paths are available.

## 3. Synthetic Sample Smoke

Run a tiny data construction smoke before training a candidate:

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python - <<'PY'
from options.errnet.train_options import TrainOptions
from data.reflect_dataset import FusionDataset

opt = TrainOptions().parse()
opt.max_dataset_size = 2
dataset = FusionDataset(opt, is_for_train=True)
print("len", len(dataset))
sample = dataset[0]
print(sorted(sample.keys()))
PY
```

Expected result: dataset length is positive and one sample loads without decode
or shape errors.

For the implemented gamma candidate, include:

```bash
--phase_d_candidate gamma_1p1_1p5
```

## 4. Screening Training Template

Use exact candidate names and options from the implementation. Keep screening
to 10 or 20 epochs first:

```bash
cd ERRNet
CANDIDATE=gamma_1p1_1p5
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name "errnet_phaseD_${CANDIDATE}_10ep" \
    --phase_d_candidate "$CANDIDATE" \
    --hyper \
    --nEpochs 10 \
    --save_iter_freq 500 \
    --nThreads 0 \
    --display_id 0
```

Expected result: status `0`, finite losses, and a checkpoint.

Implemented candidate example:

```bash
cd ERRNet
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python train_errnet.py \
    --name errnet_phaseD_gamma_1p1_1p5_10ep \
    --phase_d_candidate gamma_1p1_1p5 \
    --hyper \
    --nEpochs 10 \
    --save_iter_freq 500 \
    --nThreads 0 \
    --display_id 0
```

## 5. Tensor Scan

Run the same tensor finite scanner used for Phase C and record SHA256, epoch,
floating tensor count, and `nonfinite=0`.

## 6. Benchmark And Custom Evaluation

Evaluate the same six benchmark datasets:

```bash
cd ERRNet
CANDIDATE=gamma_1p1_1p5
CHECKPOINT=checkpoints/errnet_phaseD_gamma_1p1_1p5_10ep/errnet_010_00077320.pt
for dataset in ceilnet_table2 real20 postcard objects wild sir2_withgt; do
  conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
    python test_errnet.py \
      --name "errnet_phaseD_${CANDIDATE}_${dataset}" \
      --dataset "$dataset" \
      --save_subdir "phaseD_${CANDIDATE}_${dataset}" \
      -r \
      --icnn_path "$CHECKPOINT" \
      --hyper \
      --nThreads 0
done
```

Run custom inference:

```bash
cd ERRNet
CANDIDATE=gamma_1p1_1p5
CHECKPOINT=checkpoints/errnet_phaseD_gamma_1p1_1p5_10ep/errnet_010_00077320.pt
conda run --no-capture-output -n errnet env PYTHONNOUSERSITE=1 \
  python test_errnet.py \
    --name "errnet_phaseD_${CANDIDATE}_custom" \
    --dataset custom \
    --input_dir ../5pictures \
    --max_long_edge 1024 \
    --save_subdir "phaseD_${CANDIDATE}_custom" \
    -r \
    --icnn_path "$CHECKPOINT" \
    --hyper \
    --nThreads 0
```

## Decision Rule

- Continue a candidate only if it is finite and improves the Phase C epoch-30
  comparison on targeted datasets without broad average regression.
- Prefer candidates that improve `objects`, `postcard`, and `sir2_withgt`
  without sacrificing `real20` and `wild`.
- Treat custom images as qualitative only.
