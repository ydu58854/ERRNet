import os
import random
import torch
import torch.distributed as dist
import numpy as np
from options.base_option import BaseOptions as Base
from util import util

class BaseOptions(Base):
    def initialize(self):
        Base.initialize(self)
        # experiment specifics
        self.parser.add_argument('--inet', type=str, default='errnet', help='chooses which architecture to use for inet.')
        self.parser.add_argument('--icnn_path', type=str, default=None, help='icnn checkpoint to use.')
        self.parser.add_argument('--init_type', type=str, default='edsr', help='network initialization [normal|xavier|kaiming|orthogonal|uniform]')
        # for network
        self.parser.add_argument('--hyper', action='store_true', help='if true, augment input with vgg hypercolumn feature')
        self.parser.add_argument(
            '--attention_type',
            type=str,
            default=None,
            choices=['none', 'se', 'cbam', 'cbam_identity'],
            help='optional residual block attention override; omit to preserve the selected architecture default',
        )
        self.parser.add_argument(
            '--reflection_residual_head',
            action='store_true',
            help='enable optional second 3-channel head for explicit reflection residual prediction',
        )
        
        self.initialized = True

    def parse(self):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()
        if hasattr(self, 'postprocess_options'):
            self.postprocess_options(self.opt)
        self.opt.isTrain = self.isTrain   # train or test

        str_ids = self.opt.gpu_ids.split(',')
        self.opt.gpu_ids = []
        for str_id in str_ids:
            id = int(str_id)
            if id >= 0:
                self.opt.gpu_ids.append(id)

        self.opt.rank = int(os.environ.get('RANK', '0'))
        self.opt.local_rank = int(os.environ.get('LOCAL_RANK', '0'))
        self.opt.world_size = int(os.environ.get('WORLD_SIZE', '1'))
        self.opt.distributed = self.opt.world_size > 1

        if self.opt.distributed:
            if not torch.cuda.is_available():
                raise RuntimeError('DDP training requires CUDA devices')
            torch.cuda.set_device(self.opt.local_rank)
            dist.init_process_group(backend='nccl', init_method='env://')
            self.opt.gpu_ids = [self.opt.local_rank]

        seed = self.opt.seed + self.opt.rank
        torch.backends.cudnn.deterministic = True
        torch.manual_seed(seed)
        np.random.seed(seed) # seed for every module
        random.seed(seed)

        batch_size = getattr(self.opt, 'batchSize', None)
        if len(self.opt.gpu_ids) > 1 and batch_size is not None and batch_size < len(self.opt.gpu_ids):
            print('[w] batchSize %d is smaller than %d GPUs; some GPUs may receive no samples.' %
                (batch_size, len(self.opt.gpu_ids)))

        # set gpu ids
        if len(self.opt.gpu_ids) > 0 and not self.opt.distributed:
            torch.cuda.set_device(self.opt.gpu_ids[0])

        args = vars(self.opt)

        if self.opt.rank == 0:
            print('------------ Options -------------')
            for k, v in sorted(args.items()):
                print('%s: %s' % (str(k), str(v)))
            print('-------------- End ----------------')

        # save to the disk
        self.opt.name = self.opt.name or '_'.join([self.opt.model])
        expr_dir = os.path.join(self.opt.checkpoints_dir, self.opt.name)
        if self.opt.rank == 0:
            util.mkdirs(expr_dir)
            file_name = os.path.join(expr_dir, 'opt.txt')
            with open(file_name, 'wt') as opt_file:
                opt_file.write('------------ Options -------------\n')
                for k, v in sorted(args.items()):
                    opt_file.write('%s: %s\n' % (str(k), str(v)))
                opt_file.write('-------------- End ----------------\n')

        if self.opt.distributed:
            dist.barrier()

        if self.opt.debug:
            self.opt.display_freq = 20
            self.opt.print_freq = 20
            self.opt.nEpochs = 40
            self.opt.max_dataset_size = 100
            self.opt.no_log = False
            self.opt.nThreads = 0
            self.opt.decay_iter = 0
            self.opt.serial_batches = True
            self.opt.no_flip = True
        
        return self.opt
