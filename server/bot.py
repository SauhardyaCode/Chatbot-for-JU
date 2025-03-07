import os
import json

# Function to load data from a JSON file
def load_json_data(file_path):
    try:
        with open(file_path, 'r',encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading file {file_path}: {str(e)}")
        return None

# Function to search for a syllabus based on the subject
def search_syllabus(query):
    # Normalize the query to lowercase for easier matching
    query = query.lower()

    # List all faculties
    faculties = ['arts', 'science', 'engineering-technology', 'interdisciplinary-studies-law-and-management']
    matched_subjects = []

    # Iterate over all faculties to search for matching subjects
    for faculty in faculties:
        faculty_path = f"../xtracter/data/syllabus/{faculty}"
        
        # Check if the faculty folder exists
        if os.path.exists(faculty_path):
            for subject_folder in os.listdir(faculty_path):
                subject_path = f"{faculty_path}/{subject_folder}"
                
                # If the subject folder name contains the query, we consider it a match
                if query in subject_folder.lower():
                    about_file = f"{subject_path}/about.json"
                    courses_file = f"{subject_path}/courses.json"
                    
                    # Load the subject data
                    about_data = load_json_data(about_file)
                    courses_data = load_json_data(courses_file)
                    
                    if about_data and courses_data:
                        matched_subjects.append({
                            'faculty': faculty.capitalize(),
                            'subject': subject_folder,
                            'about': about_data,
                            'courses': courses_data
                        })

    # If we found any matches, format them into a string
    if matched_subjects:
        response = "Here are the results for your query:\n"
        print(response)
        for subject in matched_subjects:
            response += f"\nFaculty: {subject['faculty']}\n"
            response += f"Subject: {subject['subject'].replace('-', ' ').title()}\n"
            response += f"About: {subject['about']['description']}\n"
            # response += f"Courses Offered: {', '.join(subject['courses'])}\n"
            response += "-" * 50  # Separator line between different subjects

        return response.strip()  # Return the string response

    # If no match is found, return an error message as a string
    return "Sorry, no matching subjects found. Please try again with a more specific query."
