import random
import os
import subprocess
from PIL import Image
from IPython.display import display
import pandas as pd
import re

# Field-based names for actors/participants
FIELDS = {
    "Technology": ["Client", "Server", "Node", "Router", "Switch", "Firewall"],
    "Business": ["Customer", "Vendor", "Supplier", "Bank", "Investor", "Manager"],
    "Healthcare": ["Doctor", "Nurse", "Patient", "Pharmacist", "Lab Technician", "Insurance Provider"],
    "E-commerce": ["Buyer", "Seller", "Warehouse", "Courier", "Payment Gateway", "Support Agent"],
    "Legal": ["Lawyer", "Judge", "Citizen", "Police", "Government Agency"],
    "AI": ["Model", "Dataset", "API", "Inference Engine", "Data Pipeline"]
}

# Field-based message names
MESSAGES = {
    "Technology": ["Request", "Response", "ACK", "SYN", "HTTP GET", "DNS Query"],
    "Business": ["Invoice", "Payment Confirmation", "Order Request", "Loan Approval", "Tax Report"],
    "Healthcare": ["Diagnosis Report", "Prescription", "Test Results", "Insurance Claim", "Discharge Summary"],
    "E-commerce": ["Order Confirmation", "Shipping Notification", "Payment Received", "Refund Processed"],
    "Legal": ["Legal Notice", "Court Summons", "Complaint Report", "Tax Filing", "Passport Approval"],
    "AI": ["Training Request", "Model Weights", "Prediction Output", "API Response"]
}

# 1. Generate Actors and Participants
def generate_sequence_components(min_actors=2, max_actors=2, min_participants=2, max_participants=2):
    actor_field = random.choice(list(FIELDS.keys()))
    participant_field = random.choice(list(FIELDS.keys()))

    actors = random.sample(
        FIELDS[actor_field],
        min(random.randint(min_actors, max_actors), len(FIELDS[actor_field]))
    )

    participants = random.sample(
        FIELDS[participant_field],
        min(random.randint(min_participants, max_participants), len(FIELDS[participant_field]))
    )

    return actors, participants


# 2. Generate Interactions
def generate_interactions(actors, participants, min_interactions=3, max_interactions=4):
    components = actors + participants
    interactions = []
    message_field = random.choice(list(MESSAGES.keys()))

    for _ in range(random.randint(min_interactions, max_interactions)):
        sender = random.choice(components)
        receiver = random.choice(components)

        while sender == receiver:
            receiver = random.choice(components)

        message_type = random.choice(["->>", "-->>"])
        message = random.choice(MESSAGES[message_field])

        interactions.append((sender, message_type, receiver, message))

    return interactions


# 3. Generate Mermaid Code
def generate_mermaid_sequence_code(actors, participants, interactions):
    mermaid_code = ["sequenceDiagram"]

    for actor in actors:
        mermaid_code.append(f"actor {actor}")

    for participant in participants:
        mermaid_code.append(f"participant {participant}")

    for sender, message_type, receiver, message in interactions:
        mermaid_code.append(f"{sender} {message_type} {receiver}: {message}")

    return "\n".join(mermaid_code)


# 4. Save Mermaid Code
def save_mermaid_code(mermaid_code, folder_name, file_name):
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, f"{file_name}.mmd")

    with open(file_path, "w") as f:
        f.write(mermaid_code)

    return file_path


# 5. Generate PNG from Mermaid Code
def generate_mermaid_png(folder_name, file_name, scale=2):
    mmd_file = os.path.join(folder_name, f"{file_name}.mmd")
    png_file = os.path.join(folder_name, f"{file_name}.png")

    try:
        subprocess.run(
            ["mmdc", "-i", mmd_file, "-o", png_file, "-s", str(scale)],
            check=True
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "Mermaid CLI (mmdc) not found. Please install it using:\n"
            "npm install -g @mermaid-js/mermaid-cli"
        )
    except subprocess.CalledProcessError as e:
        print(f"Error generating PNG: {e}")

    return png_file


# 6. Generate Unique File Name
def generate_unique_file_name(folder_name, base_name, index):
    return f"{base_name}{index}"

def get_blocks_and_edges(mermaid_code):
    lines = mermaid_code.strip().split("\n")
    actors = []
    participants = []
    interactions = []
    
    for line in lines:
        line = line.strip()
        
        # Parse actors
        if line.startswith("actor"):
            actor = line.split("actor")[1].strip()
            if actor not in actors:
                actors.append(actor)
        
        # Parse participants
        elif line.startswith("participant"):
            participant = line.split("participant")[1].strip()
            if participant not in participants:
                participants.append(participant)
        
        # Parse interactions (multi-word entities, including duplicate interactions)
        elif re.search(r"([\w\s]+)\s*(->>|-->>)\s*([\w\s]+):\s*(.+)", line):
            match = re.findall(r"([\w\s]+)\s*(->>|-->>)\s*([\w\s]+):\s*(.+)", line)
            for from_actor, arrow_type, to_actor, message in match:
                if from_actor.strip() not in actors and from_actor.strip() not in participants:
                    participants.append(from_actor)
                if to_actor.strip() not in actors and to_actor.strip() not in participants:
                    participants.append(to_actor)
                interaction_type = "synchronous" if arrow_type == "->>" else "asynchronous"
                interactions.append({
                    "from": from_actor.strip(),
                    "to": to_actor.strip(),
                    "message": message.strip(),
                    "type": interaction_type
                })

    summary = {
        "actors": actors,
        "participants": participants,
        "interactions": interactions
    }
    
    return summary


def get_topological_summary(summary):    
    topological_summary = f"""The topological summary of the diagram is as follows:

There are {len(summary['actors'])} actors and {len(summary['participants'])} participants in the diagram:
"""
    counter = 1
    if len(summary['actors']) > 0:
        topological_summary += "\nThe name of the actors are as follows:\n"
        for block in summary['actors']:
            topological_summary += f"{counter}. '{block}'\n"
            counter += 1

    counter = 1
    topological_summary += "\nThe name of the participants are as follows:\n"
    for block in summary['participants']:
        topological_summary += f"{counter}. '{block}'\n"
        counter += 1

    topological_summary += "\nThe interactions between the entities are as follows:\n"
    counter = 1
    for rel in summary['interactions']:
        if rel['type'] == 'synchronous':
            topological_summary += f"{counter}. '{rel['from']}' sends a synchronous message '{rel['message']}' to '{rel['to']}'.\n"
        elif rel['type'] == 'asynchronous':
            topological_summary += f"{counter}. '{rel['from']}' sends an asynchronous message '{rel['message']}' to '{rel['to']}'.\n"
        counter += 1
    return topological_summary

df_structured = pd.DataFrame(columns=['Mermaid Code', 'Topological Summary'])   
# 7. Generate 1000 Images
def generate_10_images(output_folder, base_name="diagram", df_structured=None):
    # Initialize dataframe if not provided
    if df_structured is None:
        df_structured = pd.DataFrame(columns=['Mermaid Code', 'Topological Summary'])

    os.makedirs(output_folder, exist_ok=True)

    for i in range(1, 10):
        actors, participants = generate_sequence_components()
        interactions = generate_interactions(actors, participants)

        mermaid_code = generate_mermaid_sequence_code(actors, participants, interactions)
        summary = get_blocks_and_edges(mermaid_code)
        topological_summary = get_topological_summary(summary)

        file_name = generate_unique_file_name(output_folder, base_name, i)

        # Save files
        save_mermaid_code(mermaid_code, output_folder, file_name)
        generate_mermaid_png(output_folder, file_name)

        # ✅ Append to dataframe (SAME logic as your packet script)
        new_row = pd.DataFrame([{
            'Mermaid Code': mermaid_code,
            'Topological Summary': topological_summary
        }])

        df_structured = pd.concat([df_structured, new_row], ignore_index=True)

        print(f"Generated {i}/10 diagrams")

    return df_structured


# Run the generation process
if __name__ == "__main__":
    df_structured = pd.DataFrame(columns=['Mermaid Code', 'Topological Summary'])

    df_structured = generate_10_images(
        output_folder="output_diagrams",
        base_name="diagram",
        df_structured=df_structured
    )

    # Save dataset (VERY useful for your VLM thesis)
    df_structured.to_csv("sequence_diagram_dataset.csv", index=False)

    print("✅ Dataset saved as sequence_diagram_dataset.csv")