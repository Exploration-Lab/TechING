import random
import subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, deque
import pandas as pd
from IPython.display import Image, display
import re
import json
from tqdm import tqdm
import os

#Setting number of blocks and edges
def blocks_and_edges(minBlocks, maxBlocks):
    noBlocks = random.randint(minBlocks,maxBlocks)
    noEdges = noBlocks
    # noEdges = random.randint(minBlocks-2,maxBlocks)
    return noBlocks, noEdges

# Create a matrix of size m x n and fill it with 'space'
def matrix(m,n):
    position_matrix = [['space' for i in range(n)] for j in range(m)]
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
engineering_disciplines = ['Civil Engg', 'Mechanical Engineering', 'Electrical', 'Chemical', 'Computer Science', 'Aerospace', 'Biomedical Waste', 'Industrial', 'Environmental Clearance', 'Materials', 'Nuclear', 'Software', 'Petroleum Industry', 'Marine']
business_disciplines = ['Accounting Role', 'Finance', 'Marketing', 'Management Enterprise', 'Human Resources', 'Entrepreneurship', 'Supply Chain', 'Economics System', 'International Business', 'Operations Management', 'Business Analytics', 'Information Systems', 'Real Estate', 'Hospitality Management']
science_disciplines = ['Physics Discipline', 'Chemistry', 'Biology', 'Mathematics', 'Geology Sciences', 'Astronomy', 'Meteorology', 'Oceanography Report', 'Botany', 'Zoology', 'Ecology', 'Genetic Mutation', 'Microbiology', 'Biochemistry']
arts_disciplines = ['Music', 'Dance Festival', 'Theatre', 'Fine Arts', 'Photography', 'Film', 'Fashion Icon', 'Graphic Design', 'Interior Design', 'Architecture']
banking_disciplines = ['Investment Banking', 'Retail Banking', 'Corporate Banking', 'Private Banking', 'Asset Management', 'Hedge Funds', 'Private Equity', 'Venture Capital']
healthcare_disciplines = ['Nursing', 'Pharmacy Store', 'Dentistry', 'Medicine Booth', 'Physical Therapy', 'Occupational Therapy', 'Speech Therapy', 'Radiology', 'Pathology', 'Anesthesiology', 'Cardiology', 'Dermatology', 'Endocrinology', 'Gastroenterology']
cities = ['New York State', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia Crash', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin University', 'Jacksonville', 'Fort Worth', 'Columbus']
countries = ['USA', 'China PLA', 'India', 'Japan', 'Germany', 'UK', 'France', 'Brazil Forest', 'Italy', 'Canada', 'South Korea', 'Russia', 'Cricket Australia', 'Spain']
networks = ['Facebook Inc', 'Twitter', 'Instagram', 'LinkedIn Portal', 'Snapchat', 'Pinterest', 'Reddit', 'TikTok Trend', 'YouTube', 'WhatsApp University', 'Skype', 'Zoom', 'Slack Channel', 'Twitch']
sports = ['Football Team', 'Basketball', 'Baseball', 'Soccer', 'Tennis Tournament', 'Golf', 'Hockey', 'Rugby', 'Cricket Stadium', 'Volleyball', 'Boxing', 'MMA Fighter', 'Wrestling', 'Track and Field']
food = ['Pizza King', 'Burger', 'Taco bell', 'Sushi', 'Pasta Street', 'Steak', 'Salad', 'Soup', 'Dessert', 'Breakfast Date', 'Seafood Festival', 'Vegetarian', 'Vegan Menu']
movies = ['Action', 'Comedy King', 'Drama', 'Horror', 'Romance', 'SciFi', 'Thriller Plot', 'Documentary', 'Animation', 'Musical Comedy', 'Adventure', 'Fantasy World', 'Mystery', 'Crime Drama']

edge_labels = ['connects', 'is part of', 'uses', 'sends data to', 'is located in',
                'is made of', 'is found in', 'is played in', 'is served in', 'is shown in',
                'is produced in', 'is studied in', 'is practiced in', 'is managed by', 'is owned by',
                'manages', 'owns', 'operates', 'controls', 'develops', 'creates',
                'builds', 'designs', 'tests', 'analyzes', 'researches', 'teaches',
                'learns', 'performs', 'competes in', 'receives', 'provides', 'offers',
                'sells', 'buys', 'markets', 'advertises', 'promotes', 'supports',
                'deals with'
]

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
    accepted_positions = [(0,0), (0,3),
                          (3,0), (3,3),
                          (6,0), (6,3)
                          ]    
    for block in blockNames:
        x = random.randint(0, len(accepted_positions)-1)
        i, j = accepted_positions[x]
        strippedBlock = block.replace(" ", "")
        strippedBlock = strippedBlock.replace("-", "")
        matrix[i][j] = f"{strippedBlock}[\"{block}\"]:1"
        accepted_positions.pop(x)
    return matrix

# connect blocks randomly
def connect_blocks_randomly(matrix, noEdges):
    coordinates = [(x, y) for x in range(len(matrix)) for y in range(len(matrix[0])) if matrix[x][y] != 'space']
    connections = []
    edge_occupied = []
    count = 0
    for _ in range(noEdges):
        while True:
            # Pick two random blocks
            while True:
                block1coord, block2coord = random.sample(coordinates, 2)
                if (block1coord, block2coord) not in edge_occupied and (block2coord, block1coord) not in edge_occupied:
                    edge_occupied.append((block1coord, block2coord))
                    count += 1
                    break
                else:
                    count += 1
                    if count > 20:
                        return connections
            x, y = block1coord
            s, t = block2coord
            del_x = abs(x - s)
            del_y = abs(y - t)
            if del_x > 3 or del_y > 3:
                continue
            else:
                block1 = matrix[x][y].split('[')[0]
                block2 = matrix[s][t].split('[')[0]
                # If the edge doesn't already exist, add it to the connections list
                if f"{block1} --> {block2}" not in connections:
                    prob = random.choice([0, 1])
                    if prob == 0: 
                        label = random.choice(edge_labels)
                        connections.append(f"""{block1} -- "{label}" --> {block2}""")
                    else:
                        connections.append(f"{block1} --> {block2}")
                    break
        # Add the edge to the connections list
        
    return connections

# Develop the mermaid code, save it to test file and generate it's mermaid image
def write_mermaid_code(position_matrix, connections, columns):
    # Mermaid syntax as a string
    mermaid_code = f"""block-beta
columns {columns}
"""
    for row in range(len(position_matrix)):
        mermaid_code += "    "
        for col in range(len(position_matrix[0])):
            mermaid_code += f"{position_matrix[row][col]} "
        mermaid_code += "\n"
    mermaid_code += "\n"    
    for connection in connections:
        mermaid_code += f"    {connection}\n"

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

def generate_dataset_sample():
    noBlocks, noEdges = blocks_and_edges(minBlocks=4, maxBlocks=6)
    blockNames = block_names(noBlocks) 
    position_matrix = matrix(7,4)
    position_matrix = place_blocks(position_matrix, blockNames)
    connections = connect_blocks_randomly(position_matrix, noEdges)
    mermaid_code = write_mermaid_code(position_matrix, connections, columns=4) 
    return mermaid_code

def save_image_and_code(mermaid_code, counter):
    os.makedirs("MermaidImage1", exist_ok=True)
    os.makedirs("MermaidCode1", exist_ok=True)
    # File name to save as .mmd
    code_file_name = f"./MermaidCode1/BlockDiagram{counter}.mmd"
    image_file_name = f"./MermaidImage1/BlockDiagram{counter}.png"
    # Saving the string to a file
    with open(code_file_name, "w") as file:
        file.write(mermaid_code)
    command = f"mmdc -i {code_file_name} -o {image_file_name} -s 2"
        # Running the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # print(result.stdout)
    
    return image_file_name

# Update the dataset with new rows
def update_dataset(df, image_path, mermaid_code, topological_summary):
    new_row = {
        "Image": [image_path],
        "Mermaid Code": [mermaid_code],
        "Description": [topological_summary]
    }
    new_row = pd.DataFrame(new_row)

    # Append the new row using concat
    df = pd.concat([df, new_row], ignore_index=True)
    return df

counter = 0
df = pd.DataFrame(columns=["Image", "Mermaid Code", "Description"])
for _ in tqdm(range(10)):
    mermaid_code = generate_dataset_sample()
    image_path = save_image_and_code(mermaid_code, counter)
    block_dict, edges_with_labels = get_blocks_and_edges(mermaid_code)
    topological_summary = get_topological_summary(block_dict, edges_with_labels)
    df = update_dataset(df, image_path, mermaid_code, topological_summary)
    counter += 1

df.to_json("./BlockDiagramDataset1.json", orient="records", indent=4)