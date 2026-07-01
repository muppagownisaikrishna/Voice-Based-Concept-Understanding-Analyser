def calculate_score(similarity):

    score = similarity * 100

    if score >= 80:
        grade = "Excellent"

    elif score >= 60:
        grade = "Good"

    elif score >= 40:
        grade = "Average"

    else:
        grade = "Poor"

    return round(score,2), grade