from transformers import MllamaForConditionalGeneration
from peft import LoraConfig, get_peft_model, PeftModel
import torch

def get_model(args):
    model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
    model = MllamaForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
    )

    lora_config = LoraConfig(
        r=args.lora_rank,
        lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "k_proj", "v_proj"],
        lora_dropout=args.lora_dropout,
        use_rslora=args.use_rslora,
    )
    if args.model_path is not None:
        model = PeftModel.from_pretrained(model, args.model_path, is_trainable=True)
        model.train()
    else:
        model = get_peft_model(model, lora_config, 'default')
        model.print_trainable_parameters()
    return model