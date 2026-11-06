# Day 5: Evaluation of the AI Knowledge Assistant

## 1. Objective

The objective of Day 5 was to evaluate the AI Knowledge Assistant's retrieval and answer-generation performance. The evaluation focused on whether the system could retrieve relevant information from the knowledge base, answer questions using the retrieved passages, and reject questions that were outside the scope of the available documents.

## 2. Evaluation Dataset

A test dataset containing 25 questions was created using the Python documentation collected during Day 2.

The dataset included:
- 20 answerable questions related to Python programming.
- 5 unanswerable questions unrelated to the available documentation.

Each test question included an expected answerability label, expected source document, and expected keywords to help evaluate retrieval performance.

## 3. Evaluation Methodology

The evaluation was performed using the following steps:

1. Each question was submitted to the knowledge assistant.
2. The system generated an embedding for the question.
3. The retrieval system searched the local vector database for relevant passages.
4. The top matching passages were checked against the expected source document and keywords.
5. The local LLM generated an answer using the retrieved passages.
6. The results were saved in a CSV file for review.

Retrieval performance was evaluated automatically. Generated answers were marked for manual review because keyword matching alone cannot establish whether an answer is factually correct or supported by its sources.

## 4. Evaluation Results

### Retrieval Performance

| Evaluation Metric | Result |
|---|---:|
| Total test questions | 25 |
| Answerable questions | 20 |
| Unanswerable questions | 5 |
| Answerable questions retrieved correctly | 15/20 |
| Answerable retrieval pass rate | 75% |
| Unanswerable questions rejected correctly | 5/5 |
| Unanswerable rejection rate | 100% |
| Overall automated retrieval checks passed | 20/25 |
| Overall retrieval check pass rate | 80% |

### Interpretation

The system successfully retrieved the expected source and relevant keywords for 15 out of 20 answerable questions.

It also correctly rejected all 5 unanswerable questions using the configured similarity threshold.

The overall automated retrieval check pass rate was 80%.

These results measure retrieval checks, not overall answer accuracy. Answer support was not yet formally scored because the evaluation CSV marked generated answers as REVIEW.

## 5. Issues Identified

The evaluation revealed several areas for improvement.

### A. Source Document Name Mismatches

Some expected source filenames did not match the filenames returned by the retrieval system.

Examples included:
- Exception handling documentation.
- Virtual environment documentation.

These inconsistencies caused some retrieval checks to fail even when the correct document appeared in the retrieved results.

### B. Retrieval of Relevant Passages

Some questions retrieved passages from the expected document but did not pass the automated keyword check.

For example, the question about the difference between `/` and `//` retrieved passages from the Python Introduction document, but the generated answer incorrectly stated that the documentation did not contain the required information.

This suggests that the retrieved passages and the LLM's interpretation of those passages need further investigation.

### C. Answer Generation Issues

Manual review of generated answers identified examples of incorrect or unsupported statements.

Examples included:
- Incorrect explanation of the `pow()` function.
- Incorrect explanation of the return value of `list.pop()`.
- Incorrect explanation of the `list.append()` method.
- Incorrect example of creating a set.
- Inaccurate description of virtual environment creation.

These issues indicate that retrieval success does not automatically guarantee answer correctness.

## 6. Latest QA Assistant Test

The QA assistant was tested again after modifying `src/qa.py` to address the blank-answer issue.

Test question:

"What is the difference between / and // in Python?"

Observed results:
- The system retrieved five passages.
- The local LLM generated a non-empty response.
- Source references were displayed with document names, source IDs, similarity scores, and URLs.
- The generated answer incorrectly stated that the retrieved documentation did not contain enough information to answer the question.

This confirms that the blank-answer issue appears to be resolved, although answer quality and evidence interpretation still need improvement.

## 7. Improvements Planned

The following improvements were identified:

1. Standardize source document names between the evaluation dataset and the processed knowledge base.
2. Investigate questions where relevant documents are retrieved but the automated retrieval checks fail.
3. Review retrieved passages to determine whether they contain the information needed to answer each question.
4. Improve the LLM prompt to require every factual claim to be supported by retrieved evidence.
5. Prevent the assistant from introducing unsupported examples or external information.
6. Include retrieved passage text in the evaluation output to make manual review easier.
7. Re-run the evaluation after improvements and compare the results with the original baseline.
8. Manually review generated answers and classify answer support as YES, PARTIAL, NO, or N/A.

## 8. Limitations

- The evaluation dataset contains only 25 questions.
- Retrieval performance was evaluated using expected source names and keywords.
- The automated retrieval checks do not measure semantic correctness completely.
- Generated answer support has not yet been formally scored.
- The local LLM may generate incorrect or unsupported information even when relevant passages are retrieved.
- The evaluation is limited to the Python documentation currently available in the knowledge base.

## 9. Conclusion

Day 5 successfully established an initial evaluation process for the AI Knowledge Assistant.

The system achieved an 80% overall automated retrieval check pass rate, with a 75% pass rate for answerable questions and a 100% rejection rate for unanswerable questions.

The evaluation also identified inconsistencies in source document naming, retrieval limitations, and answer-generation errors.

The next improvement phase will focus on strengthening evidence-based answer generation, investigating retrieval failures, and conducting manual answer-support evaluation.

**Day 5 Deliverable:** An evaluation dataset containing 25 questions, an automated evaluation script, a CSV results file, and an initial evaluation report.