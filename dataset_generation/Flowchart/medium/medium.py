import random
import numpy as np

direction = ['LR', 'RL', 'TB', 'BT']

start = f'''---
title: Flowchart
---
flowchart {random.choice(direction)}\n'''
# print(start)

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

box_types = ['rect', 'lean-r', 'lean-l', 'cyl', 'diam', 'delay', 'h-cyl',"curv-trap","div-rect","doc","rounded","tri","win-pane","lin-doc","lin-rect","notch-pent","flip-tri","sl-rect","trap-t","circle",
    # "sm-circ",
    "dbl-circ",
    # "fr-circ",
    "bow-rect",
    "fr-rect",
    "tag-doc",
    "tag-rect",
    "stadium"]

link_types= ['-->', '---', '-.->', '==>', '== {text} ==>','-- {text} ---', '-. {text} .->', '== {text} ==>',]
# also for including text
# whether after entity is & or arrow
# choose from already existing link, ['A', 'B'] or a new one chr(ord('A') + 1)

# Check for subgraph
'''
subgraph title
    graph definition
end
'''

subgraph_names = [
    "engineering_disciplines",
    "business_disciplines",
    "science_disciplines",
    "arts_disciplines",
    "banking_disciplines",
    "healthcare_disciplines",
    "cities",
    "countries",
    "networks",
    "sports",
    "food",
    "movies",
    "technology_disciplines",
    "languages"
]
MAX_NUM_BLOCKS = 3
MIN_NUM_BLOCKS = 1
MAX_NUM_ENTITIES = 3
MIN_NUM_ENTITIES = 2
MAX_NUM_EDGES = 3
MIN_NUM_EDGES = 1
MAX_LINK_SUBGRAPHS = 2
MIN_LINK_SUBGRAPHS = 1

def create_chart():

    start = f'''---
title: Flowchart
---
    flowchart {random.choice(direction)}\n'''

    blocks = [
            engineering_disciplines, business_disciplines, science_disciplines, arts_disciplines, banking_disciplines, healthcare_disciplines,
            cities, countries, networks, sports, food, movies, technology_disciplines, languages
        ]

    num_blocks = random.randint(MIN_NUM_BLOCKS, MAX_NUM_BLOCKS)
    chosen_blocks = random.choices(blocks, k = num_blocks)

    chosen_entities_1d = []

    num_entities = []
    chosen_entities = []
    for item in chosen_blocks:
        n_entity = random.randint(MIN_NUM_ENTITIES, MAX_NUM_ENTITIES)
        chosen = random.choices(item, k=n_entity)
        chosen_entities.append(chosen) # here we got a list of chosen entities
        for it in chosen:
            chosen_entities_1d.append(it)
        
        num_entities.append(n_entity) # here we got a list containing number of entities in each block
    
    entities_char_1d = []
    chosen_entities_char = []
    ## Adding the components 
    idd = 'A'
    for block in chosen_entities:
        ls = []
        for entity in block:
            entities_char_1d.append(idd)
            ls.append(idd)
            start += (f'   {idd}@'+'{ shape: '+str(random.choice(box_types))+', label: '+f'"{entity}"'+'}\n')
            idd = chr(ord(idd) + 1)
        chosen_entities_char.append(ls)
            
    subgraphs = []
    ## Adding Subgraphs
    for block in chosen_entities_char:
        sub_name = random.choice(subgraph_names)
        subgraphs.append(sub_name)
        start += f'''   subgraph {sub_name}
        direction TB
    '''
        for entity in block:
            num_edges = random.randint(MIN_NUM_EDGES, MAX_NUM_EDGES)
            for i in range(num_edges):
                if random.random()>0.5:
                    link_to = random.choice(entities_char_1d)
                    while link_to == entity:
                        link_to = random.choice(entities_char_1d)
                    link_type = random.choice(link_types)
                    start += f'      {entity} {link_type.format(text=random.sample(sports, k=1)[0])}{link_to}\n'
        start+='   end\n'
            
    ## linking 
    for subgraph in subgraphs:
        num_links = random.randint(MIN_LINK_SUBGRAPHS, MAX_LINK_SUBGRAPHS)
        for i in range(num_links):
            if random.random()> 0.5:
                link_to = random.choice(subgraphs)
                while link_to == subgraph:
                    link_to = random.choice(subgraphs)
                link_type = random.choice(link_types)
                start += f'   {subgraph} {link_type.format(text=random.sample(cities, k=1)[0])}{link_to}\n'
    return start

# Function to parse the Mermaid flowchart and build a structural summary
import re
def get_blocks_and_edges(mermaid_code):
    nodes = {
    "N1": {
      "shape": "stadium",
      "label": "Start"
    }}
    
    relationships = []

    lines = mermaid_code.splitlines()

    for line in lines:
        line = line.strip()

        # Extract node information (ID, shape, label)
        node_match = re.match(r'(\w+)@\{\s*shape:\s*(\w+-?\w*),\s*label:\s*"(.*?)"\s*\}', line)
        if node_match:
            node_id = node_match.group(1)
            shape = node_match.group(2)
            label = node_match.group(3)
            nodes[node_id] = {"shape": shape, "label": label}
            continue  # skip to next line

        # Match shorthand node: N1(""Start"")
        shorthand_match = re.match(r'(\w+)\(\s*""(.*?)""\s*\)', line)
        if shorthand_match:
            node_id = shorthand_match.group(1)
            label = shorthand_match.group(2)
            nodes[node_id] = {"shape": "stadium", "label": label}

        # Extract relationships with or without labels
        rel_match = re.match(
                            r'(\w+)\s*'
                            r'(?:'
                            r'==\s*(?P<label1>.*?)\s*==>\s*'        # labeled: == label ==>
                            r'|-\.\s*(?P<label2>.*?)\s*\.-\>\s*'    # labeled: -. label .->
                            r'|--\s*(?P<label3>.*?)\s*---\s*'       # labeled: -- label ---
                            r'|---\s*'                              # plain -->
                            r'|-->\s*'                              # plain -->
                            r'|==>\s*'                              # plain ==>
                            r'|-\.-\>\s*'                           # plain -.-> (escaped correctly)
                            r')'
                            r'(\w+)',                               # target
                            line
                        )


        if rel_match:
            source = rel_match.group(1)
            target = rel_match.group(5)
            label = next(
                        (rel_match.group(name) for name in ('label1', 'label2', 'label3') if rel_match.group(name)),
                        ""
                    )
            relationships.append({"source": source, "target": target, "label": label.strip()})

    # Build the summary
    summary = {
        "nodes": nodes,
        "relationships": relationships
    }
    return summary

def get_topological_summary(summary):    
    topological_summary = f"""The topological summary of the diagram is as follows:

There are {len(summary['nodes'])} blocks in the diagram:
"""
    counter = 1
    for block in summary['nodes'].keys():
        topological_summary += f"{counter}. '{summary['nodes'][block]['label']}'\n"
        counter += 1

    topological_summary += "\nThe relationships between the blocks are as follows:\n"
    counter = 1
    for rel in summary['relationships']:
        if rel['label'] == '':
            counter += 1
            topological_summary += f"{counter}. Relation from '{summary['nodes'][rel['source']]['label']}' to '{summary['nodes'][rel['target']]['label']}' with no edge label.\n"
        else:
            topological_summary += f"{counter}. Relation from '{summary['nodes'][rel['source']]['label']}' to '{summary['nodes'][rel['target']]['label']}' with edge label '{rel['label']}'.\n"
            counter += 1
    return topological_summary

import subprocess
import os
import pandas as pd
code_dir = 'FlowchartMedium/MermaidCode/'
image_dir = 'FlowchartMedium/MermaidImage/'
os.makedirs(code_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)
filename_base = 'Flowchart'
df = pd.DataFrame(columns=["Image Path", "Mermaid Code", "Description"])
i=0
while True:
    try:
        print(i)
        mermaid_code = create_chart()
        summary = get_blocks_and_edges(mermaid_code)
        print(summary)
        topological_summary = get_topological_summary(summary)
        txt_file_name = code_dir+filename_base+f'{i}.mmd'
        image_file_name = image_dir+filename_base+f'{i}.png'
        print(txt_file_name, image_file_name)
    except:
        continue
        
    try:
        with open(txt_file_name, 'w') as f:
            f.write(mermaid_code)
        command = f"mmdc -i {txt_file_name} -o {image_file_name} -s 2"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except:
        print('file removed and continued')
        os.remove(txt_file_name)
        continue 
    
    df.loc[i] = [image_file_name, mermaid_code,topological_summary]
    if i == 2:
        break
    i+=1
    # break
df.to_json("./FlowchartDiagramDatasetMedium.json", orient="records", indent=4)
    
    