
import re


REQUIRED_FIELDS = {
    "answer",
    "sources",
    "insufficient_evidence",
    "limitations",
}


def validate_response(response, retrieved_sources):
    """
    Validate the response structure and make sure every displayed
    source corresponds to a document returned by retrieval.

    Returns (is_valid, errors).
    """
    errors = []

    if not isinstance(response, dict):
        return False, ["Response must be a dictionary."]

    missing_fields = REQUIRED_FIELDS - set(response.keys())
    if missing_fields:
        errors.append(
            f"Missing required fields: {', '.join(sorted(missing_fields))}"
        )

    if errors:
        return False, errors

    if not isinstance(response["answer"], str) or not response["answer"].strip():
        errors.append("Answer must be a non-empty string.")

    if not isinstance(response["sources"], list):
        errors.append("Sources must be a list.")

    if not isinstance(response["insufficient_evidence"], bool):
        errors.append("insufficient_evidence must be True or False.")

    if not isinstance(response["limitations"], list):
        errors.append("Limitations must be a list.")

    if errors:
        return False, errors

    # Build a set of source identities from the actual retrieval results.
    retrieved_ids = {
        (str(source.get("chunk_id")), str(source.get("document_name")))
        for source in retrieved_sources
        if isinstance(source, dict)
        and source.get("chunk_id") is not None
        and source.get("document_name")
    }

    displayed_labels = set()

    for source in response["sources"]:
        if not isinstance(source, dict):
            errors.append("Each source must be a dictionary.")
            continue

        for field in ("source_label", "document_name", "title", "text", "chunk_id"):
            if not source.get(field):
                errors.append(f"A source is missing its {field} field.")

        label = source.get("source_label")
        if label:
            if label in displayed_labels:
                errors.append(f"Duplicate source label: {label}")
            displayed_labels.add(label)

        identity = (
            str(source.get("chunk_id")),
            str(source.get("document_name")),
        )

        if identity not in retrieved_ids:
            errors.append(
                f"Source {label or '(unlabelled)'} does not match a retrieved document."
            )

    if response["insufficient_evidence"] and response["sources"]:
        errors.append(
            "An insufficient-evidence response should not display supporting sources."
        )

    # Check that every [S1], [S2], etc. citation in the answer exists.
    cited_labels = set(re.findall(r"\[(S\d+)\]", response["answer"]))
    invalid_citations = cited_labels - displayed_labels

    if invalid_citations:
        errors.append(
            "Answer contains citations that are not in the displayed sources: "
            + ", ".join(sorted(invalid_citations))
        )

    return len(errors) == 0, errors
