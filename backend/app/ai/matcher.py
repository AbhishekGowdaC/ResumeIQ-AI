def match_skills(
        resume_skills: list,
        job_skills: list
):
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    matched = resume_set.intersection(job_set)
    missing = job_set - resume_set
    if len(job_set) == 0:
        score = 0

    else:
        score = round(
            len(matched)/len(job_set) *100,
            2
        )
    return {
        "score": score,
        "matched": list(matched),
        "missing": list(missing)
    }