from utils.augmentations import augment_pil_image, transform
import random
import os
from utils.prompts import (
    image_to_code,
    description_to_code,
    image_to_summary,
    code_to_descriptions,
    image_to_code_and_description_prompts,
    incomplete_image_prompt_to_code,
    incomplete_image_plus_description_to_code,
    perturbed_code_plus_prompt_to_code,
    perturbed_code_plus_description_to_code,
    perturbed_image_code_plus_improvement_to_code,
    image_code_relation_prompts,
    yes_image_code_responses,
    no_image_code_responses,
    more_image_code_info_responses,
    more_code_image_info_responses,
    yes_responses_image_description,
    no_responses_image_description
)
from transformers import AutoProcessor
from datasets import load_dataset, concatenate_datasets


model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

processor = AutoProcessor.from_pretrained(model_id)


def get_dataset(train:bool = True, data:str = 'D1+D2'):
    if train and data == 'D1+D2':
        configs = [
            "D1-Block", "D1-C4", "D1-Class", "D1-Flowchart",
            "D1-Graph", "D1-Packet", "D1-Sequence", "D1-State",
            "D2-Block", "D2-Class", 
            "D2-Graph", "D2-Packet", "D2-Sequence", "D2-State",
        ]
        datasets = {
            cfg: load_dataset("Exploration-Lab/TechING", cfg, token=os.environ['HF_TOKEN'],split='train')
            for cfg in configs
            }
        datasets['D2-Block'] = datasets['D2-Block'].rename_column('Original', 'Image')
        datasets['D2-Class'] = datasets['D2-Class'].rename_column('Original', 'Image')
        datasets['D2-Graph'] = datasets['D2-Graph'].rename_column('Original', 'Image')
        datasets['D2-Packet'] = datasets['D2-Packet'].rename_column('Original', 'Image')
        datasets['D2-Sequence'] = datasets['D2-Sequence'].rename_column('Original', 'Image')
        datasets['D2-State'] = datasets['D2-State'].rename_column('Original', 'Image')
        datasets = concatenate_datasets(datasets.values())
        
        
    elif not train and data == 'D1':
        configs = [
            "D1-Block", "D1-C4", "D1-Class", "D1-Flowchart",
            "D1-Graph", "D1-Packet", "D1-Sequence", "D1-State",
        ]
        datasets = {
            cfg: load_dataset("Exploration-Lab/TechING", cfg, token=os.environ['HF_TOKEN'] ,split='test')
            for cfg in configs
            }
        # datasets = concatenate_datasets(datasets.values())
        
    elif not train and data == 'D3':
        configs = [
            "D3-Block", "D3-C4", "D3-Class", "D3-Flowchart",
            "D3-Graph", "D3-Packet", "D3-Sequence", "D3-State",
        ]
        datasets = {
            cfg: load_dataset("Exploration-Lab/TechING", cfg, token=os.environ['HF_TOKEN'] ,split='train')
            for cfg in configs
            }
        
    else:
        raise ValueError("if train is True, data should be D1+D2 else wither of D1 or D3 for test set.")
    return datasets
def collate_fn(data):
    imgs= []
    mermaid_code = []
    for item in data:
        if type(item['Prompt']) == type('string'):
            ## FOR NEW TASKS
            ## Incomplete Image + Improvement Prompt to Improved Code
            random_no = random.random()
            if random_no <= 0.125:
                imgs.append([augment_pil_image(item['Perturbed'].convert('RGB'), transform)])
                messages = [
                    {"role": "user", "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{random.choice(incomplete_image_prompt_to_code)}\n\nImprovement Prompt:\n{item['Prompt']}\n"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Incomplete Image + Topological Description to Improved Code
            elif random_no>=0.125 and random_no<=0.25:
                imgs.append([augment_pil_image(item['Perturbed'].convert('RGB'), transform)])
                messages = [
                    {"role": "user", "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{random.choice(incomplete_image_plus_description_to_code)}\n\nComplete Topological Description:\n{item['Description']}\n"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Incomplete Code + Improvement Prompt to Improved Code
            elif random_no>=0.25 and random_no<=0.375:
                messages = [
                    {"role": "user", "content": [
                        {"type": "text", "text": f"{random.choice(perturbed_code_plus_prompt_to_code)}\n\nIncomplete Code:\n{item['Perturbed Code']}\n\nImprovement Prompt:\n{item['Prompt']}\n"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                imgs=None
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Incomplete Code + Topological Description to Improved Code
            elif random_no>=0.375 and random_no<=0.5:
                messages = [
                    {"role": "user", "content": [
                        {"type": "text", "text": f"{random.choice(perturbed_code_plus_description_to_code)}\n\nIncomplete Code:\n{item['Perturbed Code']}\n\nComplete Topological Description:\n{item['Description']}\n"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                imgs=None
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Incomplete Image + Incomplete Code + Improvement Prompt to Improved Code
            elif random_no>=0.5 and random_no<=0.625:
                imgs.append([augment_pil_image(item['Perturbed'].convert('RGB'), transform)])
                messages = [
                    {"role": "user", "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{random.choice(perturbed_image_code_plus_improvement_to_code)}\n\nIncomplete Code:\n{item['Perturbed Code']}\n\nImprovement Prompt:\n{item['Prompt']}\n"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Incomplete Image + Incomplete Code + Topological Description to Improved Code
            elif random_no>=0.625 and random_no<=0.75:
                imgs.append([augment_pil_image(item['Perturbed'].convert('RGB'), transform)])
                messages = [
                    {"role": "user", "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{random.choice(perturbed_image_code_plus_improvement_to_code)}\n\nIncomplete Code:\n{item['Perturbed Code']}\n\nComplete Topological Description:\n{item['Description']}\n"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Q/A Image relates to provided Code or not
            elif random_no>=0.75 and random_no<=0.875:
                ## YES pair
                new_rand = random.random()
                ## YES pair Correct Image and Code pair
                if new_rand<=0.25:
                    imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                    messages = [
                        {"role": "user", "content": [
                            {"type": "image"},
                            {"type": "text", "text": f"{random.choice(image_code_relation_prompts)}\n\nCode:\n{item['Mermaid Code']}"},
                        ]},
                        {"role": "assistant", "content": [
                            {"type": "text", "text": f"```response\n{random.choice(yes_image_code_responses)}\n```"}
                        ]}
                    ]
                    mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
                ## No pair 
                elif new_rand>=0.25 and new_rand<=0.5:
                    imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                    code_index = random.randint(0, len(dataset))
                    # while code_index == item['index']:
                    #     code_index = random.randint(0, len(dataset))
                    messages = [
                        {"role": "user", "content": [
                            {"type": "image"},
                            {"type": "text", "text": f"{random.choice(image_code_relation_prompts)}\n\nCode:\n{dataset[code_index]['Mermaid Code']}"},
                        ]},
                        {"role": "assistant", "content": [
                            {"type": "text", "text": f"```response\n{random.choice(no_image_code_responses)}\n```"}
                        ]}
                    ]
                    mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
                ## Partial Complete Image + Perturbed Code
                elif new_rand >=0.5 and new_rand<=0.75:
                    imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                    messages = [
                        {"role": "user", "content": [
                            {"type": "image"},
                            {"type": "text", "text": f"{random.choice(image_code_relation_prompts)}\n\nCode:\n{item['Perturbed Code']}"},
                        ]},
                        {"role": "assistant", "content": [
                            {"type": "text", "text": f"```response\n{random.choice(more_image_code_info_responses)}\n```"}
                        ]}
                    ]
                    mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
                ## Partial Incomplete Image + Complete Code
                else:
                    imgs.append([augment_pil_image(item['Perturbed'].convert('RGB'), transform)])
                    messages = [
                        {"role": "user", "content": [
                            {"type": "image"},
                            {"type": "text", "text": f"{random.choice(image_code_relation_prompts)}\n\nCode:\n{item['Mermaid Code']}"},
                        ]},
                        {"role": "assistant", "content": [
                            {"type": "text", "text": f"```response\n{random.choice(more_code_image_info_responses)}\n```"}
                        ]}
                    ]
                    mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Q/A Image relation to Description
            else:
                ## YES pair
                new_rand = random.random()
                ## YES pair Correct Image and Description pair
                if new_rand<=0.5:
                    imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                    messages = [
                        {"role": "user", "content": [
                            {"type": "image"},
                            {"type": "text", "text": f"{random.choice(image_code_relation_prompts)}\n\nTopological Description:\n{item['Description']}"},
                        ]},
                        {"role": "assistant", "content": [
                            {"type": "text", "text": f"```response\n{random.choice(yes_responses_image_description)}\n```"}
                        ]}
                    ]
                    mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
                ## No pair 
                else:
                    imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                    desc_index = random.randint(0, len(dataset))
                    # while desc_index == item['index']:
                    #     desc_index = random.randint(0, len(dataset))
                    messages = [
                        {"role": "user", "content": [
                            {"type": "image"},
                            {"type": "text", "text": f"{random.choice(image_code_relation_prompts)}\n\nTopological Description:\n{dataset[desc_index]['Description']}"},
                        ]},
                        {"role": "assistant", "content": [
                            {"type": "text", "text": f"```response\n{random.choice(no_responses_image_description)}\n```"}
                        ]}
                    ]
                    mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            
            
        else:
            ## Image to Code
            random_no = random.random()
            if random_no <= 0.2:
                imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                messages = [
                    {"role": "user", "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{random.choice(image_to_code)}"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Description to Code
            elif random_no >= 0.2 and random_no <= 0.4:
                messages = [
                    {"role": "user", "content": [
                        {"type": "text", "text": f"{random.choice(description_to_code)}\n\nSummary: {item['Description']}"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```"}
                    ]}
                ]
                imgs=None
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Image to Description
            elif random_no >=0.4 and random_no <= 0.6:
                messages = [
                    {"role": "user", "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{random.choice(image_to_summary)}"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```Summary:\n{item['Description']}\n```"}
                    ]}
                ]
                imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Code to Description
            elif random_no>=0.6 and random_no<=0.8:
                messages = [
                    {"role": "user", "content": [
                        {"type": "text", "text": f"{random.choice(code_to_descriptions)}\n\nCode: {item['Mermaid Code']}"},
                    ]},
                    {"role": "assistant", "content": [
                        {"type": "text", "text": f"```Summary:\n{item['Description']}\n```"}
                    ]}
                ]
                imgs=None
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')
            ## Image to Code + Summary
            else:
                messages = [
                    {"role": "user", "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{random.choice(image_to_code_and_description_prompts)}"},
                    ]},
                    
                ]
                if random.random()<=0.5:
                    messages.append({"role": "assistant", "content": [
                        {"type": "text", "text": f"```mermaid\n{item['Mermaid Code']}\n```\n\n```Summary:\n{item['Description']}\n```\n"}
                    ]})
                else:
                    messages.append({"role": "assistant", "content": [
                        {"type": "text", "text": f"```Summary:\n{item['Description']}\n```\n\n```mermaid\n{item['Mermaid Code']}\n```\n"}
                    ]})
                    
                imgs.append([augment_pil_image(item['Image'].convert('RGB'), transform)])
                mermaid_code.append(processor.apply_chat_template(messages)+'<|end_of_text|>')

        
    updated = processor(
        imgs,
        mermaid_code,
        return_tensors='pt',
        padding=True
    )
    # print(processor.batch_decode(updated['input_ids']))
    updated.update({'labels':updated['input_ids']})
    updated.update({'ignore_index':128256})
    return updated


dataset = get_dataset(train=True, data='D1+D2')