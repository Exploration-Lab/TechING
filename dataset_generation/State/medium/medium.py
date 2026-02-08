import random
import subprocess
import pandas as pd
import re
#Setting number of blocks and edges
def blocks_and_edges(minBlocks, maxBlocks):
    noBlocks = random.randint(minBlocks,maxBlocks)
    noEdges = random.randint(noBlocks,int(1.2*noBlocks))
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

# Engineering Disciplines
engineering_disciplines = [
    'Civil', 'Mechanical', 'Electrical', 'Chemical', 'Computer', 'Aerospace', 
    'Biomedical', 'Industrial', 'Environmental', 'Materials', 'Nuclear', 
    'Software', 'Petroleum', 'Marine', 'Agricultural', 'Mining', 'Geotechnical', 
    'Architectural', 'Robotics', 'Telecommunications', 'Automation', 'Automotive',
    'Mechatronics', 'Energy Systems', 'Renewable Energy', 'Structural', 'Manufacturing'
]

# Business Disciplines
business_disciplines = [
    'Accounting', 'Finance', 'Marketing', 'Management', 'Human Resources', 
    'Entrepreneurship', 'Supply Chain', 'Economics', 'International Business', 
    'Operations Management', 'Business Analytics', 'Information Systems', 'Real Estate', 
    'Hospitality Management', 'E-Commerce', 'Strategy', 'Leadership', 'Corporate Governance',
    'Business Law', 'Innovation Management', 'Retail Management', 'Digital Marketing',
    'Financial Technology', 'Project Management', 'Business Development', 'Nonprofit Management',
    'Organizational Behavior', 'Global Supply Chain'
]

# Science Disciplines
science_disciplines = [
    'Physics', 'Chemistry', 'Biology', 'Mathematics', 'Geology', 'Astronomy', 
    'Meteorology', 'Oceanography', 'Botany', 'Zoology', 'Ecology', 'Genetics', 
    'Microbiology', 'Biochemistry', 'Psychology', 'Sociology', 'Anthropology', 'Forensic Science',
    'Neuroscience', 'Pharmacology', 'Astrophysics', 'Philosophy', 'Statistics', 'Mathematical Biology',
    'Paleontology', 'Immunology', 'Bioinformatics', 'Geophysics', 'Quantum Physics', 'Climate Science',
    'Virology', 'Marine Biology'
]

# Arts Disciplines
arts_disciplines = [
    'Music', 'Dance', 'Theatre', 'Fine Arts', 'Photography', 'Film', 'Fashion', 
    'Graphic Design', 'Interior Design', 'Architecture', 'Literature', 'Painting', 
    'Sculpture', 'Poetry', 'Ceramics', 'Printmaking', 'Textile Design', 'Digital Arts',
    'Public Art', 'Animation', 'Film Studies', 'Cinematography', 'Digital Photography', 'Creative Writing',
    'Stage Design', 'Set Design', 'Jewelry Design', 'Sound Design', 'Performance Arts', 'Art History'
]

# Banking Disciplines
banking_disciplines = [
    'Investment Banking', 'Retail Banking', 'Corporate Banking', 'Private Banking', 
    'Asset Management', 'Hedge Funds', 'Private Equity', 'Venture Capital', 
    'Wealth Management', 'Risk Management', 'Financial Planning', 'Financial Modeling', 
    'Financial Technology', 'Islamic Banking', 'Regulatory Affairs', 'Financial Reporting',
    'Banking Operations', 'Foreign Exchange', 'Mergers & Acquisitions', 'Public Finance', 'Insurance'
]

# Healthcare Disciplines
healthcare_disciplines = [
    'Nursing', 'Pharmacy', 'Dentistry', 'Medicine', 'Physical Therapy', 'Occupational Therapy', 
    'Speech Therapy', 'Radiology', 'Pathology', 'Anesthesiology', 'Cardiology', 'Dermatology', 
    'Endocrinology', 'Gastroenterology', 'Psychiatry', 'Pulmonology', 'Ophthalmology', 'Orthopedics',
    'Neurosurgery', 'Pediatrics', 'Public Health', 'Veterinary Medicine', 'Genetic Counseling', 
    'Oncology', 'Surgical Technology', 'Emergency Medicine', 'Audiology', 'Chiropractic', 'Palliative Care'
]

# Cities
cities = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
    'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 
    'Fort Worth', 'Columbus', 'Indianapolis', 'Charlotte', 'San Francisco', 'Seattle', 
    'Denver', 'Boston', 'Detroit', 'Washington D.C.', 'Miami', 'Las Vegas', 'Atlanta',
    'Portland', 'Minneapolis', 'Kansas City', 'Salt Lake City', 'Raleigh', 'Nashville', 
    'Tampa', 'Cleveland', 'Baltimore', 'Louisville', 'Omaha'
]

# Countries
countries = [
    'USA', 'China', 'India', 'Japan', 'Germany', 'UK', 'France', 'Brazil', 
    'Italy', 'Canada', 'South Korea', 'Russia', 'Australia', 'Spain', 'Mexico', 
    'South Africa', 'Argentina', 'Egypt', 'Saudi Arabia', 'Sweden', 'Norway', 
    'Netherlands', 'Turkey', 'Indonesia', 'Nigeria', 'Israel', 'Chile', 'Greece', 'Poland',
    'Belgium', 'Austria', 'Denmark', 'Finland', 'Malaysia', 'Thailand', 'Vietnam', 'Singapore'
]

# Networks
networks = [
    'Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'Snapchat', 'Pinterest', 
    'Reddit', 'TikTok', 'YouTube', 'WhatsApp', 'Skype', 'Zoom', 'Slack', 'Twitch',
    'Discord', 'Tumblr', 'Vimeo', 'WeChat', 'Telegram', 'TikTok', 'Snapchat', 'Baidu', 
    'QQ', 'Yandex', 'Flickr', 'GitHub', 'Medium'
]

# Sports
sports = [
    'Football', 'Basketball', 'Baseball', 'Soccer', 'Tennis', 'Golf', 'Hockey', 
    'Rugby', 'Cricket', 'Volleyball', 'Boxing', 'MMA', 'Wrestling', 'Track and Field', 
    'Cycling', 'Table Tennis', 'Badminton', 'Swimming', 'Athletics', 'Rowing', 'Skiing', 
    'Snowboarding', 'Gymnastics', 'Skating', 'Handball', 'Lacrosse', 'Fencing', 'Sailing', 
    'Water Polo', 'Equestrian', 'Archery', 'Canoeing', 'Bobsleigh', 'Curling'
]

# Food
food = [
    'Pizza', 'Burger', 'Taco', 'Sushi', 'Pasta', 'Steak', 'Salad', 'Soup', 'Dessert', 
    'Breakfast', 'Seafood', 'Vegetarian', 'Vegan', 'Fried Chicken', 'Sandwich', 'Ice Cream', 
    'Biryani', 'Curry', 'Fried Rice', 'Samosa', 'Casserole', 'Wraps', 'Shawarma', 
    'Ceviche', 'Baklava', 'Falafel', 'Paella', 'Poutine', 'Dim Sum', 'Ramen', 'Kimchi',
    'Chili', 'Goulash', 'Empanadas', 'Tamales', 'Moussaka', 'Kebabs', 'Churros'
]

# Movies
movies = [
    'Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'SciFi', 'Thriller', 'Documentary', 
    'Animation', 'Musical', 'Adventure', 'Fantasy', 'Mystery', 'Crime', 'Historical', 
    'Family', 'Romantic Comedy', 'War', 'Superhero', 'Indie', 'Noir', 'Western', 
    'Documentary', 'Biographical', 'Mockumentary', 'Experimental', 'Art House', 'Cult', 
    'Silent Film', 'Film Noir', 'Action-Adventure', 'Fantasy Drama'
]

# Technology Disciplines
technology_disciplines = [
    'Artificial Intelligence', 'Machine Learning', 'Blockchain', 'Cybersecurity', 
    'Data Science', 'Cloud Computing', 'Robotics', 'Internet of Things', 'Augmented Reality',
    'Virtual Reality', 'Big Data', '5G Technology', 'Autonomous Vehicles', 'Quantum Computing', 
    'Data Analytics', 'Software Engineering', 'Web Development', 'Mobile Development', 
    'Natural Language Processing', 'Human-Computer Interaction', 'Computer Vision', 'Game Development',
    'AI Ethics', 'Neural Networks', 'Digital Transformation', 'Augmented Reality', 'Edge Computing'
]

# Languages
languages = [
    'English', 'Spanish', 'Mandarin', 'French', 'Arabic', 'Russian', 'Hindi', 
    'Portuguese', 'Bengali', 'German', 'Japanese', 'Punjabi', 'Italian', 'Turkish', 
    'Korean', 'Vietnamese', 'Dutch', 'Swahili', 'Telugu', 'Marathi', 'Tamil', 
    'Urdu', 'Polish', 'Ukrainian', 'Romanian', 'Greek', 'Hebrew', 'Swedish', 'Finnish',
    'Danish', 'Norwegian', 'Hungarian', 'Czech', 'Croatian', 'Bulgarian', 'Slovak', 'Hindi'
]
# Pick block names and return a list
def block_names(noBlocks):
    blocks = [
        engineering_disciplines, business_disciplines, science_disciplines, arts_disciplines, banking_disciplines, healthcare_disciplines,
        cities, countries, networks, sports, food, movies, technology_disciplines, languages
    ]
    blockNames = []
    # Pick a single random block category and names of blocks from that category
    category = random.choice(blocks)
    blockNames = random.sample(category, noBlocks)
    return blockNames

# Placing blocks in matrix position
def place_blocks(matrix, blockNames):
    for block in blockNames:
        strippedBlock = block.replace(" ", "")
        strippedBlock = strippedBlock.replace("-", "")
        while True:
            i = random.randint(0, len(matrix) - 1)
            j = random.randint(0, len(matrix) - 1)
            if is_position_safe(matrix, i, j):
                matrix[i][j] = f"{strippedBlock}[\"{block}\"]:1"
                break
    return matrix

# connect blocks randomly
def connect_blocks_randomly(matrix, noEdges):
    coordinates = [(x, y) for x in range(len(matrix)) for y in range(len(matrix[0])) if matrix[x][y] != 'space']
    connections = []
    for _ in range(noEdges):
        while True:
            # Pick two random blocks
            block1coord, block2coord = random.sample(coordinates, 2)
            # print(block1coord, block2coord)
            # Code to make sure that if we connect those two blocks the edge doesn't intersect with any other block
            x, y = block1coord
            s, t = block2coord
            del_x = abs(x - s)
            del_y = abs(y - t)
            if del_x > 3 or del_y > 2:
                continue
            else:
                block1 = matrix[x][y].split('[')[0]
                block2 = matrix[s][t].split('[')[0]
                # If the edge doesn't already exist, add it to the connections list
                if f"{block1} --> {block2}" not in connections:
                    connections.append(f"{block1} --> {block2}")
                    break
        # Add the edge to the connections list
        
    return connections

# Creating the dataset (run only once)
df = pd.DataFrame(columns=["Image Path", "Mermaid Code", "Description"])
# df
# Update the dataset with new rows
def update_dataset(image_path, mermaid_code, description):
    global df
    # for serial, (question, option, answer) in enumerate(zip(questions, options, answers)):
    #     if serial == 0 or serial == 1:
    #         QuestionComplexity = 0
    #     elif serial == 2 or serial == 3:
    #         QuestionComplexity = 1
    #     else:
    #         QuestionComplexity = 2
    new_row = {
        "Image Path": [image_path],
        "Mermaid Code": [mermaid_code],
        "Description":[description]
        # "Diagram Complexity": [diagramComplexity],
        # "Questions": [question],
        # "Options": [option],
        # "Correct Answer": [answer],
        
        # "Question Complexity": [QuestionComplexity]
    }
    new_row = pd.DataFrame(new_row)

    # Append the new row using concat
    df = pd.concat([df, new_row], ignore_index=True)
    
    
def write_mermaid_code(position_matrix, connections, columns):
    # Mermaid syntax as a string
    mermaid_code = "stateDiagram-v2\n"

    # Add connections (transitions)
    for connection in connections:
        mermaid_code += f"    {connection}\n"

    # Saving the code to a temporary test file
    file_name = "./test6.mmd"
    try:
        with open(file_name, "w") as file:
            file.write(mermaid_code)
    except Exception as e:
        print(f"Error writing Mermaid code to file: {e}")
        return

    # Generate the image using the Mermaid CLI
    image_file_name = "./test6.png"
    command = f"mmdc -i {file_name} -o {image_file_name} -s 2"
    print(f"Running command: {command}")  # Debugging the command

    # Running the command
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error generating image: {e.stderr}")
        
    return mermaid_code


import time, os
def save_image_and_code(mermaid_code, counter):
    # File name to save as .mmd
    code_file_name = f"./StateDiagramMedium/MermaidCode/StateDiagram{counter}.mmd"
    image_file_name = f"./StateDiagramMedium/MermaidImage/StateDiagram{counter}.png"
    
    if not os.path.exists('./StateDiagramMedium/MermaidCode/'):
        os.makedirs('./StateDiagramMedium/MermaidCode/')
    if not os.path.exists('./StateDiagramMedium//MermaidImage/'):
        os.makedirs('./StateDiagramMedium/MermaidImage/')

    # Saving the string to a file
    with open(code_file_name, "w") as file:
        file.write(mermaid_code)
    command = f"mmdc -i {code_file_name} -o {image_file_name} -s 2"
        # Running the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(2)
    print(result.stdout)
    
    return image_file_name

def generate_dataset_sample():
    noBlocks, noEdges = blocks_and_edges(minBlocks=5, maxBlocks=10) # CHANGE for Level0, Level 1 and Level 2
    blockNames = block_names(noBlocks)  # Block names for Level 0 Diagram
    position_matrix = matrix(6,6) 
    # print('position matrix')
    position_matrix = place_blocks(position_matrix, blockNames)
    connections = connect_blocks_randomly(position_matrix, noEdges)
    # Questions, options, answers = generate_questions(blockNames, connections)
    mermaid_code = write_mermaid_code(position_matrix, connections, columns=5) # CHANGE 4 Columns for Level 0, 6 Columns for Level 1, 8 Columns for Level 2

    return mermaid_code
def get_blocks_and_edges(mermaid_code):
    lines = mermaid_code.strip().split("\n")
    states = set()
    transitions = []

    for line in lines:
        line = line.strip()

        # Regex to match transitions with optional edge labels
        match = re.match(r'"([\w\s&_.]+)"\s*-->\s*"([\w\s&_.]+)"(?:\s*:\s*"([\w\s&_.]+)")?', line)

        if match:
            # from_state = match.group(1).replace("_", " ").strip()
            # to_state = match.group(2).replace("_", " ").strip()
            from_state = match.group(1).strip()
            to_state = match.group(2)
            edge_label = match.group(3).strip() if match.group(3) else None
            

            states.add(from_state)
            states.add(to_state)
            
            transitions.append({
                "from": from_state,
                "to": to_state,
                "label": edge_label if edge_label else ""
            })

    summary = {
        "states": list(set(states)),
        "transitions": transitions
    }
    return summary

def get_topological_summary(summary):    
    topological_summary = f"""The topological summary of the diagram is as follows:

There are {len(summary['states'])} states in the diagram:
"""
    counter = 1
    topological_summary += "\nThe name of the states are as follows:\n"
    for block in summary['states']:
        topological_summary += f"{counter}. '{block}'\n"
        counter += 1

    topological_summary += "\nThe transitions between the states are as follows:\n"
    counter = 1
    for rel in summary['transitions']:
        if rel['label']:
            topological_summary += f"{counter}. Transition from '{rel['from']}' to '{rel['to']}' with edge label '{rel['label']}'\n"
        else:
            topological_summary += f"{counter}. Transition from '{rel['from']}' to '{rel['to']}'\n"
        counter += 1
    return topological_summary


counter = 0
for i in range(3):
    mermaid_code = generate_dataset_sample()
    summary = get_blocks_and_edges(mermaid_code)
    # print(summary)
    description = get_topological_summary(summary)
    # print(description)
    image_path = save_image_and_code(mermaid_code, counter)
    update_dataset(image_path, mermaid_code, description)
    counter += 1
    print(counter)
df.to_json("StateDiagramDatasetMedium.json", orient="records", indent=4)

