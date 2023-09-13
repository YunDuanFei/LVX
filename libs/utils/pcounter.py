def gmpn(model):
    params_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return params_num
