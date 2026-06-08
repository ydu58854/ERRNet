import torch
import torch.distributed as dist
import util.util as util
import models
import time
import os
import sys
from os.path import join
from util.visualizer import Visualizer


class Engine(object):
    def __init__(self, opt):
        self.opt = opt
        self.writer = None
        self.visualizer = None
        self.model = None
        self.best_val_loss = 1e6

        self.__setup()

    def __setup(self):
        self.basedir = join('checkpoints', self.opt.name)
        if self.is_main_process and not os.path.exists(self.basedir):
            os.mkdir(self.basedir)
        if getattr(self.opt, 'distributed', False) and dist.is_initialized():
            dist.barrier()
        
        opt = self.opt
        
        """Model"""
        self.model = models.__dict__[self.opt.model]()
        self.model.initialize(opt)
        if self.is_main_process and not opt.no_log:
            self.writer = util.get_summary_writer(os.path.join(self.basedir, 'logs'))
            self.visualizer = Visualizer(opt)

    def train(self, train_loader, **kwargs):
        if hasattr(train_loader, 'sampler') and hasattr(train_loader.sampler, 'set_epoch'):
            train_loader.sampler.set_epoch(self.epoch)

        if self.is_main_process:
            print('\nEpoch: %d' % self.epoch)
        avg_meters = util.AverageMeters()
        opt = self.opt
        model = self.model
        epoch = self.epoch

        epoch_start_time = time.time()
        for i, data in enumerate(train_loader):
            iter_start_time = time.time()
            iterations = self.iterations
            

            model.set_input(data, mode='train')
            model.optimize_parameters(**kwargs)
            
            errors = model.get_current_errors()
            if self.is_main_process:
                avg_meters.update(errors)
                util.progress_bar(i, len(train_loader), str(avg_meters))
            
            if self.is_main_process and not opt.no_log:
                util.write_loss(self.writer, 'train', avg_meters, iterations)
            
                if iterations % opt.display_freq == 0 and opt.display_id != 0:
                    save_result = iterations % opt.update_html_freq == 0
                    self.visualizer.display_current_results(model.get_current_visuals(), epoch, save_result)

                if iterations % opt.print_freq == 0 and opt.display_id != 0:
                    t = (time.time() - iter_start_time)          

            self.iterations += 1
            if self.is_main_process and opt.save_iter_freq > 0 and self.iterations % opt.save_iter_freq == 0:
                print('saving the latest model at iter %d' % self.iterations)
                model.save(label='latest')

        self.epoch += 1

        if self.is_main_process and self.epoch % opt.save_epoch_freq == 0:
            print('saving the model at epoch %d, iters %d' %
                (self.epoch, self.iterations))
            model.save()

        if self.is_main_process:
            print('saving the latest model at the end of epoch %d, iters %d' %
                (self.epoch, self.iterations))
            model.save(label='latest')

        if self.is_main_process and not self.opt.no_log:
            print('Time Taken: %d sec' %
                (time.time() - epoch_start_time))
                
        # model.update_learning_rate()
        train_loader.reset()
        self.barrier()

    def save_checkpoint(self, label='latest'):
        if not self.is_main_process:
            return
        print('saving checkpoint %s at epoch %d, iters %d' %
            (label, self.epoch, self.iterations))
        self.model.save(label=label)

    def eval(self, val_loader, dataset_name, savedir=None, loss_key=None, **kwargs):
        
        avg_meters = util.AverageMeters()
        model = self.model
        opt = self.opt
        with torch.no_grad():
            for i, data in enumerate(val_loader):                
                index = model.eval(data, savedir=savedir, **kwargs)
                avg_meters.update(index)
                
                if self.is_main_process:
                    util.progress_bar(i, len(val_loader), str(avg_meters))
                
        if self.is_main_process and not opt.no_log:
            util.write_loss(self.writer, join('eval', dataset_name), avg_meters, self.epoch)
        
        if loss_key is not None:
            val_loss = avg_meters[loss_key]
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                print('saving the best model at the end of epoch %d, iters %d' % 
                    (self.epoch, self.iterations))
                model.save(label='best_{}_{}'.format(loss_key, dataset_name))

        return avg_meters

    def test(self, test_loader, savedir=None, **kwargs):
        model = self.model
        opt = self.opt
        with torch.no_grad():
            for i, data in enumerate(test_loader):
                model.test(data, savedir=savedir, **kwargs)
                if self.is_main_process:
                    util.progress_bar(i, len(test_loader))

    @property
    def iterations(self):
        return self.model.iterations

    @iterations.setter
    def iterations(self, i):
        self.model.iterations = i

    @property
    def epoch(self):
        return self.model.epoch

    @epoch.setter
    def epoch(self, e):
        self.model.epoch = e

    @property
    def is_main_process(self):
        return getattr(self.opt, 'rank', 0) == 0

    def barrier(self):
        if getattr(self.opt, 'distributed', False) and dist.is_initialized():
            dist.barrier()
