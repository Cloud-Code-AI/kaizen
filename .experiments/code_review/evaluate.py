import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def calculate_similarity(str1, str2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([str1, str2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


def compare_issues(ground_truth, model_issues):
    matched = []
    unmatched_ground_truth = []
    unmatched_model = []

    for gt_issue in ground_truth:
        found_match = False
        for model_issue in model_issues:
            description_similarity = calculate_similarity(
                gt_issue["description"], model_issue["description"]
            )
            if (
                description_similarity > 0.1
                and gt_issue["file_path"] == model_issue["file_path"]
                and abs(
                    int(gt_issue.get("start_line", 0))
                    - int(model_issue.get("start_line", -10))
                )
                <= 1
                and abs(
                    int(gt_issue.get("end_line", 0))
                    - int(model_issue.get("end_line", -10))
                )
                <= 1
                and abs(
                    int(gt_issue.get("severity", 0))
                    - int(model_issue.get("severity", -10))
                )
                <= 1
            ):
                matched.append((gt_issue, model_issue))
                found_match = True
                break

        if not found_match:
            unmatched_ground_truth.append(gt_issue)

    for model_issue in model_issues:
        if not any(model_issue in pair for pair in matched):
            unmatched_model.append(model_issue)

    return matched, unmatched_ground_truth, unmatched_model


def evaluate_model(ground_truth, model_issues):
    matched, unmatched_gt, unmatched_model = compare_issues(ground_truth, model_issues)

    total_issues = len(ground_truth)
    issues_found = len(model_issues)
    correct_issues = len(matched)
    false_negatives = len(unmatched_gt)
    false_positives = len(unmatched_model)

    recall = correct_issues / total_issues if total_issues > 0 else 0
    precision = correct_issues / issues_found if issues_found > 0 else 0
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return {
        "total_issues": total_issues,
        "issues_found": issues_found,
        "correct_issues": correct_issues,
        "false_negatives": false_negatives,
        "false_positives": false_positives,
        "recall": recall,
        "precision": precision,
        "f1_score": f1_score,
    }


def main(folder_name):
    dataset_path = ".experiments/code_review/dataset"
    model_base_path = os.path.join(
        ".experiments", "code_review", folder_name, "no_eval"
    )

    overall_results = {
        "total_issues": 0,
        "correct_issues": 0,
        "false_negatives": 0,
        "false_positives": 0,
    }

    pr_count = 0

    for pr_folder in os.listdir(dataset_path):
        if pr_folder.startswith("pr_"):
            pr_number = pr_folder.split("_")[1]
            ground_truth_path = os.path.join(dataset_path, pr_folder, "issues.json")
            model_path = os.path.join(model_base_path, f"pr_{pr_number}", "issues.json")

            if not os.path.exists(ground_truth_path) or not os.path.exists(model_path):
                print(f"Skipping PR {pr_number} due to missing files")
                continue

            ground_truth = load_json(ground_truth_path)
            model_issues = load_json(model_path)

            results = evaluate_model(ground_truth, model_issues)

            print(f"\nEvaluation Results for {folder_name} on PR {pr_number}:")
            print(f"  Issues Found: {results['issues_found']}")
            print(
                f"  Correct issues: {results['correct_issues']}/{results['total_issues']}"
            )
            print(f"  False negatives: {results['false_negatives']}")
            print(f"  False positives: {results['false_positives']}")
            print(f"  Recall: {results['recall']:.2f}")
            print(f"  Precision: {results['precision']:.2f}")
            print(f"  F1 Score: {results['f1_score']:.2f}")

            for key in [
                "total_issues",
                "correct_issues",
                "false_negatives",
                "false_positives",
            ]:
                overall_results[key] += results[key]

            pr_count += 1

    if pr_count > 0:
        overall_recall = (
            overall_results["correct_issues"] / overall_results["total_issues"]
        )
        overall_precision = overall_results["correct_issues"] / (
            overall_results["correct_issues"] + overall_results["false_positives"]
        )
        overall_f1 = (
            2
            * (overall_precision * overall_recall)
            / (overall_precision + overall_recall)
            if (overall_precision + overall_recall) > 0
            else 0
        )

        print(f"\nOverall Results for {folder_name}:")
        print(f"  Total PRs evaluated: {pr_count}")
        print(
            f"  Correct issues: {overall_results['correct_issues']}/{overall_results['total_issues']}"
        )
        print(f"  False negatives: {overall_results['false_negatives']}")
        print(f"  False positives: {overall_results['false_positives']}")
        print(f"  Recall: {overall_recall:.2f}")
        print(f"  Precision: {overall_precision:.2f}")
        print(f"  F1 Score: {overall_f1:.2f}")
    else:
        print(f"No valid PRs found for evaluation of {folder_name}")


if __name__ == "__main__":
    folder_name = input("Enter the model name (e.g., gpt-4o): ")
    main(folder_name)
