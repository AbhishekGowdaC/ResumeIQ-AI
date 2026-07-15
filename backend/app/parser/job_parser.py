from app.parser.resume_parser import extract_text_from_pdf
from app.parser.info_parser import extract_skills
def extract_job_title(text: str):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if line:

            return line

    return None