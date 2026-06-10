# ERRNet DIP26 Guide

## 1. Clone and Download

### 1.1 Clone the repository

```bash
git clone https://github.com/ydu58854/ERRNet.git
cd ERRNet
git checkout dip26
```

### 1.2 Setup the environment

Recommended on this workspace: use the packed ERRNet environment from the
persistent disk.

Archive:

```text
/inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/packed/errnet-py310-cu128-20260525.tar.gz
```

SHA256:

```text
95379e971c43b4d8a69ce2f5945ed080e9434fd9faa0be784fb09c1ab0131ccf
```

Unpack and activate:

```bash
mkdir -p /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/errnet-py310-cu128
tar -xzf /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/packed/errnet-py310-cu128-20260525.tar.gz -C /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/errnet-py310-cu128
source /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/errnet-py310-cu128/bin/activate
conda-unpack
```

Run commands from the ERRNet repository after activation:

```bash
cd /inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理/ERRNet
python test_errnet.py --name errnet --dataset ceilnet_table2 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

The current machine also has the live conda environment at
`/opt/conda/envs/errnet`, so this works without unpacking:

```bash
conda activate errnet
cd /inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理/ERRNet
python test_errnet.py --name errnet --dataset ceilnet_table2 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

To recreate the environment from scratch instead of using the archive:

```bash
conda create -n errnet python=3.10 -y
conda activate errnet
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
pip install -U pip wheel "setuptools<82"
pip install visdom==0.2.4 --no-build-isolation
```

Notes:
- Install the correct `torch`/`torchvision` version for your machine. Use a CUDA build if you have a GPU, and a CPU build otherwise. (Refer to https://pytorch.org/get-started/previous-versions/)
- The packed archive was created from the tested environment on 2026-05-25.
  It targets Python 3.10 and PyTorch 2.7.0 cu128 on Linux x86_64.

### 1.3 Download files

Download through [BaiduYun](https://pan.baidu.com/s/1MWb4eT18ySjogKVlcfPozg?pwd=egv2) or [GoogleDrive](https://drive.google.com/drive/folders/1_tN6JDlAmKZTgaqniQep1YJXmbFwGav7?usp=drive_link), then unzip and place files in ERRNet like this: 
```text
ERRNet/
  checkpoints/
    errnet/
      errnet_060_00463920.pt
  datasets/
    raw_data/
      VOCdevkit/
      CEILNet/
      real89/
      robustsirr_test_dataset/
      Dataset/
```

The GitHub repository intentionally excludes datasets, checkpoints, generated
benchmark outputs, custom-image outputs, and run logs. Keep those files locally
or publish model weights through a separate download link for final submission.

## 2. Prepare the Training and Testing Data


Run:

```bash
python datasets/prepare_test_data.py
python datasets/prepare_train_data.py
```


## 3. Testing

The testing script is `test_errnet.py`.

### 3.1 Benchmark testing

Supported benchmark names:

- `ceilnet_table2`
- `real20`
- `postcard`
- `objects`
- `wild`
- `sir2_withgt`

```bash
# gpu
python test_errnet.py --name errnet --dataset [dataset] -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
# cpu
python test_errnet.py --name errnet_cpu --dataset [dataset] -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```


### 3.2 Test on your own images

If you only want to run the model on your own reflection images, ground truth is not required. Put your images in any folder, for example:

```text
datasets/raw_data/my_test_images/
  img1.jpg
  img2.jpg
```

Run:
```bash
python test_errnet.py --name errnet --dataset custom --input_dir ./datasets/raw_data/my_test_images -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

Each image will have its own subfolder. You will usually see:

- `m_input.png`: the input image
- `errnet.png` or `errnet_cpu.png`: the model output

## 4. Training

There are two training stages:

- Aligned-data training: `train_errnet.py`
- Unaligned-data finetuning: `train_errnet_unaligned.py`

### 4.1 Train the aligned baseline

```bash
# gpu
python train_errnet.py --name errnet --hyper
# cpu
python train_errnet.py --name errnet_cpu --hyper --gpu_ids -1
```

Optional 8-GPU aligned training uses PyTorch DDP with one process per GPU:

```bash
torchrun --standalone --nproc_per_node=8 train_errnet.py \
  --name errnet_cbam_identity_10ep_ddp8 \
  --hyper \
  --attention_type cbam_identity \
  --batchSize 1 \
  --nEpochs 10 \
  --save_iter_freq 500 \
  --nThreads 4 \
  --display_id 0
```

Under `torchrun`, `batchSize` is per process. The example above gives effective
batch size `8`, split across eight GPU processes. Only rank `0` writes logs and
checkpoints. Checkpoints are saved without `module.` prefixes, so single-GPU
evaluation can still load them when the same architecture flags are used.

For a same-epoch SE-vs-attention control, run the default SE candidate with the
same DDP settings:

```bash
torchrun --standalone --nproc_per_node=8 train_errnet.py \
  --name errnet_se_10ep_ddp8 \
  --hyper \
  --batchSize 1 \
  --nEpochs 10 \
  --save_iter_freq 500 \
  --nThreads 4 \
  --display_id 0
```

Optional local loss-weight experiment:

```bash
python train_errnet.py --name errnet_loss_weight_smoke --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4
```

The defaults keep the aligned pixel-loss composition compatible with the
baseline: MSE weight `0.2` and GradientLoss weight `0.4`.

Optional Phase C exclusion-loss smoke:

```bash
python train_errnet.py --name errnet_phaseC_exclusion_smoke --hyper --lambda_exclusion 0.001 --nEpochs 1 --max_dataset_size 2 --nThreads 0 --display_id 0 --save_iter_freq 1
```

`--lambda_exclusion 0.0` is the default and disables the extra term. Positive
values add a transmission/residual gradient exclusion loss using `input -
output` as a residual proxy; this does not change the network, loader, metrics,
or checkpoint schema.

Optional residual-attention / CBAM screening:

```bash
python train_errnet.py --name errnet_cbam_10ep --hyper --attention_type cbam --nEpochs 10 --save_iter_freq 500 --nThreads 0 --display_id 0
```

Omitting `--attention_type` preserves the selected architecture default:
`errnet` keeps its original SE-style channel attention and `basenet` keeps no
residual-block attention. Passing `--attention_type cbam` replaces the residual
block attention with channel attention followed by spatial attention; data,
losses, metrics, and checkpoint wrapper fields stay unchanged. Train and
evaluate CBAM checkpoints with the same `--attention_type cbam` flag because
the generator parameters differ from SE checkpoints.

Passing `--attention_type cbam_identity` keeps the original SE channel attention
and adds an identity-initialized spatial gate. This is the conservative
attention candidate: at initialization the spatial gate multiplies features by
`1.0`, then learns deviations during training. Train and evaluate these
checkpoints with `--attention_type cbam_identity`.

Optional reflection-residual head training, matching the main structural
variant discussed in the course paper:

```bash
torchrun --standalone --nproc_per_node=8 train_errnet.py \
  --name errnet_reflection_residual_lamR005_lamC001_80ep_ddp8 \
  --hyper \
  --reflection_residual_head \
  --train_synthetic_only \
  --lambda_reflection 0.05 \
  --lambda_composition 0.01 \
  --batchSize 1 \
  --nEpochs 80 \
  --save_iter_freq 500 \
  --nThreads 4 \
  --display_id 0
```

Evaluate a reflection-residual checkpoint with the same architecture flag:

```bash
python test_errnet.py --name errnet_reflection_residual_lamR005_lamC001_80ep_ddp8 --dataset [dataset] -r --hyper --reflection_residual_head --icnn_path checkpoints/errnet_reflection_residual_lamR005_lamC001_80ep_ddp8/errnet_080_00076480.pt
```

`--reflection_residual_head` is off by default. The auxiliary terms are also off
unless `--lambda_reflection` or `--lambda_composition` is positive, so the
baseline commands remain compatible.

Optional Phase D data-strategy screening:

```bash
python train_errnet.py --name errnet_phaseD_gamma_1p1_1p5_10ep --hyper --phase_d_candidate gamma_1p1_1p5 --nEpochs 10 --save_iter_freq 500 --nThreads 0 --display_id 0
```

`--phase_d_candidate none` is the default and preserves the original synthetic
data parameters. The `gamma_1p1_1p5` preset changes only the synthetic gamma
range to `low_gamma=1.1` and `high_gamma=1.5`; omit the flag or pass `none` to
roll back to the old defaults.

For long aligned runs, save a refreshable latest checkpoint during an epoch:

```bash
python train_errnet.py --name errnet_improved_retrain_60ep --hyper --pixel_loss_weight 0.2 --gradient_loss_weight 0.4 --save_iter_freq 500
```

`--save_iter_freq 0` is the default and preserves the original epoch-only save
cadence.

### 4.2 Finetune on unaligned data


#### GPU version

```bash
# gpu
python train_errnet_unaligned.py --name errnet_unaligned_ft --hyper -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --unaligned_loss vgg
# cpu
python train_errnet_unaligned.py --name errnet_unaligned_ft_cpu --hyper -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --unaligned_loss vgg
```


## 5. Baseline Result

> checkpoints/errnet/errnet_060_00463920.pt

| Dataset | PSNR | SSIM | NCC | LMSE |
| --- | --- | --- | --- | --- |
| CEILNet Table 2 | 27.88 | 0.9407 | 0.9808 | 0.0048 |
| real20 | 23.55 | 0.8285 | 0.8877 | 0.0201 |
| objects | 24.85 | 0.8980 | 0.9817 | 0.0029|
| postcard | 22.07 | 0.8773 | 0.9463 | 0.0044 |
| wild | 25.18 | 0.886 | 0.9359 | 0.0083|
