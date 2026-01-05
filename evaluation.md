## LLM Backend Comparison

The system was evaluated using two LLM backends on the same retrieval results.

### Local LLM
- Produces grounded answers
- Often extracts text verbatim from sources
- Limited explanation depth
- Suitable for offline and zero-cost usage

### API-based LLaMA-3.1-8B-Instant
- Produces clearer, more structured explanations
- Better synthesis of retrieved context
- Improved reasoning and readability
- Requires internet access and API key

### Key Observation
Retrieval quality remained identical across both backends.
Differences in answer quality are entirely due to the LLM used,
demonstrating clean separation between retrieval and generation.
