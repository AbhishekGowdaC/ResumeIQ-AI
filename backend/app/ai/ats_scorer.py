def calculate_ats_score(
    skill_score: float,
    education_score: float,
    project_score: float,
    keyword_score: float
):
    final_score = (
        skill_score * 0.60
        + education_score * 0.15
        + project_score * 0.15
        + keyword_score * 0.10
    )

    return round(final_score, 2)

def calculate_education_score(
    resume_education: str,
    job_description: str
):
    if not resume_education:
        return 0

    resume_text = resume_education.lower()
    job_text = job_description.lower()

    degree_groups = {
        "bachelor": [
            "bachelor",
            "b.e",
            "b.tech",
            "be ",
            "btech"
        ],
        "master": [
            "master",
            "m.e",
            "m.tech",
            "mtech"
        ],
        "phd": [
            "phd",
            "doctorate"
        ]
    }

    for degree, keywords in degree_groups.items():

        job_requires_degree = any(
            keyword in job_text
            for keyword in keywords
        )

        if job_requires_degree:

            resume_has_degree = any(
                keyword in resume_text
                for keyword in keywords
            )

            if resume_has_degree:
                return 100

            return 0

    return 100

def calculate_project_score(
    resume_projects: str,
    job_skills: list
):
    if not resume_projects or not job_skills:
        return 0

    project_text = resume_projects.lower()

    matched_skills = []

    for skill in job_skills:
        if skill.lower() in project_text:
            matched_skills.append(skill)

    score = (
        len(matched_skills)
        / len(job_skills)
    ) * 100

    return round(score, 2)

def calculate_keyword_score(
    resume_text: str,
    job_skills: list
):
    if not resume_text or not job_skills:
        return 0

    resume_text = resume_text.lower()

    matched_keywords = []

    for skill in job_skills:
        if skill.lower() in resume_text:
            matched_keywords.append(skill)

    score = (
        len(matched_keywords)
        / len(job_skills)
    ) * 100

    return round(score, 2)