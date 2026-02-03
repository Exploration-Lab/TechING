from datasets import load_dataset

def load_teching_dataset(dataset_name="D1", diag_type="Block", split="train"):
    """Load the TechING dataset from Hugging Face."""
    if split=="train" or split=="test":
        print(f"Loading TechING dataset for split: {split}...")
        ds = load_dataset("Exploration-Lab/TechING", name=f"{dataset_name}-{diag_type}", split=split)
        print(f"Loaded {len(ds)} samples for {split} split.")
    elif split=="all":
        print(f"Loading TechING dataset for all splits...")
        ds = load_dataset("Exploration-Lab/TechING", name=f"{dataset_name}-{diag_type}")
        print(f"Loaded {len(ds)} samples for all splits.")
    else:
        raise ValueError("Invalid split name. Choose from 'train', 'test', or 'all'.")
    return ds
