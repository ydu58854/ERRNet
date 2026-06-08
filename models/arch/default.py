# Define network components here
import torch
from torch import nn
import torch.nn.functional as F


class PyramidPooling(nn.Module):
    def __init__(self, in_channels, out_channels, scales=(4, 8, 16, 32), ct_channels=1):
        super().__init__()
        self.stages = []
        self.stages = nn.ModuleList([self._make_stage(in_channels, scale, ct_channels) for scale in scales])
        self.bottleneck = nn.Conv2d(in_channels + len(scales) * ct_channels, out_channels, kernel_size=1, stride=1)
        self.relu = nn.LeakyReLU(0.2, inplace=True)

    def _make_stage(self, in_channels, scale, ct_channels):
        # prior = nn.AdaptiveAvgPool2d(output_size=(size, size))
        prior = nn.AvgPool2d(kernel_size=(scale, scale))
        conv = nn.Conv2d(in_channels, ct_channels, kernel_size=1, bias=False)
        relu = nn.LeakyReLU(0.2, inplace=True)
        return nn.Sequential(prior, conv, relu)

    def forward(self, feats):
        h, w = feats.size(2), feats.size(3)
        priors = torch.cat([F.interpolate(input=stage(feats), size=(h, w), mode='nearest') for stage in self.stages] + [feats], dim=1)
        return self.relu(self.bottleneck(priors))


class SELayer(nn.Module):
    def __init__(self, channel, reduction=16):
        super(SELayer, self).__init__()
        hidden = max(1, channel // reduction)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
                nn.Linear(channel, hidden),
                nn.ReLU(inplace=True),
                nn.Linear(hidden, channel),
                nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        
        return x * y        


class ChannelAttention(nn.Module):
    def __init__(self, channel, reduction=16):
        super(ChannelAttention, self).__init__()
        hidden = max(1, channel // reduction)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Sequential(
                nn.Linear(channel, hidden),
                nn.ReLU(inplace=True),
                nn.Linear(hidden, channel)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        b, c, _, _ = x.size()
        avg_y = self.fc(self.avg_pool(x).view(b, c))
        max_y = self.fc(self.max_pool(x).view(b, c))
        y = self.sigmoid(avg_y + max_y).view(b, c, 1, 1)

        return x * y


class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        if kernel_size % 2 == 0:
            raise ValueError('spatial attention kernel_size must be odd')
        padding = kernel_size // 2
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_y = torch.mean(x, dim=1, keepdim=True)
        max_y, _ = torch.max(x, dim=1, keepdim=True)
        y = torch.cat([avg_y, max_y], dim=1)
        y = self.sigmoid(self.conv(y))

        return x * y


class IdentitySpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(IdentitySpatialAttention, self).__init__()
        if kernel_size % 2 == 0:
            raise ValueError('spatial attention kernel_size must be odd')
        self.padding = kernel_size // 2
        self.weight = nn.Parameter(torch.zeros(1, 2, kernel_size, kernel_size))

    def forward(self, x):
        avg_y = torch.mean(x, dim=1, keepdim=True)
        max_y, _ = torch.max(x, dim=1, keepdim=True)
        y = torch.cat([avg_y, max_y], dim=1)
        y = 2.0 * torch.sigmoid(F.conv2d(y, self.weight, padding=self.padding))

        return x * y


class CBAMLayer(nn.Module):
    def __init__(self, channel, reduction=16, spatial_kernel_size=7):
        super(CBAMLayer, self).__init__()
        self.channel_attention = ChannelAttention(channel, reduction)
        self.spatial_attention = SpatialAttention(spatial_kernel_size)

    def forward(self, x):
        x = self.channel_attention(x)
        x = self.spatial_attention(x)

        return x


class SEIdentitySpatialLayer(nn.Module):
    def __init__(self, channel, reduction=16, spatial_kernel_size=7):
        super(SEIdentitySpatialLayer, self).__init__()
        self.channel_attention = SELayer(channel, reduction)
        self.spatial_attention = IdentitySpatialAttention(spatial_kernel_size)

    def forward(self, x):
        x = self.channel_attention(x)
        x = self.spatial_attention(x)

        return x


class DRNet(torch.nn.Module):
    def __init__(self, in_channels, out_channels, n_feats, n_resblocks, norm=nn.BatchNorm2d, 
    se_reduction=None, res_scale=1, bottom_kernel_size=3, pyramid=False, attention_type=None,
    reflection_residual_head=False):
        super(DRNet, self).__init__()
        # Initial convolution layers
        conv = nn.Conv2d
        deconv = nn.ConvTranspose2d
        act = nn.ReLU(True)
        self.reflection_residual_head = reflection_residual_head
        
        self.pyramid_module = None
        self.conv1 = ConvLayer(conv, in_channels, n_feats, kernel_size=bottom_kernel_size, stride=1, norm=None, act=act)
        self.conv2 = ConvLayer(conv, n_feats, n_feats, kernel_size=3, stride=1, norm=norm, act=act)
        self.conv3 = ConvLayer(conv, n_feats, n_feats, kernel_size=3, stride=2, norm=norm, act=act)

        # Residual layers
        dilation_config = [1] * n_resblocks

        self.res_module = nn.Sequential(*[ResidualBlock(
            n_feats, dilation=dilation_config[i], norm=norm, act=act, 
            se_reduction=se_reduction, res_scale=res_scale, attention_type=attention_type) for i in range(n_resblocks)])

        # Upsampling Layers
        self.deconv1 = ConvLayer(deconv, n_feats, n_feats, kernel_size=4, stride=2, padding=1, norm=norm, act=act)

        if not pyramid:
            self.deconv2 = ConvLayer(conv, n_feats, n_feats, kernel_size=3, stride=1, norm=norm, act=act)
            self.deconv3 = ConvLayer(conv, n_feats, out_channels, kernel_size=1, stride=1, norm=None, act=act)
        else:
            self.deconv2 = ConvLayer(conv, n_feats, n_feats, kernel_size=3, stride=1, norm=norm, act=act)
            self.pyramid_module = PyramidPooling(n_feats, n_feats, scales=(4,8,16,32), ct_channels=n_feats//4)
            self.deconv3 = ConvLayer(conv, n_feats, out_channels, kernel_size=1, stride=1, norm=None, act=act)
        self.reflection_head = None
        if self.reflection_residual_head:
            self.reflection_head = ConvLayer(conv, n_feats, out_channels, kernel_size=1, stride=1, norm=None, act=act)
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.res_module(x)

        x = self.deconv1(x)
        x = self.deconv2(x)
        if self.pyramid_module is not None:
            x = self.pyramid_module(x)
        output_t = self.deconv3(x)

        if self.reflection_head is None:
            return output_t

        output_r = self.reflection_head(x)
        return output_t, output_r


class ConvLayer(torch.nn.Sequential):
    def __init__(self, conv, in_channels, out_channels, kernel_size, stride, padding=None, dilation=1, norm=None, act=None):
        super(ConvLayer, self).__init__()
        # padding = padding or kernel_size // 2
        padding = padding or dilation * (kernel_size - 1) // 2
        self.add_module('conv2d', conv(in_channels, out_channels, kernel_size, stride, padding, dilation=dilation))
        if norm is not None:
            self.add_module('norm', norm(out_channels))
            # self.add_module('norm', norm(out_channels, track_running_stats=True))
        if act is not None:
            self.add_module('act', act)


class ResidualBlock(torch.nn.Module):
    def __init__(self, channels, dilation=1, norm=nn.BatchNorm2d, act=nn.ReLU(True), se_reduction=None, res_scale=1, attention_type=None):
        super(ResidualBlock, self).__init__()
        conv = nn.Conv2d
        self.conv1 = ConvLayer(conv, channels, channels, kernel_size=3, stride=1, dilation=dilation, norm=norm, act=act)
        self.conv2 = ConvLayer(conv, channels, channels, kernel_size=3, stride=1, dilation=dilation, norm=norm, act=None)
        self.se_layer = None
        self.cbam_layer = None
        self.se_identity_spatial_layer = None
        self.res_scale = res_scale
        self.attention_type = attention_type
        if self.attention_type is None:
            self.attention_type = 'se' if se_reduction is not None else 'none'
        if self.attention_type not in ('none', 'se', 'cbam', 'cbam_identity'):
            raise ValueError('unsupported attention_type: {}'.format(self.attention_type))
        attention_reduction = se_reduction or 16
        if self.attention_type == 'se':
            self.se_layer = SELayer(channels, attention_reduction)
        elif self.attention_type == 'cbam':
            self.cbam_layer = CBAMLayer(channels, attention_reduction)
        elif self.attention_type == 'cbam_identity':
            self.se_identity_spatial_layer = SEIdentitySpatialLayer(channels, attention_reduction)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.conv2(out)
        if self.se_layer:
            out = self.se_layer(out)
        if self.cbam_layer:
            out = self.cbam_layer(out)
        if self.se_identity_spatial_layer:
            out = self.se_identity_spatial_layer(out)
        out = out * self.res_scale
        out = out + residual
        return out

    def extra_repr(self):
        return 'res_scale={}, attention_type={}'.format(self.res_scale, self.attention_type)
