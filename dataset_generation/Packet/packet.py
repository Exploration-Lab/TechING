import random
import subprocess
import os
import pandas as pd
import re

# Directory to save generated diagrams and images
OUTPUT_DIR = "generated_packets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of possible packet fields
PACKET_FIELDS = [
    "Source Port", "Destination Port", "Sequence Number", "Acknowledgment Number",
    "Data Offset", "Reserved", "Flags (URG, ACK, PSH, RST, SYN, FIN)",
    "Window Size", "Checksum", "Urgent Pointer", "(Options and Padding)", "Data (Variable Length)"
]

# Function to generate a random packet structure
def generate_packet_diagram():
    num_fields = random.randint(5, 10)  # Choose 5-10 fields
    selected_fields = ["Source Port", "Destination Port"]  # Ensure these exist

    # Randomly pick remaining fields (allow some repetition)
    for _ in range(num_fields - len(selected_fields)):
        selected_fields.append(random.choice(PACKET_FIELDS))  
    
    byte_offset = 0  # Start position
    mermaid_code = "---\ntitle: \"Random Packet Diagram\"\n---\npacket-beta\n"
    
    for field in selected_fields:
        field_size = random.randint(8, 32)  # Random field size
        mermaid_code += f"{byte_offset}-{byte_offset + field_size - 1}: \"{field}\"\n"
        byte_offset += field_size

    return mermaid_code

def get_blocks_and_edges(mermaid_code):
    lines = mermaid_code.strip().split("\n")
    summary = {
        "title": "",
        "segments": []
    }

    for line in lines:
        line = line.strip()
        
        # Extract title if present
        title_match = re.match(r'---\s*title:\s*"(.*?)"\s*---', line)
        if title_match:
            summary["title"] = title_match.group(1)
            continue

        # Extract packet segments (bit range and label)
        segment_match = re.match(r'(\d+)-(\d+):\s*"(.*?)"', line)
        if segment_match:
            start_bit = int(segment_match.group(1))
            end_bit = int(segment_match.group(2))
            label = segment_match.group(3)
            
            summary["segments"].append({
                "start_bit": start_bit,
                "end_bit": end_bit,
                "label": label
            })

    return summary


def get_topological_summary(summary):    
    topological_summary = f"""The topological summary of the diagram is as follows:

There are {len(summary['segments'])} headers in the packet diagram:
"""
    counter = 1
    topological_summary += "\nThe name of the header along with the bit information are as follows:\n"
    for block in summary['segments']:
        topological_summary += f"{counter}. '{block['label']}' header is occuying {block['end_bit']-block['start_bit']} bits from {block['start_bit']} to {block['end_bit']}.\n"
        counter += 1
    return topological_summary

# Function to save the diagram and generate an image

df_structured = pd.DataFrame(columns=["Mermaid Code", "Topological Summary"])

def save_and_generate_image(index,df_structured):
    mermaid_code = generate_packet_diagram()
    summary = get_blocks_and_edges(mermaid_code)
    topological_summary = get_topological_summary(summary)
    
    # Define file paths
    mmd_file = os.path.join(OUTPUT_DIR, f"packet_diagram_{index}.mmd")
    png_file = os.path.join(OUTPUT_DIR, f"packet_diagram_{index}.png")

    # Save the Mermaid code
    with open(mmd_file, "w") as f:
        f.write(mermaid_code)
    
    # Convert Mermaid to PNG using mmdc
    try:
        subprocess.run(["mmdc", "-i", mmd_file, "-o", png_file], check=True)
        print(f"✅ Saved: {mmd_file}")
        print(f"🖼️ Image generated: {png_file}")
    except Exception as e:
        print("❌ Error generating image:", e)
    new_row = pd.DataFrame([{
        'Mermaid Code': mermaid_code,
        'Topological Summary': topological_summary
    }])
    
    df_structured = pd.concat([df_structured, new_row], ignore_index=True)
    
    return df_structured
    
# Generate and save multiple packet diagrams
num_diagrams = 10  # Number of diagrams to generate
for i in range(1, num_diagrams + 1):
    df_structured = save_and_generate_image(i, df_structured)
    

print(f"📂 All {num_diagrams} packet diagrams and images saved in {OUTPUT_DIR}")

df_structured.to_csv("testing.csv", index=False)
