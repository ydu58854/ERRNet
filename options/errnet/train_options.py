from .base_options import BaseOptions


PHASE_D_DATA_CANDIDATES = {
    'none': {},
    'gamma_1p1_1p5': {
        'low_gamma': 1.1,
        'high_gamma': 1.5,
    },
}


class TrainOptions(BaseOptions):
    def initialize(self):
        BaseOptions.initialize(self)        
        # for displays
        self.parser.add_argument('--display_freq', type=int, default=100, help='frequency of showing training results on screen')        
        self.parser.add_argument('--update_html_freq', type=int, default=1000, help='frequency of saving training results to html')
        self.parser.add_argument('--print_freq', type=int, default=100, help='frequency of showing training results on console')
        self.parser.add_argument('--no_html', action='store_true', help='do not save intermediate training results to [opt.checkpoints_dir]/[opt.name]/web/')
        self.parser.add_argument('--save_epoch_freq', type=int, default=10, help='frequency of saving checkpoints at the end of epochs')
        self.parser.add_argument('--save_iter_freq', type=int, default=0, help='frequency of saving the latest checkpoint by iteration; 0 disables iteration checkpointing')
        self.parser.add_argument('--debug', action='store_true', help='only do one epoch and displays at each iteration')

        # for training (Note: in train_errnet.py, we mannually tune the training protocol, but you can also use following setting by modifying the code in errnet_model.py)
        self.parser.add_argument('--nEpochs', '-n', type=int, default=60, help='# of epochs to run')
        self.parser.add_argument('--lr', type=float, default=1e-4, help='initial learning rate for adam')
        self.parser.add_argument('--wd', type=float, default=0, help='weight decay for adam')

        self.parser.add_argument('--low_sigma', type=float, default=2, help='min sigma in synthetic dataset')
        self.parser.add_argument('--high_sigma', type=float, default=5, help='max sigma in synthetic dataset')
        self.parser.add_argument('--low_gamma', type=float, default=1.3, help='max gamma in synthetic dataset')
        self.parser.add_argument('--high_gamma', type=float, default=1.3, help='max gamma in synthetic dataset')
        self.parser.add_argument(
            '--phase_d_candidate',
            type=str,
            default='none',
            choices=sorted(PHASE_D_DATA_CANDIDATES.keys()),
            help='optional Phase D data strategy preset; none preserves existing synthetic data parameters',
        )
        
        # data augmentation
        self.parser.add_argument('--batchSize', '-b', type=int, default=1, help='input batch size')
        self.parser.add_argument('--loadSize', type=str, default='224,336,448', help='scale images to multiple size')
        self.parser.add_argument('--fineSize', type=str, default='224,224', help='then crop to this size')
        self.parser.add_argument('--no_flip', action='store_true', help='if specified, do not flip the images for data augmentation')
        self.parser.add_argument('--resize_or_crop', type=str, default='resize_and_crop', help='scaling and cropping of images at load time [resize_and_crop|crop|scale_width|scale_width_and_crop]')
        self.parser.add_argument('--train_synthetic_only', action='store_true', help='train only on aligned synthetic CEIL data; default keeps existing synthetic/real fusion')

        # for discriminator
        self.parser.add_argument('--which_model_D', type=str, default='disc_vgg', choices=['disc_vgg', 'disc_patch'])
        self.parser.add_argument('--gan_type', type=str, default='rasgan', help='gan/sgan : Vanilla GAN; rasgan : relativistic gan')
        
        # loss weight
        self.parser.add_argument('--unaligned_loss', type=str, default='vgg', help='learning rate policy: vgg|mse|ctx|ctx_vgg')
        self.parser.add_argument('--vgg_layer', type=int, default=31, help='vgg layer of unaligned loss')
        
        self.parser.add_argument('--lambda_gan', type=float, default=0.01, help='weight for gan loss')
        self.parser.add_argument('--lambda_vgg', type=float, default=0.1, help='weight for vgg loss')
        self.parser.add_argument('--pixel_loss_weight', type=float, default=0.2, help='weight for MSE term inside aligned pixel loss')
        self.parser.add_argument('--gradient_loss_weight', type=float, default=0.4, help='weight for GradientLoss term inside aligned pixel loss')
        self.parser.add_argument('--lambda_laplacian', type=float, default=0.0, help='weight for optional aligned Laplacian edge guidance loss')
        self.parser.add_argument('--lambda_exclusion', type=float, default=0.0, help='weight for optional transmission/residual gradient exclusion loss')
        self.parser.add_argument('--lambda_reflection', type=float, default=0.0, help='weight for optional aligned reflection residual reconstruction loss')
        self.parser.add_argument('--lambda_composition', type=float, default=0.0, help='weight for optional input/transmission/reflection composition consistency loss')
        self.parser.add_argument('--composition_alpha', type=float, default=1.0, help='reflection scale alpha in input ~= T_hat + alpha * R_hat consistency loss')
        
        self.isTrain = True

    def postprocess_options(self, opt):
        candidate = PHASE_D_DATA_CANDIDATES[opt.phase_d_candidate]
        for name, value in candidate.items():
            setattr(opt, name, value)
