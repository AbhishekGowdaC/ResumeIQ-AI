def get_match_level(score):

    if score >= 90:
        return "Excellent Match"

    elif score >= 75:
        return "Strong Match"

    elif score >= 60:
        return "Good Match"

    elif score >= 40:
        return "Average Match"

    else:
        return "Poor Match"
def get_strengths(matched_skills : list):

    strenghts = []

    for skill in matched_skills:
        strenghts.append(
            f"Strong Knowledge of {skill}"
        )
    
    return strenghts

def get_recommendations(missing_skills: list):
    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Consider learning {skill}"
        )
    return recommendations

