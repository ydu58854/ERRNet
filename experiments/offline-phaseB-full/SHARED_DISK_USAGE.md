# Shared Disk Usage

The training machine and this machine see the same project files, so do not
copy or package anything. Run these commands directly on the training machine
from the shared project path.

Two GPUs:

```bash
cd /inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理
bash ERRNet/experiments/offline-phaseB-full/run_train_pair_shared_disk.sh
bash ERRNet/experiments/offline-phaseB-full/run_eval_pair_shared_disk.sh
```

One GPU:

```bash
cd /inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理
GPU_CTX_VGG=0 GPU_CTX=0 bash ERRNet/experiments/offline-phaseB-full/run_train_pair_shared_disk.sh
GPU_CTX_VGG=0 GPU_CTX=0 bash ERRNet/experiments/offline-phaseB-full/run_eval_pair_shared_disk.sh
```

Outputs stay in place:

```text
ERRNet/checkpoints/errnet_phaseB_full_improved_ctx_vgg/
ERRNet/checkpoints/errnet_phaseB_full_improved_ctx/
ERRNet/experiments/run-logs/phaseB_full_*
ERRNet/results/phaseB_full_*
```

After those commands finish, no transfer step is needed.

The scripts use the shared project Torch cache by default:

```text
/inspire/hdd/global_user/yanjunchi-24040/dyh/数字图像处理/.torch/hub/checkpoints/vgg19-dcbb9e9d.pth
```
