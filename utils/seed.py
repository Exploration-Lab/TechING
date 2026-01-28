import random
import torch
from transformers import set_seed as hf_set_seed
import numpy as np

def set_all_seeds(seed: int = 42):
    # Python and NumPy
    random.seed(seed)
    np.random.seed(seed)

    # PyTorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)          # if you use multi-GPU

    # cuDNN determinism
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark     = False

    # Hugging Face (Trainer, tokenizer shuffles, etc.)
    hf_set_seed(seed)