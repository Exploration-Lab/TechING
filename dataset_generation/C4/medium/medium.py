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

#Setting number of blocks and edges
def class_and_edges(minBlocks, maxBlocks):
    noClasses = random.randint(minBlocks,maxBlocks)
    return noClasses

persons = {
    "Engineer": {"title": "Engineer", "desc": "An engineer of the company", "arrow": "Operates on"},
    "Developer": {"title": "Developer", "desc": "A software developer of the company", "arrow": "Uses"},
    "Programmer": {"title": "Programmer", "desc": "A coder of the company", "arrow": "Programs"},
    "Designer": {"title": "Designer", "desc": "A designer of the textile company", "arrow": "Reviews"},
    "Artist": {"title": "Artist", "desc": "An artist of the association", "arrow": "Uses"},
    "Manager": {"title": "Manager", "desc": "An employee of a company", "arrow": "Reviews"},
    "Director": {"title": "Director", "desc": "The director of the firm", "arrow": "Uses"},
    "CEO": {"title": "CEO", "desc": "The CEO of the company", "arrow": "Uses"},
    "CTO": {"title": "CTO", "desc": "The CTO of the firm", "arrow": "Reviews"},
    "CFO": {"title": "CFO", "desc": "The head of the finance department", "arrow": "Uses"},
    "COO": {"title": "COO", "desc": "The COO of the company", "arrow": "Reviews"},
    "CIO": {"title": "CIO", "desc": "The CIO of the firm", "arrow": "Operates on"},
    "Supervisor": {"title": "Supervisor", "desc": "Supervisor of the project", "arrow": "Uses"},
    "Analyst": {"title": "Analyst", "desc": "Stock Analyst of the firm", "arrow": "Reviews"},
    "Consultant": {"title": "Consultant", "desc": "A freelance consultant", "arrow": "Operates on"},
    "Specialist": {"title": "Specialist", "desc": "External specialist of the company", "arrow": "Reviews"},
    "Technician": {"title": "Technician", "desc": "Any technician on call", "arrow": "Uses"},
    "Administrator": {"title": "Administrator", "desc": "Administrator of the website", "arrow": "Operates on"},
    "Coordinator": {"title": "Coordinator", "desc": "Mediator of the firm", "arrow": "Uses"},
    "Assistant": {"title": "Assistant", "desc": "An assistant to the manager", "arrow": "Reviews"},
    "Customer": {"title": "Customer", "desc": "A customer of the company", "arrow": "Uses"},
    "Representative": {"title": "Representative", "desc": "A representative from the client company", "arrow": "Uses"},
    "Agent": {"title": "Agent", "desc": "An agent of the company", "arrow": "Reviews"},
    "Associate": {"title": "Associate", "desc": "An associate of the legal partner", "arrow": "Operates on"},
    "Operator": {"title": "Operator", "desc": "An operator of the firm", "arrow": "Uses"},
    "Technologist": {"title": "Technologist", "desc": "A freelance technologist hired by the company", "arrow": "Uses"},
    "Professor": {"title": "Professor", "desc": "A professor of the university", "arrow": "Reviews"},
    "Instructor": {"title": "Instructor", "desc": "An instructor of the vocational school", "arrow": "Operates on"},
    "Teacher": {"title": "Teacher", "desc": "A teacher of the school", "arrow": "Uses"},
    "Lecturer": {"title": "Lecturer", "desc": "A lecturer of the college", "arrow": "Reviews"},
    "Researcher": {"title": "Researcher", "desc": "A researcher of the R&D department", "arrow": "Uses"},
    "Scientist": {"title": "Scientist", "desc": "A scientist of the research lab", "arrow": "Operates on"}
}

systems = {"Internet Banking System": {"title": "Internet Banking System", "desc": "A system for online banking", "arrow": "Communicates with"},
           "Shopping System": {"title": "Shopping System", "desc": "An online shopping system", "arrow": "Authenticates with"},
           "Social Media System": {"title": "Social Media System", "desc": "A social media platform", "arrow": "Sends data to"},
           "E-Learning System": {"title": "E-Learning System", "desc": "An online learning platform", "arrow": "Uses"},
           "E-Commerce System": {"title": "E-Commerce System", "desc": "An online commerce platform", "arrow": "Creates request to"},
           "Online Ticketing System": {"title": "Online Ticketing System", "desc": "An online ticketing platform", "arrow": "Communicates with"},
           "Food Delivery System": {"title": "Food Delivery System", "desc": "An online food delivery platform", "arrow": "Authenticates with"},
           "Banking System": {"title": "Banking System", "desc": "A banking system", "arrow": "Sends data to"},
           "Payment System": {"title": "Payment System", "desc": "A payment system", "arrow": "Uses"},
           "Reservation System": {"title": "Reservation System", "desc": "A reservation system", "arrow": "Creates request to"},
           "Booking System": {"title": "Booking System", "desc": "A booking system", "arrow": "Communicates with"},
           "Registration System": {"title": "Registration System", "desc": "A registration system", "arrow": "Authenticates with"},
           "Examination System": {"title": "Examination System", "desc": "An examination system", "arrow": "Sends data to"},
           "Voting System": {"title": "Voting System", "desc": "A voting system", "arrow": "Uses"},
           "Feedback System": {"title": "Feedback System", "desc": "A feedback system", "arrow": "Creates request to"},
           "Survey System": {"title": "Survey System", "desc": "A survey system", "arrow": "Communicates with"},
           "Library System": {"title": "Library System", "desc": "A library system", "arrow": "Authenticates with"},
           "Hotel Booking System": {"title": "Hotel Booking System", "desc": "A hotel booking system", "arrow": "Sends data to"},
           "Flight Booking System": {"title": "Flight Booking System", "desc": "A flight booking system", "arrow": "Uses"},
           "Bus Booking System": {"title": "Bus Booking System", "desc": "A bus booking system", "arrow": "Creates request to"},
           "Car Rental System": {"title": "Car Rental System", "desc": "A car rental system", "arrow": "Communicates with"},
           "Taxi Booking System": {"title": "Taxi Booking System", "desc": "A taxi booking system", "arrow": "Authenticates with"},
           "Event Management System": {"title": "Event Management System", "desc": "An event management system", "arrow": "Sends data to"},
           "Appointment System": {"title": "Appointment System", "desc": "An appointment system", "arrow": "Uses"},
           "Queue Management System": {"title": "Queue Management System", "desc": "A queue management system", "arrow": "Creates request to"},
           "Queue System": {"title": "Queue System", "desc": "A queue system", "arrow": "Communicates with"},
           "Queueing System": {"title": "Queueing System", "desc": "A queueing system", "arrow": "Authenticates with"},
           "API Handling System": {"title": "API Handling System", "desc": "An API handling system", "arrow": "Sends data to"},
           "API System": {"title": "API System", "desc": "An API system", "arrow": "Uses"},
           "API Management System": {"title": "API Management System", "desc": "An API management system", "arrow": "Creates request to"},
           "API Gateway System": {"title": "API Gateway System", "desc": "An API gateway system", "arrow": "Communicates with"},
           "Mainframe System": {"title": "Mainframe System", "desc": "A mainframe system", "arrow": "Authenticates with"},
           "E-mail System": {"title": "E-mail System", "desc": "An e-mail system", "arrow": "Sends data to"},
           "Messaging System": {"title": "Messaging System", "desc": "A messaging system", "arrow": "Uses"},
           "Chat System": {"title": "Chat System", "desc": "A chat system", "arrow": "Creates request to"},
           "Notification System": {"title": "Notification System", "desc": "A notification system", "arrow": "Communicates with"}
}

system_components = ["Frontend",
                        "Backend",
                        "Database",
                        "API",
                        "Server",
                        "Client",
                        "Mobile App",
                        "Web App",
                        "Desktop App",
                        "Cloud",
                        "Mainframe",
                        "Middleware",
                        "Operating System",
                        "Network",
                        "Security",
                        "Storage",
                        "Cache",
                        "Queue",
                        "Queueing System",
                        "Queue Management System",
                        "Queue System",
                        "API Handling System",
                        "API System",
                        "API Management System",
                        "API Gateway System",
                        "Mainframe System",
                        "E-mail System",
                        "Messaging System",
                        "Chat System",
                        "Notification System",
                        "Internet Banking System",
                        "Shopping System",
                        "Social Media System",
                        "E-Learning System",
                        "E-Commerce System",
                        "Onlibe Ticketing System",
                        "Food Delivery System",
                        "Banking System",
                        "Payment System",
                        "Reservation System",
                        "Booking System",
                        "Registration System",
                        "Examination System",
                        "Voting System",
                        "Feedback System",
                        "Survey System",
                        "Library System",
                        "Hotel Booking System",
                        "Flight Booking System",
                        "Bus Booking System",
                        "Car Rental System",
                        "Taxi Booking System",
                        "Event Management System",
                        "Appointment System",
                        "Queue Management System",
                        "Queue System",
                        "Queueing System",
                        "API Handling System",
                        "API System",
                        "API Management System",
                        "API Gateway System",
                        "Mainframe System",
                        "E-mail System",
                        "Messaging System",
                        "Chat System",
                        "Notification System"]

databases = {
  "Customer Database": {"title": "Customer Database", "desc": "Stores customer information", "arrow": "Sends data to"},
  "User Database": {"title": "User Database", "desc": "Stores user information", "arrow": "Sends data to"},
  "Product Database": {"title": "Product Database", "desc": "Stores product information", "arrow": "Sends data to"},
  "Order Database": {"title": "Order Database", "desc": "Stores order information", "arrow": "Sends data to"},
  "Transaction Database": {"title": "Transaction Database", "desc": "Stores transaction information", "arrow": "Sends data to"},
  "Payment Database": {"title": "Payment Database", "desc": "Stores payment information", "arrow": "Sends data to"},
  "Reservation Database": {"title": "Reservation Database", "desc": "Stores reservation information", "arrow": "Sends data to"},
  "Booking Database": {"title": "Booking Database", "desc": "Stores booking information", "arrow": "Sends data to"},
  "Registration Database": {"title": "Registration Database", "desc": "Stores registration information", "arrow": "Sends data to"},
  "Examination Database": {"title": "Examination Database", "desc": "Stores examination information", "arrow": "Sends data to"},
  "Voting Database": {"title": "Voting Database", "desc": "Stores voting information", "arrow": "Sends data to"},
  "Feedback Database": {"title": "Feedback Database", "desc": "Stores feedback information", "arrow": "Sends data to"},
  "Survey Database": {"title": "Survey Database", "desc": "Stores survey information", "arrow": "Sends data to"},
  "Library Database": {"title": "Library Database", "desc": "Stores library information", "arrow": "Sends data to"},
  "Hotel Booking Database": {"title": "Hotel Booking Database", "desc": "Stores hotel booking information", "arrow": "Sends data to"},
  "Flight Booking Database": {"title": "Flight Booking Database", "desc": "Stores flight booking information", "arrow": "Sends data to"},
  "Bus Booking Database": {"title": "Bus Booking Database", "desc": "Stores bus booking information", "arrow": "Sends data to"},
  "Car Rental Database": {"title": "Car Rental Database", "desc": "Stores car rental information", "arrow": "Sends data to"},
  "Taxi Booking Database": {"title": "Taxi Booking Database", "desc": "Stores taxi booking information", "arrow": "Sends data to"},
  "Event Management Database": {"title": "Event Management Database", "desc": "Stores event management information", "arrow": "Sends data to"},
  "Appointment Database": {"title": "Appointment Database", "desc": "Stores appointment information", "arrow": "Sends data to"},
  "Queue Management Database": {"title": "Queue Management Database", "desc": "Stores queue management information", "arrow": "Sends data to"},
  "Queue Database": {"title": "Queue Database", "desc": "Stores queue information", "arrow": "Sends data to"},
  "Queueing Database": {"title": "Queueing Database", "desc": "Stores queueing information", "arrow": "Sends data to"},
  "API Handling Database": {"title": "API Handling Database", "desc": "Stores API handling information", "arrow": "Sends data to"},
  "API Database": {"title": "API Database", "desc": "Stores API information", "arrow": "Sends data to"},
  "API Management Database": {"title": "API Management Database", "desc": "Stores API management information", "arrow": "Sends data to"},
  "API Gateway Database": {"title": "API Gateway Database", "desc": "Stores API gateway information", "arrow": "Sends data to"},
  "Mainframe Database": {"title": "Mainframe Database", "desc": "Stores mainframe information", "arrow": "Sends data to"},
  "E-mail Database": {"title": "E-mail Database", "desc": "Stores e-mail information", "arrow": "Sends data to"},
  "Messaging Database": {"title": "Messaging Database", "desc": "Stores messaging information", "arrow": "Sends data to"},
  "Chat Database": {"title": "Chat Database", "desc": "Stores chat information", "arrow": "Sends data to"},
  "Notification Database": {"title": "Notification Database", "desc": "Stores notification information", "arrow": "Sends data to"},
  "Internet Banking Database": {"title": "Internet Banking Database", "desc": "Stores internet banking information", "arrow": "Sends data to"},
  "Shopping Database": {"title": "Shopping Database", "desc": "Stores shopping information", "arrow": "Sends data to"},
  "Social Media Database": {"title": "Social Media Database", "desc": "Stores social media information", "arrow": "Sends data to"},
  "E-Learning Database": {"title": "E-Learning Database", "desc": "Stores e-learning information", "arrow": "Sends data to"},
  "E-Commerce Database": {"title": "E-Commerce Database", "desc": "Stores e-commerce information", "arrow": "Sends data to"},
  "Online Ticketing Database": {"title": "Online Ticketing Database", "desc": "Stores online ticketing information", "arrow": "Sends data to"},
  "Food Delivery Database": {"title": "Food Delivery Database", "desc": "Stores food delivery information", "arrow": "Sends data to"},
  "Banking Database": {"title": "Banking Database", "desc": "Stores banking information", "arrow": "Sends data to"},
  "Payment Database": {"title": "Payment Database", "desc": "Stores payment information", "arrow": "Sends data to"},
  "Reservation Database": {"title": "Reservation Database", "desc": "Stores reservation information", "arrow": "Sends data to"},
  "Booking Database": {"title": "Booking Database", "desc": "Stores booking information", "arrow": "Sends data to"},
  "Registration Database": {"title": "Registration Database", "desc": "Stores registration information", "arrow": "Sends data to"},
  "Examination Database": {"title": "Examination Database", "desc": "Stores examination information", "arrow": "Sends data to"},
  "Voting Database": {"title": "Voting Database", "desc": "Stores voting information", "arrow": "Sends data to"},
  "Feedback Database": {"title": "Feedback Database", "desc": "Stores feedback information", "arrow": "Sends data to"},
  "Survey Database": {"title": "Survey Database", "desc": "Stores survey information", "arrow": "Sends data to"},
  "Library Database": {"title": "Library Database", "desc": "Stores library information", "arrow": "Sends data to"},
  "Hotel Booking Database": {"title": "Hotel Booking Database", "desc": "Stores hotel booking information", "arrow": "Sends data to"},
  "Flight Booking Database": {"title": "Flight Booking Database", "desc": "Stores flight booking information", "arrow": "Sends data to"},
  "Bus Booking Database": {"title": "Bus Booking Database", "desc": "Stores bus booking information", "arrow": "Sends data to"},
  "Car Rental Database": {"title": "Car Rental Database", "desc": "Stores car rental information", "arrow": "Sends data to"},
  "Taxi Booking Database": {"title": "Taxi Booking Database", "desc": "Stores taxi booking information", "arrow": "Sends data to"},
  "Event Management Database": {"title": "Event Management Database", "desc": "Stores event management information", "arrow": "Sends data to"},
  "Appointment Database": {"title": "Appointment Database", "desc": "Stores appointment information", "arrow": "Sends data to"},
  "Queue Management Database": {"title": "Queue Management Database", "desc": "Stores queue management information", "arrow": "Sends data to"},
  "Queue Database": {"title": "Queue Database", "desc": "Stores queue information", "arrow": "Sends data to"},
  "Queueing Database": {"title": "Queueing Database", "desc": "Stores queueing information", "arrow": "Sends data to"},
  "API Handling Database": {"title": "API Handling Database", "desc": "Stores API handling information", "arrow": "Sends data to"},
  "API Database": {"title": "API Database", "desc": "Stores API information", "arrow": "Sends data to"},
  "API Management Database": {"title": "API Management Database", "desc": "Stores API management information", "arrow": "Sends data to"},
  "API Gateway Database": {"title": "API Gateway Database", "desc": "Stores API gateway information", "arrow": "Sends data to"},
  "Mainframe Database": {"title": "Mainframe Database", "desc": "Stores mainframe information", "arrow": "Sends data to"},
  "E-mail Database": {"title": "E-mail Database", "desc": "Stores e-mail information", "arrow": "Sends data to"},
  "Messaging Database": {"title": "Messaging Database", "desc": "Stores messaging information", "arrow": "Sends data to"},
  "Chat Database": {"title": "Chat Database", "desc": "Stores chat information", "arrow": "Sends data to"},
  "Notification Database": {"title": "Notification Database", "desc": "Stores notification information", "arrow": "Sends data to"}
}
languages = ["Python", "Java", "C++", "C#", "JavaScript", "PHP", "Ruby", "Swift", 
             "Kotlin", "Objective-C", "Go", "Rust", "TypeScript", "Scala", "Perl", 
             "R", "Haskell", "Lua", "Dart", "Julia", "Clojure", "Erlang", "F#", 
             "Groovy", "Racket", "Scheme", "Smalltalk", "Tcl", "Visual Basic", 
             "Assembly", "COBOL", "Fortran", "Lisp", "Pascal", "Ada", "Forth", 
             "Prolog", "Bash", "Shell", "PowerShell", "SQL", "HTML", "CSS", "XML", 
             "JSON", "YAML", "Markdown", "LaTeX", "R Markdown", "Jupyter Notebook", 
             "MATLAB", "Mathematica", "Maple", "LabVIEW", "AutoCAD", "SolidWorks", 
             "SketchUp", "Blender", "Unity", "3ds Max", 
             "ZBrush", "Photoshop", "Illustrator", "InDesign", "Premiere Pro", 
             "After Effects", "Final Cut Pro", "DaVinci Resolve", "Audition", 
             "Logic Pro", "Pro Tools", "Ableton Live", "FL Studio", "GarageBand", 
             "Cubase", "Reason", "Bitwig Studio", "Studio One", "Reaper", "Ardour", 
             "LMMS", "Audacity", "OBS Studio", "Blender", "Unreal Engine", 
             "Maya", "3ds Max", "ZBrush", "Photoshop", "Illustrator", "InDesign", 
             "Premiere Pro", "After Effects", "Final Cut Pro", "DaVinci Resolve", 
             "Audition", "Pro Tools"]

container_components = ["User authentication", "Account Management", "Transaction Processing", "Shopping Cart", "Checkout Process",
            "Sign in Controller", "Sign up Controller", "Sign out Controller", "Profile Controller", "Settings Controller",
            "Accounts Summary Controller", "Transaction History Controller", "Transaction Details Controller", "Transaction Confirmation Controller",
            "Add to Cart Controller", "Remove from Cart Controller", "Update Cart Controller", "Checkout Controller", "Payment Controller",
            "Security Component", "Database Component", "API Component", "Server Component", "Client Component", "Mobile App Component",
            "Application Ready Listener", "Application Started Listener", "Application Failed Listener", "Application Environment Preparer",
            "Script Manager Service", "Script Executor Service", "Script Scheduler Service", "Script Monitor Service", "Script Logger Service",
            "Resource Identifcation", "Resource Allocation", "Resource Management", "Resource Monitoring",
            "Resource Segmentation", "Resource Optimization", "Resource Utilization", "Resource Allocation"
              ]

# Pick block names and return three lists
def pick_class_names(personNo, system1, system2):
    personNames = random.sample(list(persons.keys()), personNo)
    system1Names = []
    system1Names.append(random.choice(list(databases.keys())))
    system1Names.extend(random.sample(list(systems.keys()), system1-1))
    if random.random() < 0.5:
        system2Names = random.sample(list(systems.keys()), system2)
    else:
        system2Names = []
        system2Names.append(random.choice(list(databases.keys())))
        system2Names.extend(random.sample(list(systems.keys()), system2-1))
    # print(classNames)
    return personNames, system1Names, system2Names

# Connect classes with edges
def connect_classes(personNames, system1Names, system2Names):
    connectionPairs = []
    combinedList = personNames + system1Names + system2Names
    combinedsystemList = system1Names + system2Names
    
    
    for person in personNames:
        connectionPairs.append((person, random.choice(system1Names)))
    

    for system in system1Names:
        filteredList = [name for name in system1Names if name != system]
        connectionPairs.append((system, random.choice(filteredList + system2Names)))
    
    randsystem1 = random.choice(system2Names)
    filteredList = [name for name in system2Names if name != randsystem1]
    connectionPairs.append((randsystem1, random.choice(filteredList)))

    return connectionPairs

# Update the dataset with new rows
def update_dataset(df, image_path, mermaid_code, Description):
    new_row = {
        "Image": [image_path],
        "Mermaid Code": [mermaid_code],
        "Description": [Description]
    }
    new_row = pd.DataFrame(new_row)

    # Append the new row using concat
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Develop the mermaid code, save it to test file and generate it's mermaid image
def write_mermaid_code(personNames, system1Names, system2Names, connectionPairs): 
    # Mermaid syntax as a string
    boundaries = 0
    mermaid_code = f"""C4Context

""" 
    # Outer boundary starts
    first_boundary_exists = random.choice([0,1])
    if first_boundary_exists == 1:
        boundaries += 1
        outer_boundary_name = random.choice(["Bank System", "Hospital System", "University System", "Library System", "Retail System"
                                            "Banking System", "Healthcare System", "Education System", "Retail System", "Library System"
                                            "Online Marketing System", "E-commerce System", "Social Media System", "Telecom System", "Transport System",
                                            "Logistics System", "Supply Chain System", "Manufacturing System", "Automobile System", "Aerospace System",
                                            "Defense System", "Government System", "Insurance System", "Real Estate System", "Construction System", "Energy System",
                                            "Oil and Gas System", "Mining System", "Agriculture System", "Food and Beverage System", "Pharmaceutical System"])
        mermaid_code += f"""        Enterprise_Boundary(b{boundaries}, "{outer_boundary_name}") {{\n"""

    # First Module    
    boundaries += 1
    mermaid_code += f"""        Enterprise_Boundary(b{boundaries}, "Personnel Boundary") {{\n"""
    for i in range(len(personNames)):
        mermaid_code += f"""                Person({persons[personNames[i]]["title"].replace(" ", "")}, "{persons[personNames[i]]["title"]}", "{persons[personNames[i]]["desc"]}")\n"""
    mermaid_code += f"""            }}\n"""
    
    # Second Module
    boundaries += 1
    mermaid_code += f"""        Enterprise_Boundary(b{boundaries}, "System Boundary 1") {{\n"""
    for i in range(len(system1Names)):
        if system1Names[i] in databases:
            mermaid_code += f"""                SystemDb({databases[system1Names[i]]["title"].replace(" ", "")}, "{databases[system1Names[i]]["title"]}", "{databases[system1Names[i]]["desc"]}")\n"""
        else:
            mermaid_code += f"""                System({systems[system1Names[i]]["title"].replace(" ", "")}, "{systems[system1Names[i]]["title"]}", "{systems[system1Names[i]]["desc"]}")\n"""    
    mermaid_code += f"""            }}\n"""
    
    # Third Module
    boundaries += 1
    mermaid_code += f"""            Enterprise_Boundary(b{boundaries}, "System Boundary 2") {{\n"""
    for i in range(len(system2Names)):
        if system2Names[i] in databases:
            mermaid_code += f"""            SystemDb({databases[system2Names[i]]["title"].replace(" ", "")}, "{databases[system2Names[i]]["title"]}", "{databases[system2Names[i]]["desc"]}")\n"""
        else:
            mermaid_code += f"""            System({systems[system2Names[i]]["title"].replace(" ", "")}, "{systems[system2Names[i]]["title"]}", "{systems[system2Names[i]]["desc"]}")\n"""    
    mermaid_code += f"""        }}\n"""
   
    if first_boundary_exists == 1:
    # Outer boundary ends here
        mermaid_code += f"""    }}\n"""

    # Connections
    counter = 0
    total_connections = len(personNames) + len(system1Names) + len(system2Names)
    for person in personNames:
        mermaid_code += f"""    Rel({person.replace(" ", "")}, {connectionPairs[counter][1].replace(" ", "")}, "{persons[person]["arrow"]}")\n"""
        counter += 1
    for system in system1Names:
        if system in databases:
            mermaid_code += f"""    Rel({system.replace(" ", "")}, {connectionPairs[counter][1].replace(" ", "")}, "{databases[system]["arrow"]}")\n"""
            counter += 1
        else:
            mermaid_code += f"""    Rel({system.replace(" ", "")}, {connectionPairs[counter][1].replace(" ", "")}, "{systems[system]["arrow"]}")\n"""
            counter += 1
    system = connectionPairs[counter][0]
    if system in databases:
        mermaid_code += f"""    Rel({system.replace(" ", "")}, {connectionPairs[counter][1].replace(" ", "")}, "{databases[system]["arrow"]}")\n"""
        counter += 1
    else:
        mermaid_code += f"""    Rel({system.replace(" ", "")}, {connectionPairs[counter][1].replace(" ", "")}, "{systems[system]["arrow"]}")\n"""
        counter += 1

    mermaid_code += """ UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="3")"""

    return mermaid_code, boundaries

def save_image_and_code(mermaid_code, counter):
    # File name to save as .mmd
    os.makedirs("MermaidImageMedium", exist_ok=True)
    os.makedirs("MermaidCodeMedium", exist_ok=True)
    # File name to save as .mmd
    code_file_name = f"./MermaidCodeMedium/C4Diagram{counter}.mmd"
    image_file_name = f"./MermaidImageMedium/C4Diagram{counter}.png"
    # Saving the string to a file
    with open(code_file_name, "w") as file:
        file.write(mermaid_code)
    command = f"mmdc -i {code_file_name} -o {image_file_name}"
        # Running the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # print(result.stdout)
    
    return image_file_name

def get_blocks_and_edges(mermaid_code):
    summary = {"nodes": [], "relationships": []}
    
    lines = mermaid_code.splitlines()
    
    for line in lines:
        line = line.strip()
        
        # Extract nodes
        if line.startswith("Person(") or line.startswith("System(") or line.startswith("SystemDb(") or line.startswith("Container("):
            # Extract the part inside the parentheses
            content = line.split("(")[1].rstrip(")")

            # Split the extracted string by commas and strip quotes and spaces
            values = [val.strip().strip('"') for val in content.split(",")]
            summary["nodes"].append({"type": values[0], "name": values[1], "details": values[2]})
            
        
        # Extract relationships
        elif line.startswith("Rel("):
            # Extract the part inside the parentheses
            content = line.split("(")[1].rstrip(")")

            # Split the extracted string by commas and strip quotes and spaces
            values = [val.strip().strip('"') for val in content.split(",")]
            summary["relationships"].append({"source": values[0], "target": values[1], "relationship": values[2]})
    
    return summary

def get_topological_summary(summary):    
    topological_summary = f"""The topological summary of the diagram is as follows:

There are {len(summary['nodes'])} entities in the diagram:
"""
    counter = 1
    for block in summary['nodes']:
        topological_summary += f"{counter}. {block['name']}\n"
        counter += 1
    topological_summary += "\nThe relationships between the entities are as follows:\n"
    counter = 1
    for edge in summary['relationships']:
        source = edge['source']
        target = edge['target']
        source = re.sub(r'([a-z])([A-Z])', r'\1 \2', source)
        target = re.sub(r'([a-z])([A-Z])', r'\1 \2', target)
        topological_summary += f"{counter}. Relation from '{source}' to '{target}' with edge label '{edge['relationship']}'.\n"
        counter += 1
    return topological_summary

def generate_dataset_sample():
    person= class_and_edges(minBlocks=1, maxBlocks=2) 
    sysem1= class_and_edges(minBlocks=2, maxBlocks=2) 
    system2= class_and_edges(minBlocks=2, maxBlocks=2)
    personNames, system1Names, system2Names = pick_class_names(person, sysem1, system2)
    connectionPairs = connect_classes(personNames, system1Names, system2Names)
    mermaid_code, boundaries = write_mermaid_code(personNames, system1Names, system2Names, connectionPairs)
    
    return mermaid_code

counter = 0
df = pd.DataFrame(columns=["Image", "Mermaid Code", "Description"])
for _ in tqdm(range(2)):
    mermaid_code = generate_dataset_sample()
    image_path = save_image_and_code(mermaid_code, counter)
    summary = get_blocks_and_edges(mermaid_code)
    topological_summary = get_topological_summary(summary)
    df = update_dataset(df, image_path, mermaid_code, topological_summary)
    counter += 1

df.to_json("./C4DiagramDatasetMedium.json", orient="records", indent=4)              