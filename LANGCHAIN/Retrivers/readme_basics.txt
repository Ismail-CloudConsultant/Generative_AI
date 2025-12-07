A retriver is a component that fetches relevent documents from a datasource - vector store/vector data base in responce to user query
all retrivers are langchain runnables
there are multiple types of retrivers



wikipedia retriver?
vector store retriver?

wht do we use retrivers if we can do the same with vectorstore.similarity score?


1. Vector Store Retriever
What is it?
A retriever that finds the most semantically similar documents using embeddings.
Backed by vector databases (Faiss, Chroma, Pinecone, Weaviate, etc.).

Problem it solves
Exact keyword search fails when queries use different wording.
Helps LLMs access relevant context for QA, chatbots, RAG systems.

How it works
Stores embeddings of documents as vectors.
Converts the query to an embedding.
Performs similarity search using cosine / dot-product / Euclidean distance.
Returns top-k most similar documents.

When to use
Standard RAG systems.
Semantic search.
Knowledge bases where synonyms/paraphrases matter.
High recall is acceptable; redundancy is fine.
------------------------------------------------------------------------------------------------
MMR Retriever (Maximal Marginal Relevance Retriever)
What is it?
A retriever that balances relevance and diversity among returned documents.

Problem it solves
Vanilla vector search returns many near-identical chunks.
Important context from other areas gets ignored.

How it works
Ranks documents using:
MMR = λ * similarity(query, doc) – (1 - λ) * similarity(doc, selected_docs)
Ensures each result is relevant AND not redundant.

When to use
When your vector search returns duplicates.
Long documents with repetitive sections.
Need to cover diverse subtopics of a query.
------------------------------------------------------------------------------------------------
3. MQR — Multi-Query Retriever
What is it?
A retriever that expands a single user query into multiple paraphrased queries using an LLM, then searches with all of them.

Problem it solves
Single-query vector search misses relevant chunks due to narrow phrasing.
Improves recall when queries are ambiguous or incomplete.

How it works
LLM generates 3–10 alternate versions of the query.
Each query performs vector search.
Combine all returned documents and deduplicate.

When to use
When retrieval quality is low due to poor user queries.
Complex questions with multiple sub-intent.
RAG systems needing higher recall than standard retrievers.
------------------------------------------------------------------------------------------------
4. CCR — Contextual Compression Retriever
What is it?

A retriever that compresses or filters documents using an LLM or embedding model BEFORE returning them to the final LLM.

Problem it solves
Long retrieved documents cause:
High token cost
Irrelevant noise
Lower model accuracy
Need only the essential snippets.

How it works
Vector store retrieves raw documents.
A compressor (LLM or heuristic) extracts:
Key sentences
Important spans
Summaries
Returns compressed info to downstream LLM.

When to use
Big documents where only small parts matter.
Reduce context window cost.
Improve precision in RAG pipelines.
------------------------------------------------------------------------------------------------
5. Wikipedia Retriever
What is it?
A retriever that fetches content directly from the live Wikipedia API or a local dump.

Problem it solves
Need high-quality, public factual information.
Avoids hosting your own vector store for global knowledge.

How it works
Converts query → keyword search → Wikipedia API lookup.
Retrieves relevant article titles & fetches text sections.
Returns the raw article text or summaries.

When to use
You need real-world knowledge not in your custom data.
QA over public domain topics (history, biology, events).
LLM answering general knowledge questions.