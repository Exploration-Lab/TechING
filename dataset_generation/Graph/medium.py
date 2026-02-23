import random
import os
import pydot
import pandas as pd

# Predefined Nodes and Edges
FIELDS = {
    "Technology": ["Client", "Server", "Node", "Router", "Switch", "Firewall"],
    "Business": ["Customer", "Vendor", "Supplier", "Bank", "Investor", "Manager"],
    "Healthcare": ["Doctor", "Nurse", "Patient", "Pharmacist", "Lab Technician", "Insurance Provider"],
    "E-commerce": ["Buyer", "Seller", "Warehouse", "Courier", "Payment Gateway", "Support Agent"],
    "Legal": ["Lawyer", "Judge", "Citizen", "Police", "Government Agency"],
    "AI": ["Model", "Dataset", "API", "Inference Engine", "Data Pipeline"]
}

EDGES = {
    "Technology": ["Request", "Response", "ACK", "SYN", "HTTP GET", "DNS Query"],
    "Business": ["Invoice", "Payment Confirmation", "Order Request", "Loan Approval", "Tax Report"],
    "Healthcare": ["Diagnosis Report", "Prescription", "Test Results", "Insurance Claim", "Discharge Summary"],
    "E-commerce": ["Order Confirmation", "Shipping Notification", "Payment Received", "Refund Processed"],
    "Legal": ["Legal Notice", "Court Summons", "Complaint Report", "Tax Filing", "Passport Approval"],
    "AI": ["Training Request", "Model Weights", "Prediction Output", "API Response"]
}

# Initialize structured dataframe (IMPORTANT)
df_structured = pd.DataFrame(columns=["Image Path", "Mermaid Code", "Topological Summary"])


def generate_graph_nodes(min_nodes=4, max_nodes=5):
    category = random.choice(list(FIELDS.keys()))
    available_nodes = FIELDS[category]

    num_nodes = random.randint(
        min(min_nodes, len(available_nodes)),
        min(max_nodes, len(available_nodes))
    )

    nodes = random.sample(available_nodes, num_nodes)
    return nodes, category


def generate_graph_edges(nodes, category, min_edges=3, max_edges=4):
    if len(nodes) < 2:
        return []

    max_possible_edges = len(nodes) * (len(nodes) - 1)
    num_edges = random.randint(
        min(min_edges, max_edges),
        min(max_edges, max_possible_edges)
    )

    edges = set()
    edge_labels = EDGES[category]

    while len(edges) < num_edges:
        source, target = random.sample(nodes, 2)
        label = random.choice(edge_labels)
        edges.add((source, target, label))

    return list(edges)


def save_graph_image(edges, output_folder, file_name):
    os.makedirs(output_folder, exist_ok=True)
    graph = pydot.Dot(graph_type="digraph")

    for source, target, label in edges:
        graph.add_edge(pydot.Edge(source, target, label=label))

    output_path = os.path.join(output_folder, f"{file_name}.png")
    graph.write_png(output_path)
    return output_path


def generate_mermaid_code(nodes, edges):
    mermaid_lines = ["graph TD"]

    for node in nodes:
        node_id = node.replace(" ", "_")
        mermaid_lines.append(f'{node_id}["{node}"]')

    for source, target, label in edges:
        source_id = source.replace(" ", "_")
        target_id = target.replace(" ", "_")
        mermaid_lines.append(f'{source_id} -->|"{label}"| {target_id}')

    return "\n".join(mermaid_lines)


def get_blocks_and_edges(mermaid_code):
    triplets = []
    nodes = set()

    for line in mermaid_code.split("\n")[1:]:
        if "-->" in line:
            parts = line.split("-->")
            head = parts[0].strip()
            rest = parts[1].strip()

            if "|" in rest:
                label = rest.split("|")[1].replace('"', '')
                tail = rest.split("|")[-1].strip()
            else:
                label = ""
                tail = rest.strip()

            nodes.add(head)
            nodes.add(tail)
            triplets.append((head, label, tail))

    return triplets, list(nodes)


def get_topological_summary(triplets, nodes):
    summary = f"""The topological summary of the diagram is as follows:

There are {len(nodes)} nodes in the diagram:

The name of the nodes are as follows:
"""
    for i, node in enumerate(nodes, 1):
        summary += f"{i}. '{node}'\n"

    summary += "\nThe edges between the nodes are as follows:\n"
    for i, (src, label, tgt) in enumerate(triplets, 1):
        if label == "":
            summary += f"{i}. '{src}' is connected to '{tgt}'.\n"
        else:
            summary += f"{i}. '{src}' is connected to '{tgt}' with edge label '{label}'.\n"

    return summary


def save_mermaid_file(mermaid_code, output_folder, file_name):
    os.makedirs(output_folder, exist_ok=True)
    path = os.path.join(output_folder, f"{file_name}.mmd")
    with open(path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)
    return path


# 🔥 MAIN DATASET GENERATION FUNCTION (Like your previous scripts)
def generate_graph_dataset(num_samples=100,
                           image_folder="graph_images",
                           mermaid_folder="mermaid_files",
                           csv_path="graph_dataset.csv"):

    global df_structured

    for i in range(1, num_samples + 1):
        nodes, category = generate_graph_nodes()
        edges = generate_graph_edges(nodes, category)

        file_name = f"graph_{i}"

        # Generate Mermaid + Summary
        mermaid_code = generate_mermaid_code(nodes, edges)
        triplets, parsed_nodes = get_blocks_and_edges(mermaid_code)
        topological_summary = get_topological_summary(triplets, parsed_nodes)

        # Save files
        image_path = save_graph_image(edges, image_folder, file_name)
        save_mermaid_file(mermaid_code, mermaid_folder, file_name)

        # Append to dataframe (like your packet/sequence code)
        df_structured = pd.concat([
            df_structured,
            pd.DataFrame([{
                "Mermaid Code": mermaid_code,
                "Topological Summary": topological_summary
            }])
        ], ignore_index=True)

        print(f"Generated {file_name}")

    # Save dataset CSV (VERY IMPORTANT for training)
    df_structured.to_csv(csv_path, index=False)
    print(f"\nDataset saved at: {csv_path}")


# Run generation
if __name__ == "__main__":
    generate_graph_dataset(num_samples=10)