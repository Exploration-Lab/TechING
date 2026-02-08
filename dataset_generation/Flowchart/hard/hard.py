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
    'Civil engineering focuses on infrastructure design.',
    'Mechanical engineering deals with machinery and tools.',
    'Electrical engineering studies electrical systems.',
    'Chemical engineering involves chemical processes.',
    'Computer engineering integrates hardware and software.',
    'Aerospace engineering develops aircraft and spacecraft.',
    'Biomedical engineering improves medical devices and healthcare.',
    'Industrial engineering optimizes complex production systems.',
    'Environmental engineering addresses sustainability challenges.',
    'Materials science studies properties of materials.',
    'Nuclear engineering works with nuclear energy.',
    'Software engineering develops and maintains software applications.',
    'Petroleum engineering focuses on oil and gas extraction.',
    'Marine engineering designs and maintains marine vessels.',
    'Agricultural engineering enhances farming technology.',
    'Mining engineering deals with resource extraction.',
    'Geotechnical engineering studies soil and foundations.',
    'Architectural engineering integrates design and construction.',
    'Robotics engineering creates intelligent automated systems.',
    'Telecommunications engineering improves communication networks.',
    'Automation engineering streamlines industrial processes.',
    'Automotive engineering advances vehicle technology.',
    'Mechatronics combines mechanics and electronics.',
    'Energy systems engineering optimizes power generation.',
    'Renewable energy engineering focuses on sustainable sources.',
    'Structural engineering ensures stability in construction.',
    'Manufacturing engineering enhances production efficiency.'
]

# Business Disciplines
business_disciplines = [
    'Accounting tracks financial transactions and statements.',
    'Finance manages investments and economic planning.',
    'Marketing promotes products and brand awareness.',
    'Management oversees business operations effectively.',
    'Human resources handles employee relations.',
    'Entrepreneurship drives new business ventures.',
    'Supply chain optimizes production and logistics.',
    'Economics analyzes markets and financial trends.',
    'International business expands companies globally.',
    'Operations management improves business efficiency.',
    'Business analytics uses data for decisions.',
    'Information systems integrate technology in business.',
    'Real estate involves property investment strategies.',
    'Hospitality management enhances guest experiences.',
    'E-commerce boosts online business sales.',
    'Strategy planning drives corporate success.',
    'Leadership fosters organizational growth and innovation.',
    'Corporate governance ensures business accountability.',
    'Business law regulates corporate legal matters.',
    'Innovation management enhances product development.',
    'Retail management optimizes store operations.',
    'Digital marketing promotes brands online.',
    'Financial technology innovates banking solutions.',
    'Project management organizes business initiatives.',
    'Business development expands company opportunities.',
    'Nonprofit management oversees charitable organizations.',
    'Organizational behavior studies workplace dynamics.',
    'Global supply chain manages international logistics.'
]

# Science Disciplines
science_disciplines = [
    'Physics explores fundamental natural laws.',
    'Chemistry studies matter and reactions.',
    'Biology examines living organisms and ecosystems.',
    'Mathematics develops theories and equations.',
    'Geology investigates Earth’s structure and composition.',
    'Astronomy explores celestial objects and space.',
    'Meteorology predicts weather and climate patterns.',
    'Oceanography studies marine environments.',
    'Botany focuses on plant biology.',
    'Zoology examines animal species and behavior.',
    'Ecology analyzes ecosystems and conservation.',
    'Genetics studies DNA and inheritance.',
    'Microbiology researches microscopic organisms.',
    'Biochemistry connects chemistry and biology.',
    'Psychology studies human mind and behavior.',
    'Sociology analyzes social structures.',
    'Anthropology explores human history and culture.',
    'Forensic science aids criminal investigations.',
    'Neuroscience researches the nervous system.',
    'Pharmacology studies drugs and their effects.',
    'Astrophysics examines space phenomena.',
    'Philosophy explores human thought and logic.',
    'Statistics analyzes data for insights.',
    'Mathematical biology models biological systems.',
    'Paleontology studies ancient fossils.',
    'Immunology examines immune system responses.',
    'Bioinformatics processes biological data.',
    "Geophysics investigates Earth's physical properties.",
    'Quantum physics studies atomic behavior.',
    'Climate science examines global temperature trends.',
    'Virology researches viruses and infections.',
    'Marine biology explores oceanic life.'
]
# Arts Disciplines
arts_disciplines = [
    'Music explores sound, rhythm, and harmony.',
    'Dance expresses emotions through movement.',
    'Theatre brings stories to life on stage.',
    'Fine arts encompass painting and sculpture.',
    'Photography captures moments and perspectives.',
    'Film creates visual storytelling experiences.',
    'Fashion designs clothing and personal style.',
    'Graphic design enhances visual communication.',
    'Interior design improves indoor aesthetics.',
    'Architecture blends art with structural design.',
    'Literature explores stories and human expression.',
    'Painting brings imagination to the canvas.',
    'Sculpture crafts three-dimensional art forms.',
    'Poetry conveys emotions through words.',
    'Ceramics shapes artistic clay structures.',
    'Printmaking creates unique visual designs.',
    'Textile design innovates fabric patterns.',
    'Digital arts utilize technology for creativity.',
    'Public art enhances shared urban spaces.',
    'Animation brings drawings to motion.',
    'Film studies analyze cinematic techniques.',
    'Cinematography captures compelling visuals.',
    'Digital photography refines image creation.',
    'Creative writing develops compelling narratives.',
    'Stage design builds immersive theater sets.',
    'Set design enhances performance spaces.',
    'Jewelry design creates decorative accessories.',
    'Sound design enhances auditory experiences.',
    'Performance arts express emotions live.',
    'Art history studies artistic evolution.'
]

# Banking Disciplines
banking_disciplines = [
    'Investment banking manages financial assets.',
    'Retail banking provides consumer financial services.',
    'Corporate banking supports business financing.',
    'Private banking offers personalized wealth management.',
    'Asset management optimizes investment portfolios.',
    'Hedge funds handle high-risk investments.',
    'Private equity invests in private companies.',
    'Venture capital funds startup growth.',
    'Wealth management builds financial security.',
    'Risk management minimizes financial uncertainties.',
    'Financial planning sets economic goals.',
    'Financial modeling forecasts market trends.',
    'Financial technology enhances banking efficiency.',
    'Islamic banking follows Sharia finance rules.',
    'Regulatory affairs ensure compliance in finance.',
    'Financial reporting analyzes business performance.',
    'Banking operations oversee financial transactions.',
    'Foreign exchange trades global currencies.',
    'Mergers & acquisitions restructure corporations.',
    'Public finance manages government resources.',
    'Insurance provides financial risk protection.'
]

# Healthcare Disciplines
healthcare_disciplines = [
    'Nursing provides essential patient care.',
    'Pharmacy dispenses and researches medications.',
    'Dentistry focuses on oral health.',
    'Medicine diagnoses and treats diseases.',
    'Physical therapy aids injury recovery.',
    'Occupational therapy restores daily functions.',
    'Speech therapy improves communication skills.',
    'Radiology diagnoses conditions with imaging.',
    'Pathology studies diseases and their causes.',
    'Anesthesiology ensures pain-free procedures.',
    'Cardiology treats heart-related conditions.',
    'Dermatology specializes in skin health.',
    'Endocrinology focuses on hormone disorders.',
    'Gastroenterology studies digestive health.',
    'Psychiatry addresses mental health issues.',
    'Pulmonology treats lung diseases.',
    'Ophthalmology specializes in eye care.',
    'Orthopedics focuses on bone health.',
    'Neurosurgery performs brain and spine surgeries.',
    'Pediatrics cares for children’s health.',
    'Public health promotes community wellness.',
    'Veterinary medicine treats animal health.',
    'Genetic counseling advises on inherited conditions.',
    'Oncology specializes in cancer treatment.',
    'Surgical technology assists in operations.',
    'Emergency medicine handles urgent care.',
    'Audiology diagnoses hearing disorders.',
    'Chiropractic treats spinal misalignments.',
    'Palliative care supports terminal patients.'
]

# Cities
cities = [
    'New York offers vibrant urban life.',
    'Los Angeles leads in entertainment industry.',
    'Chicago blends history with modern architecture.',
    'Houston thrives in space and energy sectors.',
    'Phoenix boasts a warm desert climate.',
    'Philadelphia holds rich historical significance.',
    'San Antonio preserves cultural heritage.',
    'San Diego offers scenic coastal views.',
    'Dallas excels in business and technology.',
    'San Jose fosters Silicon Valley innovation.',
    'Austin blends music with tech startups.',
    'Jacksonville features vast riverfront areas.',
    'Fort Worth showcases Western traditions.',
    'Columbus flourishes in education and research.',
    'Indianapolis celebrates motorsports culture.',
    'Charlotte thrives as a financial hub.',
    'San Francisco pioneers tech advancements.',
    'Seattle drives innovation and coffee culture.',
    'Denver enjoys a mountain-filled landscape.',
    'Boston excels in academia and history.',
    'Detroit revitalizes automotive industries.',
    'Washington D.C. holds national significance.',
    'Miami thrives in tourism and nightlife.',
    'Las Vegas offers world-famous entertainment.',
    'Atlanta fosters Southern hospitality and business.',
    'Portland embraces sustainability and creativity.',
    'Minneapolis thrives in arts and commerce.',
    'Kansas City is known for barbecue culture.',
    'Salt Lake City offers winter sports destinations.',
    'Raleigh leads in research and innovation.',
    'Nashville thrives as a music capital.',
    'Tampa provides beautiful coastal living.',
    'Cleveland boasts diverse cultural attractions.',
    'Baltimore blends maritime history with arts.',
    'Louisville celebrates horse racing traditions.',
    'Omaha develops strong business communities.'
]

# Technology Disciplines
technology_disciplines = [
    'Artificial intelligence powers smart systems.',
    'Machine learning enables data-driven predictions.',
    'Blockchain secures digital transactions.',
    'Cybersecurity protects online information.',
    'Data science uncovers actionable insights.',
    'Cloud computing scales IT infrastructure.',
    'Robotics automates industrial processes.',
    'Internet of Things connects smart devices.',
    'Augmented reality enhances digital experiences.',
    'Virtual reality creates immersive simulations.',
    'Big data analyzes large datasets.',
    '5G technology improves wireless connectivity.',
    'Autonomous vehicles revolutionize transportation.',
    'Quantum computing advances computational power.',
    'Data analytics optimizes business strategies.',
    'Software engineering builds digital applications.',
    'Web development creates interactive websites.',
    'Mobile development enhances smartphone functionality.',
    'Natural language processing improves AI communication.',
    'Human-computer interaction studies user experience.',
    'Computer vision powers image recognition.',
    'Game development designs engaging virtual worlds.',
    'AI ethics ensures responsible technology use.',
    'Neural networks mimic human brain functions.',
    'Digital transformation modernizes businesses.',
    'Edge computing enhances processing efficiency.'
]

# Languages
languages = [
    'English dominates global communication.',
    'Spanish flourishes in many countries.',
    'Mandarin is China’s primary language.',
    'French thrives in diplomacy and culture.',
    'Arabic has deep historical significance.',
    'Russian holds political and scientific importance.',
    'Hindi unites many Indian communities.',
    'Portuguese spans multiple continents.',
    'Bengali is widely spoken in South Asia.',
    'German influences global engineering advancements.',
    'Japanese integrates tradition with technology.',
    'Punjabi connects diverse communities worldwide.',
    'Italian celebrates art and cuisine.',
    'Turkish bridges Europe and Asia.',
    'Korean drives global entertainment exports.',
    'Vietnamese reflects Southeast Asian culture.',
    'Dutch influences European trade and business.',
    'Swahili unites East African regions.',
    'Telugu thrives in South India.',
    'Marathi is widely spoken in Maharashtra.',
    'Tamil has ancient literary heritage.',
    'Urdu connects South Asian communities.',
    'Polish influences Eastern European history.',
    'Ukrainian strengthens national identity.',
    'Romanian bridges Latin and Slavic influences.',
    'Greek preserves ancient philosophical traditions.',
    'Hebrew plays a central role in Israel.',
    'Swedish leads in innovation and design.',
    'Finnish promotes linguistic uniqueness.',
    'Danish fosters Scandinavian unity.',
    'Norwegian blends heritage with modernity.',
    'Hungarian preserves a unique language structure.',
    'Czech embraces rich cultural legacies.',
    'Croatian thrives along the Adriatic coast.',
    'Bulgarian enriches Slavic linguistic history.',
    'Slovak maintains strong European ties.'
]
# Countries
countries = [
    'The USA stands for united States of America.',
    'China has the world’s largest population.',
    'India is rich in cultural diversity.',
    'Japan excels in technology and tradition.',
    'Germany is a powerhouse of engineering.',
    'The UK blends history with modernity.',
    'France is famous for art and cuisine.',
    'Brazil thrives in football and festivals.',
    'Italy showcases ancient history and fashion.',
    'Canada offers vast natural landscapes.',
    'South Korea drives global pop culture.',
    'Russia spans across two continents.',
    'Australia is known for unique wildlife.',
    'Spain celebrates art and architecture.',
    'Mexico offers vibrant traditions and cuisine.',
    'South Africa leads in wildlife conservation.',
    'Argentina is passionate about tango and football.',
    'Egypt preserves ancient pyramids and history.',
    'Saudi Arabia is central to Islamic heritage.',
    'Sweden is a leader in sustainability.',
    'Norway boasts breathtaking fjords and landscapes.',
    'The Netherlands pioneers water management.',
    'Turkey connects Europe and Asia seamlessly.',
    'Indonesia is an archipelago of diverse cultures.',
    'Nigeria has a thriving film industry.',
    'Israel excels in technology and innovation.',
    'Chile offers stunning mountain landscapes.',
    'Greece is the birthplace of democracy.',
    'Poland has a rich medieval history.',
    'Belgium is known for chocolate and waffles.',
    'Austria embraces classical music and skiing.',
    'Denmark ranks high in happiness.',
    'Finland excels in education and design.',
    'Malaysia blends modernity with tradition.',
    'Thailand attracts millions with its beaches.',
    'Vietnam is famous for its street food.',
    'Singapore is a global financial hub.'
]

# Networks
networks = [
    'Facebook connects people worldwide.',
    'Twitter enables real-time discussions.',
    'Instagram shares visual content globally.',
    'LinkedIn supports professional networking.',
    'Snapchat offers instant photo sharing.',
    'Pinterest inspires creativity and ideas.',
    'Reddit fosters diverse online communities.',
    'TikTok popularizes short video trends.',
    'YouTube hosts millions of videos.',
    'WhatsApp simplifies global communication.',
    'Skype enables video conferencing worldwide.',
    'Zoom revolutionized virtual meetings.',
    'Slack improves workplace collaboration.',
    'Twitch dominates live gaming streams.',
    'Discord connects online gaming communities.',
    'Tumblr blends blogging with social media.',
    'Vimeo showcases high-quality video content.',
    'WeChat integrates messaging and payments.',
    'Telegram offers secure messaging features.',
    'Baidu powers China’s search engine market.',
    'QQ remains a popular Chinese platform.',
    'Yandex dominates Russian online searches.',
    'Flickr stores and shares digital photos.',
    'GitHub fosters open-source collaboration.',
    'Medium provides a platform for writers.'
]

# Sports
sports = [
    'Football is the world’s most popular sport.',
    'Basketball thrives in fast-paced gameplay.',
    'Baseball is America’s favorite pastime.',
    'Soccer excites fans across all continents.',
    'Tennis showcases individual athletic skill.',
    'Golf is a game of precision.',
    'Hockey features intense ice action.',
    'Rugby blends strategy with physicality.',
    'Cricket is beloved in South Asia.',
    'Volleyball dominates beach and indoor courts.',
    'Boxing is the ultimate combat sport.',
    'MMA combines various fighting techniques.',
    'Wrestling dates back to ancient Greece.',
    'Track and field test speed and endurance.',
    'Cycling challenges athletes in long races.',
    'Table tennis requires rapid reflexes.',
    'Badminton is a high-speed racket sport.',
    'Swimming is essential for fitness and competition.',
    'Athletics cover multiple sporting events.',
    'Rowing demands strength and teamwork.',
    'Skiing is a thrilling winter sport.',
    'Snowboarding combines balance and agility.',
    'Gymnastics showcases flexibility and skill.',
    'Skating includes figure and speed variations.',
    'Handball is a fast-paced team sport.',
    'Lacrosse mixes speed with strategy.',
    'Fencing is a sport of precision.',
    'Sailing explores wind-powered navigation.',
    'Water polo is intense aquatic competition.',
    'Equestrian sports highlight horse riding skills.',
    'Archery requires focus and accuracy.',
    'Canoeing is an exciting water sport.',
    'Bobsleigh races on icy tracks.',
    'Curling combines strategy and finesse.'
]

# Food
food = [
    'Pizza is a global favorite dish.',
    'Burgers are an American classic meal.',
    'Tacos bring Mexican flavors to life.',
    'Sushi showcases delicate Japanese cuisine.',
    'Pasta comes in countless delicious varieties.',
    'Steak is loved by meat enthusiasts.',
    'Salad offers a fresh, healthy option.',
    'Soup warms the body and soul.',
    'Desserts satisfy every sweet craving.',
    'Breakfast is the most important meal.',
    'Seafood provides rich ocean flavors.',
    'Vegetarian meals focus on plant-based ingredients.',
    'Vegan dishes eliminate animal products.',
    'Fried chicken is crispy and delicious.',
    'Sandwiches are perfect for quick meals.',
    'Ice cream is a delightful frozen treat.',
    'Biryani is a fragrant rice dish.',
    'Curry is packed with spices and flavors.',
    'Fried rice is a staple in Asia.',
    'Samosas are crispy and flavorful snacks.',
    'Casseroles make hearty family meals.',
    'Wraps offer a convenient meal option.',
    'Shawarma is a Middle Eastern favorite.',
    'Ceviche is a refreshing seafood dish.',
    'Baklava is a sweet layered pastry.',
    'Falafel is a crunchy vegetarian delight.',
    'Paella is Spain’s famous rice dish.',
    'Poutine is a Canadian comfort food.',
    'Dim sum offers small flavorful bites.',
    'Ramen is Japan’s favorite noodle dish.',
    'Kimchi is a spicy fermented side dish.',
    'Chili adds spice to any meal.',
    'Goulash is a hearty Hungarian stew.',
    'Empanadas are stuffed pastry delights.',
    'Tamales are wrapped and steamed treats.',
    'Moussaka is a layered Greek dish.',
    'Kebabs bring grilled meat perfection.',
    'Churros are crispy, sweet street food.'
]

# Movies
movies = [
    'Action movies feature high-energy stunts.',
    'Comedy films bring laughter and joy.',
    'Drama explores deep emotional storytelling.',
    'Horror movies create spine-chilling suspense.',
    'Romance films capture love stories beautifully.',
    'Sci-fi explores futuristic and imaginative worlds.',
    'Thrillers keep audiences on the edge.',
    'Documentaries educate with real-world stories.',
    'Animation brings characters to life creatively.',
    'Musicals blend song with storytelling.',
    'Adventure films take viewers on journeys.',
    'Fantasy movies create magical new worlds.',
    'Mystery films unravel gripping puzzles.',
    'Crime movies depict law and justice.',
    'Historical films portray past events vividly.',
    'Family movies appeal to all ages.',
    'Romantic comedies mix love with humor.',
    'War movies depict intense battle scenes.',
    'Superhero films showcase extraordinary abilities.',
    'Indie films highlight unique storytelling styles.',
    'Noir movies create dark and moody tones.',
    'Western films showcase cowboy adventures.',
    'Biographical films tell real-life stories.',
    'Mockumentaries blend fiction with documentary style.',
    'Experimental films push creative boundaries.',
    'Art house films appeal to niche audiences.',
    'Cult films gain passionate fan followings.',
    'Silent films rely on visual storytelling.',
    'Film noir features suspenseful crime stories.',
    'Action-adventure films combine excitement and thrill.',
    'Fantasy dramas weave magic into narratives.'
]

edge_labels = [
    "Trigger", "Transition", "Process", "Cause", "Effect", "Result",
    "Input", "Output", "Compute", "Store", "Retrieve", "Send",
    "Receive", "Transfer", "Generate", "Enable", "Disable", "Activate",
    "Deactivate", "Approve", "Reject", "Start", "End", "Open", "Close",
    "On", "Off", "Success", "Failure", "Waiting", "Processing",
    "Ready", "Running", "Valid", "Invalid", "Accept", "Decline",
    "Before", "After", "Next", "Previous", "Connect", "Depend",
    "Influence", "Affect", "Extend", "Associate", "Build", "Relate",
    "Example", "Type", "Variation", "Simultaneous", "Delay", "Complete",
    "Require"
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
MAX_NUM_BLOCKS = 2
MIN_NUM_BLOCKS = 1
MAX_NUM_ENTITIES = 3
MIN_NUM_ENTITIES = 2
MAX_NUM_EDGES = 2
MIN_NUM_EDGES = 2
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
code_dir = 'FlowchartHard/MermaidCode/'
image_dir = 'FlowchartHard/MermaidImage/'
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
df.to_json("./FlowchartDiagramDatasetHard.json", orient="records", indent=4)
    
    