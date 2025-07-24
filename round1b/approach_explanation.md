## Round 1B Approach

We split PDFs into sections and embed them using MiniLM. Then we compute semantic similarity with a given persona and job-to-be-done, rank the top 10 sections, and output structured metadata.
