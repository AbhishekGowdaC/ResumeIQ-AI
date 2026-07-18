import re

def extract_email(text: str):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match= re.search(pattern, text)
    if match:
        return match.group()
    return None

def extract_phone(text: str):

    pattern = r"(\+91[- ]?)?[6-9]\d{9}"

    match = re.search(pattern, text)
    if match:
        return match.group()
    return None

def extract_name(text: str):
    lines = text.split("\n")

    keywords = [
        "mobile",
        "email",
        "professional summary"
    ]

    for line in lines:
        line = line.strip()

        if line:
            original_line = line
            lower_line = line.lower()

            for keyword in keywords:
                if keyword in lower_line:
                    index = lower_line.index(keyword)
                    return original_line[:index].strip()

            return original_line

    return None

import re

def extract_skills(text: str):

    # Normalize spaces and convert to lowercase
    text = re.sub(r"\s+", " ", text).lower()

    skills_list = [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "OpenCV",
        "Flask",
        "FastAPI",
        "Django",
        "Git",
        "GitHub",
        "Docker",
        "AWS",
        "NLP"
    ]

    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    # Handle C separately
    if re.search(r"(?<!\w)C(?!\w)", text, re.IGNORECASE):
        found_skills.append("C")

    return found_skills
import re

EDUCATION = [
    "Bachelor of Engineering",
    "B.E",
    "B.Tech",
    "Bachelor of Technology",
    "Master of Technology",
    "M.Tech",
    "Bachelor of Science",
    "B.Sc",
    "Master of Science",
    "M.Sc",
    "Bachelor of Computer Applications",
    "BCA",
    "Master of Computer Applications",
    "MCA",
    "MBA",
    "Diploma",
    "PhD"
]

def extract_education(text: str):

    found_education = []

    # Convert multiple spaces/newlines/tabs into a single space
    text = re.sub(r"\s+", " ", text).lower()

    for degree in EDUCATION:

        if degree.lower() in text:
            found_education.append(degree)

    return found_education

def extract_projects(text: str):

    projects = []

    lines = text.split("\n")

    capture = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.lower() in [
            "projects",
            "project",
            "academic projects",
            "personal projects"
        ]:
            capture = True
            continue

        if capture:

            if line.lower() in [
                "education",
                "skills",
                "experience",
                "certifications"
            ]:
                break

            projects.append(line)

    return projects