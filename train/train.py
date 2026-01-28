from utils.seed import set_all_seeds
import os
from transformers import Trainer, TrainingArguments
from transformers import TrainingArguments, Trainer
from utils.parser import parse_args
from model.llama import get_model
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("HF_TOKEN")




def main(args=None):
    model = get_model(args)
    os.environ['HF_TOKEN']=args.hf_token
    from data.dataset import dataset, collate_fn
    print(dataset)

    training_args = TrainingArguments(
        output_dir= args.output_dir,
        do_train=args.do_train,
        do_eval=args.do_eval,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        weight_decay = args.weight_decay,
        num_train_epochs=args.num_train_epochs,
        lr_scheduler_type=args.lr_scheduler_type,
        warmup_ratio=args.warmup_ratio,
        bf16=args.bf16,
        save_strategy=args.save_strategy,
        save_steps=args.save_steps,
        logging_steps=args.logging_steps,
        dataloader_num_workers=args.dataloader_num_workers,
        torch_compile=False,
        remove_unused_columns=False,
        ddp_find_unused_parameters=True,
        report_to=args.report_to,
        run_name=args.run_name,
        seed=args.seed,
        ddp_backend=args.ddp_backend,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator = collate_fn,
        train_dataset=dataset, 
    )


    trainer.train()

if __name__ == "__main__":

    args = parse_args()
    set_all_seeds(args.seed)
    args.hf_token = token
    main(args)
