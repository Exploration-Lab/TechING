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
def class_and_edges(minClasses, maxClasses):
    noClasses = random.randint(minClasses,maxClasses)
    noConnections = 3
    return noClasses, noConnections

# Classes and their respective Attributes
bank_account = ['account_number', 'account_type', 'balance', 'account_holder', 'branch', 'bank', 'ifsc_code', 'branch_code', 'branch_address', 'branch_manager']
customer = ['customer_id', 'customer_name', 'customer_address', 'customer_email', 'customer_phone', 'customer_dob', 'customer']
branch = ['branch_name', 'branch_code', 'branch_address', 'branch_manager', 'branch_phone', 'branch_email', 'branch']
loan = ['loan_id', 'loan_type', 'loan_amount', 'loan_duration', 'loan_interest', 'loan_status', 'loan']
course = ['course_id', 'course_name', 'course_duration', 'course_fee', 'course', 'course_description']
student = ['student_id', 'student_name', 'student_address', 'student_email', 'student_phone', 'student_dob', 'student']
teacher = ['teacher_id', 'teacher_name', 'teacher_address', 'teacher_email', 'teacher_phone', 'teacher_dob', 'teacher']
employee = ['employee_id', 'employee_name', 'employee_address', 'employee_email', 'employee_phone', 'employee_dob', 'employee']
hospital = ['hospital_id', 'hospital_name', 'hospital_address', 'hospital_phone', 'hospital_email', 'hospital']
doctor = ['doctor_id', 'doctor_name', 'doctor_address', 'doctor_phone', 'doctor_email', 'doctor']
patient = ['patient_id', 'patient_name', 'patient_address', 'patient_phone', 'patient_email', 'patient']
appointment = ['appointment_id', 'appointment_date', 'appointment_time', 'appointment_status', 'appointment']
medicine = ['medicine_id', 'medicine_name', 'medicine_price', 'medicine_quantity', 'medicine']
engineering_discipline = ['discipline_id', 'discipline_name', 'discipline_description', 'discipline', 'discipline_duration', 'discipline_fee']
college = ['college_id', 'college_name', 'college_address', 'college_phone', 'college_email', 'college']
professor = ['professor_id', 'professor_name', 'professor_address', 'professor_phone', 'professor_email', 'professor']
network_fields = ['network_id', 'network_name', 'network_description', 'network', 'network_duration', 'network_fee']
network_provider = ['provider_id', 'provider_name', 'provider_address', 'provider_phone', 'provider_email', 'provider']
services = ['service_id', 'service_name', 'service_description', 'service', 'service_duration', 'service_fee']
product = ['product_id', 'product_name', 'product_price', 'product_quantity', 'product']

all_classes = {
    'bank_account': bank_account,
    'customer': customer,
    'branch': branch,
    'loan': loan,
    'course': course,
    'student': student,
    'teacher': teacher,
    'employee': employee,
    'hospital': hospital,
    'doctor': doctor,
    'patient': patient,
    'appointment': appointment,
    'medicine': medicine,
    'engineering_discipline': engineering_discipline,
    'college': college,
    'professor': professor,
    'network_fields': network_fields,
    'network_provider': network_provider,
    'services': services,
    'product': product
}

# Pick block names and return a list
def pick_class_names(noClasses):
    classes = [
        'bank_account', 'customer', 'branch', 'loan', 'course', 'student', 
        'teacher', 'employee', 'hospital', 'doctor', 'patient', 'appointment', 
        'medicine', 'engineering_discipline', 'college', 'professor', 'network_fields', 'network_provider', 
        'services', 'product'
    ]
    classNames = random.sample(classes, noClasses)
    # print(classNames)
    return classNames

# Pick attributes for each class
def pick_attributes_and_methods(classNames):
    final_attributes = defaultdict(list)
    visibility = ['+','-','#','~']
    method_prefixes = ['get_', 'set_','is_', 'has_', 'add_','remove_',
                       'delete_','update_','create_','find_','search_','fetch_',
                       'insert_', 'select_','change_','calculate_','process_',]
    method_suffixes = ['()', '(int)', '(str)', '(float)', '(bool)', '(list)', '(dict)', '(set)', '(tuple)'] 
    for className in classNames:
        numAttributes = random.randint(1, 3)
        numMethods = random.randint(1, 3)
        attribute = random.sample(all_classes[className], numAttributes)
        method = random.sample(all_classes[className], numMethods)
        for att in attribute:
            visibility_type = random.choice(visibility)
            attribute_name = f"{visibility_type}{att}\n"
            final_attributes[className].append(attribute_name)
        for met in method:
            visibility_type = random.choice(visibility)
            method_prefix = random.choice(method_prefixes)
            method_suffix = random.choice(method_suffixes)
            attribute_name = f"{visibility_type}{method_prefix}{met}{method_suffix}\n"
            final_attributes[className].append(attribute_name)
                # print(attribute_name)

            
    # print(final_attributes)   
    return final_attributes

# Connect classes with edges
def connect_classes(noEdges, classNames):
    connections = []
    arrows = ['<|--','--|>','*--','--*',
              'o--','--o','<--','-->',
              '<-->','<..','..>','..|>',
              '<|..']
    # Make one class as root
    root = random.choice(classNames)
    two_arrows = random.sample(arrows,2) 
    # Create a new list excluding the root
    filtered_class_names = [name for name in classNames if name != root]
    diagram_choice = random.choice([0,1,2,3])

    if diagram_choice == 0: # Root --> 3 children
        arrow = random.choice(arrows)
        #Same arrow for all
        for className in filtered_class_names:
            text = f"{root} {arrow} {className}"
            connections.append(text)
            
            
    elif diagram_choice == 1: # Root --> 1 Child --> 2 Grandchild
        text = f"{root} {two_arrows[0]} {filtered_class_names[0]}"
        connections.append(text)
        for className in filtered_class_names[1:]:
            text = f"{filtered_class_names[0]} {two_arrows[1]} {className}"
            connections.append(text)

    else:
        for className in filtered_class_names[:2]: # Root --> 2 Child --> 1 Grandchild
            text = f"{root} {two_arrows[0]} {className}"
            connections.append(text)
        random_class = random.choice(filtered_class_names[:2])
        text = f"{random_class} {two_arrows[1]} {filtered_class_names[2]}"
        connections.append(text)
        
    return connections

# Update the dataset with new rows
def update_dataset(df, image_path, mermaid_code, description):
    new_row = {
        "Image": [image_path],
        "Mermaid Code": [mermaid_code],
        "Description": [description]
    }
    new_row = pd.DataFrame(new_row)

    # Append the new row using concat
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Develop the mermaid code, save it to test file and generate it's mermaid image
def write_mermaid_code(classNames, connections, attributes): 
    # Mermaid syntax as a string
    mermaid_code = f"""---
title: Class Diagram
---
classDiagram
""" 
    for class_name in classNames:
        mermaid_code += f"    class {class_name}{{\n"
        for attribute in attributes[class_name]:
            mermaid_code += f"        {attribute}"
        mermaid_code += f"    }}\n"   
    for connection in connections:
        mermaid_code += f"    {connection}\n"

    return mermaid_code


def save_image_and_code(mermaid_code, counter):
    # File name to save as .mmd
    os.makedirs("MermaidImageMedium", exist_ok=True)
    os.makedirs("MermaidCodeMedium", exist_ok=True)
    # File name to save as .mmd
    code_file_name = f"./MermaidCodeMedium/ClassDiagram{counter}.mmd"
    image_file_name = f"./MermaidImageMedium/ClassDiagram{counter}.png"
    # Saving the string to a file
    with open(code_file_name, "w") as file:
        file.write(mermaid_code)
    command = f"mmdc -i {code_file_name} -o {image_file_name}"
        # Running the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # print(result.stdout)
    
    return image_file_name

def get_blocks_and_edges(mermaid_code):
    classes = defaultdict(lambda: {"attributes": [], "methods": []})
    relationships = []

    lines = mermaid_code.splitlines()
    current_class = None

    for line in lines:
        line = line.strip()

        # Extract class definitions
        class_match = re.match(r'class (\w+)\{', line)
        if class_match:
            current_class = class_match.group(1)
            continue

        # Extract class attributes and methods
        if current_class:
            attribute_match = re.match(r'([~+#-])(\w+)(\((.*?)\))?', line)
            if attribute_match:
                visibility = attribute_match.group(1)
                name = attribute_match.group(2)
                param = attribute_match.group(4)
                if param:  # If it has parameters, it's a method
                    classes[current_class]["methods"].append({
                        "name": name,
                        "visibility": visibility,
                        "parameters": param
                    })
                else:  # Otherwise, it's an attribute
                    classes[current_class]["attributes"].append({
                        "name": name,
                        "visibility": visibility
                    })

        # Extract relationships
        rel_match = re.match(r'(\w+)\s+([.<|>*o-]+)\s+(\w+)', line)
        if rel_match:
            source = rel_match.group(1)
            relationship = rel_match.group(2)
            target = rel_match.group(3)
            relationships.append({"source": source, "relationship": relationship, "target": target})

    # Build the summary
    summary = {
        "classes": classes,
        "relationships": relationships
    }
    return summary

def visibility_type(attribute):
    if attribute['visibility'] == '~':
        return 'protected'
    elif attribute['visibility'] == '+':
        return 'public'
    elif attribute['visibility'] == '-':
        return 'private'
    else:
        return 'package'

def get_relationship_type(relationship):
    if relationship == '--' or relationship == '-->' or relationship == '<--':
        return 'association'
    elif relationship == 'o--' or relationship == '--o':
        return 'aggregation'
    elif relationship == '--|>' or relationship == '<|--':
        return 'inheritance'
    elif relationship == '--*' or relationship == '*--':
        return 'composition'
    elif relationship == '..>' or relationship == '<..':
        return 'dependency'
    elif relationship == '..|>' or relationship == '<|..':
        return 'realization'
    else:
        return 'unknown'

def get_topological_summary(summary):    
    topological_summary = f"""The topological summary of the diagram is as follows:

There are {len(summary['classes'])} classes in the diagram:
"""
    counter = 1
    for block in summary['classes'].keys():
        topological_summary += f"{counter}. '{block}' class with the following attributes and methods:\n"
        for attribute in summary['classes'][block]['attributes']:
            visibility = visibility_type(attribute)
            topological_summary += f"   - {attribute['name']}: {visibility}\n"
        for method in summary['classes'][block]['methods']:
            visibility = visibility_type(method)
            topological_summary += f"   - {method['name']}({method['parameters']}): {visibility}\n"

        counter += 1
    topological_summary += "\nThe relationships between the classes are as follows:\n"
    counter = 1
    for relationship in summary['relationships']:
        rel_type = get_relationship_type(relationship['relationship'])
        if relationship['relationship'][0] == '-' or relationship['relationship'] == '.':
            topological_summary += f"{counter}. Relation from {relationship['source']} to {relationship['target']} of {rel_type}.\n"
            counter += 1
        else:
            topological_summary += f"{counter}. Relation from {relationship['target']} to  {relationship['source']} of {rel_type}.\n"
            counter += 1
    return topological_summary

def generate_dataset_sample():
    noClasses, noConnections = class_and_edges(minClasses=4, maxClasses=4) 
    classNames = pick_class_names(noClasses) 
    attributeDict = pick_attributes_and_methods(classNames)
    connections = connect_classes(noConnections, classNames)
    mermaid_code = write_mermaid_code(classNames, connections, attributeDict)
    return mermaid_code


counter = 0
df = pd.DataFrame(columns=["Image", "Mermaid Code", "Description"])
for _ in tqdm(range(10)):
    mermaid_code = generate_dataset_sample()
    image_path = save_image_and_code(mermaid_code, counter)
    summary = get_blocks_and_edges(mermaid_code)
    topological_summary = get_topological_summary(summary)
    df = update_dataset(df, image_path, mermaid_code, topological_summary)
    counter += 1

df.to_json("./ClassDiagramDatasetMedium.json", orient="records", indent=4)