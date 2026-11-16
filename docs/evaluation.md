
# Evaluation Results

## Evaluation Dataset

The initial evaluation used 25 questions:

- 20 answerable questions about Python documentation
- 5 unanswerable questions outside the knowledge base

The evaluation checked whether relevant documents were retrieved and whether unsupported questions were rejected.

## Baseline Results

| Metric | Result |
|---|---:|
| Answerable questions passing retrieval checks | 15/20 |
| Answerable retrieval pass rate | 75% |
| Unsupported questions correctly rejected | 5/5 |
| Unsupported rejection rate | 100% |
| Overall automated retrieval checks passed | 20/25 |
| Overall retrieval check pass rate | 80% |

## Interpretation

The initial retrieval system passed 75% of the answerable-question checks and correctly rejected all five unsupported questions.

The results demonstrate that the application can retrieve relevant documentation and recognize some questions outside its knowledge base.

However, the 80% overall score measures automated retrieval checks. It does not represent overall answer accuracy or factual correctness.

Answer support was marked REVIEW in the original evaluation output, so a reliable answer-grounding accuracy score was not established.

## Observed Failure Cases

1. Some questions retrieved an unexpected document because expected filenames did not match the actual filenames.
2. Some relevant passages were not ranked highly enough.
3. Some generated answers contained incorrect or contradictory Python explanations.
4. Similarity scores alone did not guarantee that retrieved content supported the generated answer.

## Future Improvements

- Improve document coverage and metadata consistency.
- Tune chunking and retrieval settings.
- Capture retrieved passages in evaluation output.
- Manually assess answer support using YES, PARTIAL, NO, and N/A.
- Expand the evaluation dataset.
- Compare retrieval configurations using the same dataset.
