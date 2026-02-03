from dotenv import load_dotenv
load_dotenv()

import os
os.environ['HF_HOME']= os.getenv("HF_DIRECTORY")
import torch
import argparse
import pandas as pd
from tqdm import tqdm
from PIL import Image
from torch.utils.data import Dataset, DataLoader

from transformers import pipeline, AutoModelForImageTextToText, AutoProcessor
from accelerate import Accelerator
import random
from transformers import set_seed as hf_set_seed
import numpy as np

from utils.hf_dataset_download import load_teching_dataset

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if using multi-GPU

    # Make CUDA and cuDNN deterministic
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    hf_set_seed(seed)

class DiagramDataset(Dataset):
    def __init__(self, hf_dataset):
        self.dataset = hf_dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        row = self.dataset[idx]
        image = row["Image"].convert("RGB")
        # mermaid_code = row["Mermaid Code"]
        return image

def collate_fn(batch, processor, prompt_template):
    images = batch
    messages = [
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": prompt_template}
        ]}
    ]
    input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(
        images=list(images),
        text=[input_text] * len(images),
        add_special_tokens=False,
        return_tensors="pt",
        padding=True
    )
    return inputs

def image2code(args):
    
    load_dotenv()
    os.environ['HF_TOKEN']= os.getenv("HF_ACCESS_TOKEN")
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{args.device}"
    device = torch.device(f"cuda" if torch.cuda.is_available() else "cpu")

    # Load model & processor
    processor = AutoProcessor.from_pretrained("meta-llama/Llama-3.2-11B-Vision-Instruct", device_map="auto")
    model = AutoModelForImageTextToText.from_pretrained("meta-llama/Llama-3.2-11B-Vision-Instruct",  device_map="auto")
    model.eval()
    prompt = f"""I am giving you a {args.diag_type} diagram in the form of an image. 
Analyze the diagram carefully and provide the Mermaid code for the diagram.
Do not provide steps for your analysis or any other information.
Just provide the Mermaid code in this format:

```mermaid

```
"""
    hf_dataset = load_teching_dataset(
        dataset_name=args.dataset.upper(),
        diag_type=args.diag_type, 
        split="test"
        )
    dataset = DiagramDataset(hf_dataset)

    def dynamic_collate(batch):
        inputs = collate_fn(batch, processor, prompt)
        return inputs.to(device)

    dataloader = DataLoader(
        dataset,
        batch_size=1,
        shuffle=False,
        collate_fn=dynamic_collate
    )

    responses = []
    with torch.no_grad():
        set_seed(args.seed)
        for inputs in tqdm(dataloader):
            outputs = model.generate(**inputs, 
                                     max_new_tokens=300, 
                                     temperature=0.9)
            for output in outputs:
                decoded = processor.decode(output)
                cleaned = decoded.split('<|end_header_id|>')[-1].split('<|eot_id|>')[0].strip()
                print(cleaned)
                responses.append(cleaned)
    # Save results to JSON
    df = pd.DataFrame(responses, columns=["Generated Code"])
    os.makedirs("baselines_eval/llama/results", exist_ok=True)
    output_path = os.path.join("baselines_eval/llama/results", f"{args.diag_type}_{args.task}_Responses.json")
    df.to_json(output_path, orient='records', lines=False, indent=4)
    print(f"Saved results to {output_path}")