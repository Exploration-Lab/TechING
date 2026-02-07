import random
import subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, deque
import pandas as pd
from IPython.display import Image, display
import re
import os
import json
from tqdm import tqdm

# Create a matrix of size n x n and fill it with 'space'
def matrix(n):
    position_matrix = [['space' for i in range(n)] for j in range(n)]
    return position_matrix

# function to check if the position is safe to put a block
def is_position_safe(matrix, row, col):
    """Check if placing a value at matrix[row][col] is safe."""
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 0),  (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(matrix) and 0 <= c < len(matrix) and matrix[r][c] != 'space':
            return False
    return True

# Block Categories and their respective names
engineering_disciplines = ['Civil', 'Mechanical', 'Electrical', 'Chemical', 'Computer', 'Aerospace', 'Biomedical', 'Industrial', 'Environmental', 'Materials', 'Nuclear', 'Software', 'Petroleum', 'Marine']
business_disciplines = ['Accounting', 'Finance', 'Marketing', 'Management', 'Human Resources', 'Entrepreneurship', 'Supply Chain', 'Economics', 'International Business', 'Operations Management', 'Business Analytics', 'Information Systems', 'Real Estate', 'Hospitality Management']
science_disciplines = ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Geology', 'Astronomy', 'Meteorology', 'Oceanography', 'Botany', 'Zoology', 'Ecology', 'Genetics', 'Microbiology', 'Biochemistry']
arts_disciplines = ['Music', 'Dance', 'Theatre', 'Fine Arts', 'Photography', 'Film', 'Fashion', 'Graphic Design', 'Interior Design', 'Architecture']
banking_disciplines = ['Investment Banking', 'Retail Banking', 'Corporate Banking', 'Private Banking', 'Asset Management', 'Hedge Funds', 'Private Equity', 'Venture Capital']
healthcare_disciplines = ['Nursing', 'Pharmacy', 'Dentistry', 'Medicine', 'Physical Therapy', 'Occupational Therapy', 'Speech Therapy', 'Radiology', 'Pathology', 'Anesthesiology', 'Cardiology', 'Dermatology', 'Endocrinology', 'Gastroenterology']
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus']
countries = ['USA', 'China', 'India', 'Japan', 'Germany', 'UK', 'France', 'Brazil', 'Italy', 'Canada', 'South Korea', 'Russia', 'Australia', 'Spain']
networks = ['Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'Snapchat', 'Pinterest', 'Reddit', 'TikTok', 'YouTube', 'WhatsApp', 'Skype', 'Zoom', 'Slack', 'Twitch']
sports = ['Football', 'Basketball', 'Baseball', 'Soccer', 'Tennis', 'Golf', 'Hockey', 'Rugby', 'Cricket', 'Volleyball', 'Boxing', 'MMA', 'Wrestling', 'Track and Field']
food = ['Pizza', 'Burger', 'Taco', 'Sushi', 'Pasta', 'Steak', 'Salad', 'Soup', 'Dessert', 'Breakfast', 'Seafood', 'Vegetarian', 'Vegan']
movies = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'SciFi', 'Thriller', 'Documentary', 'Animation', 'Musical', 'Adventure', 'Fantasy', 'Mystery', 'Crime']

# Pick block names and return a list
def block_names(noBlocks):
    blocks = [
        engineering_disciplines, business_disciplines, science_disciplines, arts_disciplines, banking_disciplines, healthcare_disciplines,
        cities, countries, networks, sports, food, movies
    ]
    blockNames = []
    # Pick a single random block category and names of blocks from that category
    category = random.choice(blocks)
    blockNames = random.sample(category, noBlocks)
    return blockNames

# Placing blocks in matrix position
def place_blocks(matrix, blockNames):
    positions = [(0,0), (0,2), (2,0), (2,2)]

    for block in blockNames:
        strippedBlock = block.replace(" ", "").replace("-", "")

        while positions:  # avoid infinite loop
            i, j = random.choice(positions)

            if matrix[i][j] == 'space':
                matrix[i][j] = f'{strippedBlock}["{block}"]:1'
                positions.remove((i, j))  # don't reuse position
                break
            else:
                positions.remove((i, j))  # remove tried position

    return matrix

# connect blocks randomly
def connect_blocks_randomly(matrix, noEdges):
    coordinates = [(x, y) for x in range(len(matrix)) for y in range(len(matrix)) if matrix[x][y] != 'space']
    connections = []
    for _ in range(noEdges):
        while True:
            # Pick two random blocks
            block1coord, block2coord = random.sample(coordinates, 2)
            # print(block1coord, block2coord)
            # Code to make sure that if we connect those two blocks the edge doesn't intersect with any other block
            x, y = block1coord
            s, t = block2coord
            del_x = x - s
            del_y = y - t
            max_del = max(del_x, del_y)
            startx, stopx, n = 0, del_x, max_del
            starty, stopy, n = 0, del_y, max_del
            stepsx = [startx + (i+1) * (stopx - startx) / (n) for i in range(n-1)]
            stepsy = [starty + (i+1) * (stopy - starty) / (n) for i in range(n-1)]
            # print(stepsx)
            # print(stepsy)
            for e, f in zip(stepsx, stepsy):
                p, q = int(s+e), int(t+f)
                if matrix[p][q] != 'space':
                    break
            block1 = matrix[x][y].split('[')[0]
            block2 = matrix[s][t].split('[')[0]
            # If the edge doesn't already exist, add it to the connections list
            if f"{block1} --> {block2}" not in connections:
                break
        # Add the edge to the connections list
        connections.append(f"{block1} --> {block2}")
    return connections

# Update the dataset with new rows
def update_dataset(df, image_path, mermaid_code, topological_summary):
    new_row = {
        "Image": [image_path],
        "Mermaid Code": [mermaid_code],
        "Description": [topological_summary]  # Placeholder for description
    }
    new_row = pd.DataFrame(new_row)

    # Append the new row using concat
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Develop the mermaid code, save it to test file and generate it's mermaid image
def write_mermaid_code(position_matrix, connections, columns):
    # Mermaid syntax as a string
    # Case 1: all left
    if position_matrix[0][0] != 'space' and position_matrix[2][0] != 'space':
        mermaid_code = f"""block-beta
columns 1
"""
        mermaid_code += f"    {position_matrix[0][0]}\n"
        mermaid_code += f"    {position_matrix[1][0]}\n"
        mermaid_code += f"    {position_matrix[2][0]}\n\n"   

    # Case 2: all right
    elif position_matrix[2][0] != 'space' and position_matrix[2][2] != 'space':
        mermaid_code = f"""block-beta
columns 1
"""
        mermaid_code += f"    {position_matrix[2][0]}\n"
        mermaid_code += f"    {position_matrix[2][1]}\n"
        mermaid_code += f"    {position_matrix[2][2]}\n\n"   

    # Case 3: All top
    elif position_matrix[0][0] != 'space' and position_matrix[0][2] != 'space':
        mermaid_code = f"""block-beta
columns 3
"""
        mermaid_code += f"    {position_matrix[0][0]} {position_matrix[0][1]} {position_matrix[0][2]}\n\n"

    # Case 4: All bottom
    elif position_matrix[2][0] != 'space' and position_matrix[2][2] != 'space':
        mermaid_code = f"""block-beta
columns 3
"""
        mermaid_code += f"    {position_matrix[2][0]} {position_matrix[2][1]} {position_matrix[2][2]}\n\n"
    
    # Case 5: Mixed
    else:
        mermaid_code = f"""block-beta
columns 3
"""
        for row in range(len(position_matrix)):
            mermaid_code += "    "
            for col in range(len(position_matrix)):
                mermaid_code += f"{position_matrix[row][col]} "
            mermaid_code += "\n"
        mermaid_code += "\n"

    # Adding connections to the mermaid code
    for connection in connections:
        mermaid_code += f"    {connection}\n"
    
    # Saving the code to a temporary test file
    file_name = f"./test.mmd"
    with open(file_name, "w") as file:
        file.write(mermaid_code)
    image_file_name = f"./test.png"
    command = f"mmdc -i {file_name} -o {image_file_name} -s 2"
        # Running the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    return mermaid_code


def save_image_and_code(mermaid_code, counter):
    # File name to save as .mmd
    os.makedirs("MermaidImageEasy", exist_ok=True)
    os.makedirs("MermaidCodeEasy", exist_ok=True)
    # File name to save as .mmd
    code_file_name = f"./MermaidCodeEasy/BlockDiagram{counter}.mmd"
    image_file_name = f"./MermaidImageEasy/BlockDiagram{counter}.png"
    # Saving the string to a file
    with open(code_file_name, "w") as file:
        file.write(mermaid_code)
    command = f"mmdc -i {code_file_name} -o {image_file_name} -s 2"
        # Running the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    
    return image_file_name

def generate_dataset_sample():
    noBlocks, noEdges = blocks_and_edges(minBlocks=2, maxBlocks=2) # CHANGE for Level0, Level 1 and Level 2
    blockNames = block_names(noBlocks)  # Block names for Level 0 Diagram
    position_matrix = matrix(3) # CHANGE 4x4 Matrix for Level 0 Diagram, 6x6 for Level 1, 8x8 for Level 2
    position_matrix = place_blocks(position_matrix, blockNames)
    connections = connect_blocks_randomly(position_matrix, noEdges)
    mermaid_code = write_mermaid_code(position_matrix, connections, columns=3) # CHANGE 4 Columns for Level 0, 6 Columns for Level 1, 8 Columns for Level 2
    return mermaid_code

def get_blocks_and_edges(mermaid_code):
    # Extract block names (with multi-word names)
    block_dict = {match[0]: match[1] for match in re.findall(r'(\w+)\["([^"]+)"\]', mermaid_code)}

    # Extract edges with labels
    edges = re.findall(r'(\w+)\s*--\s*"(.*?)"\s*-->\s*(\w+)', mermaid_code)
    edges_with_labels = [(block_dict.get(edge[0], edge[0]), edge[1], block_dict.get(edge[2], edge[2])) for edge in edges]

    # Extract simple edges (without labels)
    simple_edges = re.findall(r'(\w+)\s*-->\s*(\w+)', mermaid_code)
    edges_with_labels.extend([(block_dict.get(edge[0], edge[0]), '', block_dict.get(edge[1], edge[1])) for edge in simple_edges if edge not in edges])

    # # Display results
    # print("Block Names:", list(block_dict.values()))
    # print("Number of Blocks:", len(block_dict))
    # print("Edges with Labels and Triplets:")
    # for edge in edges_with_labels:
    #     print(f"('{edge[0]}', '{edge[1]}', '{edge[2]}')")
    return block_dict, edges_with_labels

def get_topological_summary(block_dict, edges_with_labels):    
    topological_summary = f"""The topological summary of the diagram is as follows:

There are {len(block_dict)} blocks in the diagram:
"""
    counter = 1
    for block in block_dict.values():
        topological_summary += f"{counter}. {block}\n"
        counter += 1
    topological_summary += "\nThe relationships between the blocks are as follows:\n"
    counter = 1
    for edge in edges_with_labels:
        if edge[1]:
            topological_summary += f"{counter}. Relation from '{edge[0]}' to '{edge[2]}' with edge lable '{edge[1]}'.\n"
        else:
            topological_summary += f"{counter}. Relation from '{edge[0]}' to '{edge[2]}' with no edge label.\n"
        counter += 1
    return topological_summary

# If the sample generated from the previous code block is acceptable, save the image and append to the dataset by running this block
from tqdm import tqdm
counter = 0
df = pd.DataFrame(columns=["Image", "Mermaid Code", "Description"])
for _ in tqdm(range(10)):
    mermaid_code = generate_dataset_sample()
    image_path = save_image_and_code(mermaid_code, counter)
    block_dict, edges_with_labels = get_blocks_and_edges(mermaid_code)
    topological_summary = get_topological_summary(block_dict, edges_with_labels)
    df = update_dataset(df, image_path, mermaid_code, topological_summary)
    counter += 1

df.to_json("./BlockDiagramDatasetEasy.json", orient="records", indent=4)