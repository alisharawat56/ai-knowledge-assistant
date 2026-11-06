
import csv
import json
from pathlib import Path

import requests

from src.search import retrieve_documents
from src.qa import generate_answer


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "evaluation_questions.jsonl"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "evaluation_results.csv"
)


def load_questions():
    questions = []

    with open(DATASET_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                questions.append(json.loads(line))

    return questions


def check_retrieval(question, retrieved_chunks):
    """
    Check whether retrieval found the expected source
    and at least one expected term.
    """

    if not question["answerable"]:
        # An unanswerable question passes if no chunks
        # were returned above the retrieval threshold.
        return len(retrieved_chunks) == 0

    expected_source = question["expected_source"]
    expected_terms = question["expected_terms"]

    for chunk in retrieved_chunks:
        source_matches = (
            chunk["document_name"].lower()
            == expected_source.lower()
        )

        passage = chunk["text"].lower()

        term_matches = any(
            term.lower() in passage
            for term in expected_terms
        )

        if source_matches and term_matches:
            return True

    return False


def evaluate_question(question):
    print(f"\nRunning {question['id']}: {question['question']}")

    result = {
        "id": question["id"],
        "question": question["question"],
        "expected_answerable": question["answerable"],
        "expected_source": question["expected_source"],
        "retrieved_sources": "",
        "retrieved_chunk_ids": "",
        "top_similarity": "",
        "retrieval_pass": False,
        "generated_answer": "",
        "answer_supported": "REVIEW",
        "review_notes": ""
    }

    try:
        retrieved_chunks, all_results = retrieve_documents(
            question["question"]
        )

        result["retrieved_sources"] = "; ".join(
            sorted({
                chunk["document_name"]
                for chunk in retrieved_chunks
            })
        )

        result["retrieved_chunk_ids"] = "; ".join(
            chunk["chunk_id"]
            for chunk in retrieved_chunks
        )

        if all_results:
            result["top_similarity"] = round(
                all_results[0]["score"], 3
            )

        result["retrieval_pass"] = check_retrieval(
            question,
            retrieved_chunks
        )

        if retrieved_chunks:
            result["generated_answer"] = generate_answer(
                question["question"],
                retrieved_chunks
            )

        else:
            result["generated_answer"] = (
                "No answer generated: no sufficiently "
                "relevant passages were retrieved."
            )

        print(
            "Retrieval:",
            "PASS" if result["retrieval_pass"] else "FAIL"
        )

    except (requests.RequestException, ValueError, KeyError) as error:
        result["review_notes"] = f"ERROR: {error}"
        print(f"ERROR: {error}")

    except Exception as error:
        result["review_notes"] = f"ERROR: {error}"
        print(f"ERROR: {error}")

    return result


def main():
    questions = load_questions()

    print("=" * 70)
    print("AI KNOWLEDGE ASSISTANT - EVALUATION")
    print("=" * 70)
    print(f"Questions to evaluate: {len(questions)}")

    results = []

    for question in questions:
        results.append(evaluate_question(question))

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "id",
        "question",
        "expected_answerable",
        "expected_source",
        "retrieved_sources",
        "retrieved_chunk_ids",
        "top_similarity",
        "retrieval_pass",
        "generated_answer",
        "answer_supported",
        "review_notes"
    ]

    with open(
        RESULTS_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(results)

    answerable_results = [
        result for result in results
        if result["expected_answerable"]
    ]

    unanswerable_results = [
        result for result in results
        if not result["expected_answerable"]
    ]

    answerable_passes = sum(
        result["retrieval_pass"]
        for result in answerable_results
    )

    unanswerable_passes = sum(
        result["retrieval_pass"]
        for result in unanswerable_results
    )

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Answerable questions retrieved correctly: "
        f"{answerable_passes}/{len(answerable_results)}"
    )

    print(
        f"Unanswerable questions correctly rejected: "
        f"{unanswerable_passes}/{len(unanswerable_results)}"
    )

    total_passes = answerable_passes + unanswerable_passes

    print(
        f"Retrieval evaluation passes: "
        f"{total_passes}/{len(results)}"
    )

    print(f"\nResults saved to: {RESULTS_FILE}")

    print(
        "\nIMPORTANT: Generated answers still need manual "
        "support review in the CSV."
    )


if __name__ == "__main__":
    main()
