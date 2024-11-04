def calculate_scores(recognized_words, fluency_scores, durations, prosody_scores):
    # Calculate accuracy score
    final_accuracy_scores = [
        word.accuracy_score for word in recognized_words if word.error_type != 'Insertion'
    ]
    accuracy_score = sum(final_accuracy_scores) / len(final_accuracy_scores) if final_accuracy_scores else 0

    # Calculate fluency score
    fluency_score = sum([x * y for (x, y) in zip(fluency_scores, durations)]) / sum(durations) if durations else 0

    # Calculate prosody score
    prosody_score = sum(prosody_scores) / len(prosody_scores) if prosody_scores else 0

    # Calculate completeness score
    completeness_score = len(
        [w for w in recognized_words if w.error_type == "None"]
    ) / len(recognized_words) * 100 if recognized_words else 0
    completeness_score = min(completeness_score, 100)  # Cap at 100

    # Calculate overall pronunciation score
    pron_score = accuracy_score * 0.4 + prosody_score * 0.2 + fluency_score * 0.2 + completeness_score * 0.2

    # Return all scores in a dictionary
    return {
        "pronunciation_score": pron_score,
        "accuracy": accuracy_score,
        "fluency": fluency_score,
        "prosody": prosody_score,
        "completeness": completeness_score
    }