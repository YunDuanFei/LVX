from tensorboardX import SummaryWriter
from datetime import datetime
import torch.optim as optim
from pathlib import Path
from libs import *
import logging
import warnings
import os


def main():
    ##################################
    # init params
    #################################
    args = make_args()
    eqstat = EqStat()
    setup_seed(args.seed)
    save_path = Path(args.logdir, eqstat.path)
    save_path.mkdir(parents=True, exist_ok=True)
    Writer = SummaryWriter(log_dir=save_path)
    logging.basicConfig(
        filename=os.path.join(save_path, 'run.log'),
        filemode='w',
        format='%(asctime)s: %(message)s',
        level=logging.INFO)
    warnings.filterwarnings("ignore")

    ##################################
    # load model scheduler optimizer
    #################################
    model = Lyapunov(eqstat)
    model.to(args.device)
    # optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.wtdecay)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = CosineAnnealingLR(optimizer, T_max=(args.iters - args.warm), warmup='linear', warmup_iters=args.warm, eta_min=1e-8)

    ##################################
    # train
    #################################
    train(model, optimizer, scheduler, gmpn, Writer, logging, args, eqstat, MCheckLyapunov, CheckLyapunov, AddCounterexamples, dataloader, exdataloader, EXCheckLyapunov)


if __name__ == '__main__':
    main()

