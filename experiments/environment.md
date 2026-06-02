# Environment Record

## Status

- Status: `completed`
- Recorded at: 2026-05-25
- Recorder: Codex

## Runtime

| Field | Value | Source / Command |
| --- | --- | --- |
| OS | Linux dyh-cpu--210169a40253-c4wdt7jctr 5.15.0-141-generic x86_64 | `uname -a` |
| Python | Python 3.10.20 | `conda run -n errnet python --version` |
| Git commit | `25716669d3df94b052bdd6aecb6da2ca1f0d267a` | `git rev-parse HEAD` |
| Git branch | `001-errnet-reflection-spec` | `git branch --show-current` |
| Conda environment | `/opt/conda/envs/errnet` | `conda env list` |
| PyTorch | `2.7.0+cu128` | import check |
| CUDA available | `True` | `torch.cuda.is_available()` |
| CUDA version | `12.8` | `torch.version.cuda` |
| GPU model | NVIDIA GeForce RTX 4090 | `nvidia-smi --query-gpu=name --format=csv,noheader` |
| CPU fallback | completed | `test_errnet.py --gpu_ids -1 ...` |
| GPU smoke | completed | `test_errnet.py ...` |

## Dependency Snapshot

| Dependency | Version / Status | Source |
| --- | --- | --- |
| torch | `2.7.0+cu128` | import check |
| torchvision | `0.22.0+cu128` | import check |
| torchaudio | `2.7.0+cu128` | import check |
| numpy | `2.2.6` | import check |
| PIL/Pillow | `12.2.0` | import check |
| cv2/OpenCV | `4.13.0` | import check |
| skimage | `0.25.2` | import check |
| tensorboardX | installed | import check |
| visdom | `0.2.4` | import check |

## Packed Environment

| Field | Value |
| --- | --- |
| Archive path | `/inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/packed/errnet-py310-cu128-20260525.tar.gz` |
| Archive size | `4221294828` bytes |
| SHA256 | `95379e971c43b4d8a69ce2f5945ed080e9434fd9faa0be784fb09c1ab0131ccf` |
| Source environment | `/opt/conda/envs/errnet` |
| Pack command | `conda_pack.pack(name='errnet', output=..., ignore_missing_files=True)` |
| Archive validation | `tar -tzf ...` listed archive entries successfully |

Unpack and activate:

```bash
mkdir -p /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/errnet-py310-cu128
tar -xzf /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/packed/errnet-py310-cu128-20260525.tar.gz -C /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/errnet-py310-cu128
source /inspire/hdd/global_user/yanjunchi-24040/dyh/conda_envs/errnet-py310-cu128/bin/activate
conda-unpack
```

Run from the ERRNet repository:

```bash
cd /inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理/ERRNet
python test_errnet.py --name errnet --dataset ceilnet_table2 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper
```

The pack command used `ignore_missing_files=True` because the experiment guide's
`pip install -U pip wheel "setuptools<82"` step overwrote conda-managed
`pip`, `wheel`, and `setuptools` metadata. The live environment was tested
successfully before packing.

## Smoke Test Results

| Check | Command / Method | Result |
| --- | --- | --- |
| Import check | import torch, torchvision, torchaudio, skimage, cv2, tensorboardX, h5py, visdom | passed |
| CUDA check | `torch.cuda.is_available()` | `True`, RTX 4090 |
| Option parse | `--pixel_loss_weight 0.2 --gradient_loss_weight 0.4 --gpu_ids -1` | passed |
| CPU baseline smoke | `python test_errnet.py --name errnet_cpu_smoke --dataset ceilnet_table2 -r --gpu_ids -1 --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --max_dataset_size 1 --nThreads 0` | `PSNR 27.8767`, `SSIM 0.9407`, `NCC 0.9808`, `LMSE 0.0048` |
| GPU baseline smoke | `python test_errnet.py --name errnet_gpu_smoke --dataset ceilnet_table2 -r --icnn_path checkpoints/errnet/errnet_060_00463920.pt --hyper --max_dataset_size 1 --nThreads 0` | `PSNR 27.8770`, `SSIM 0.9407`, `NCC 0.9808`, `LMSE 0.0048` |

## Notes

- Default runtime compatibility boundary: CPU import/CPU inference plus
  optional single-card CUDA.
- Multi-card or distributed training is out of scope for this ERRNet PJ feature.
- The active ERRNet environment is ready for CPU and single-card CUDA baseline
  testing on this machine.
