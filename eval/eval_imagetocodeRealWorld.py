from tqdm import tqdm
import torch
import pandas as pd
from model.llama import get_model
import os
from eval.parser import parse_args
configs = {
    'D3-Block': 'Block',
    'D3-C4': 'C4',
    'D3-Class': 'Class',
    'D3-Flowchart': 'Flowchart',
    'D3-Graph': 'Graph',
    'D3-Packet': 'Packet',
    'D3-Sequence': 'Sequence',
    'D3-State': 'State'
}
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("HF_TOKEN")
def main(args):
    
    from data.dataset import processor, get_dataset
    model = get_model(args).to(torch.bfloat16).to('cuda')
    
    test_dataset = get_dataset(train=False, data='D3')
    print(test_dataset)
    for diag_type, dataset in test_dataset.items():
        df = pd.DataFrame(columns=['Diagram Type','Ground Truth', 'Generation'])
        i = 0
        for item in tqdm(dataset, desc=f"{diag_type}: "):
            img = item['Handdrawn_Diag']
            messages = [
                {"role": "user", "content": [
                    {"type": "image"},
                    {"type": "text", "text": 'Generate the Mermaid code for the provided image'}
                ]}
            ]

            input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
            inputs = processor(
                img,
                input_text,
                add_special_tokens=False,
                return_tensors="pt"
            ).to(model.device)

            output = model.generate(**inputs, max_new_tokens=300)

            output = processor.decode(output[0])

            output = output.split('<|end_header_id|>')[-1].split('<|eot_id|>')[0].strip().split('```mermaid')[-1].split('```')[0].strip()
            df.loc[i] = [diag_type, item['Mermaid Code'], output]
            i+=1
        df.to_csv(os.path.join(args.output_dir, f"{configs[diag_type]}_Image2Code_RealWorld.csv"), index=False)

if __name__ == '__main__':
    args = parse_args()
    args.hf_token = token
    main(args)


