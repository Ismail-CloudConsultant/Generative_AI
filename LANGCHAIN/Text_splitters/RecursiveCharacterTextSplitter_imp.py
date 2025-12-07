    # "\n\n" → Paragraph Separator
    # "\n" → Line Break (New Line)
    # " " → Space
    # "" → Character-Level (Fallback)

# Start with the biggest separator
# Split
# If any piece > chunk_size → split again using the next smaller separator
# Repeat recursively until:
# either the size fits or final fallback "" is used
# Use sliding window to add chunk overlap
# Return final chunks

from langchain_text_splitters import RecursiveCharacterTextSplitter

text="""langchain_text_splitters is where most of LangChain’s built-in text splitters live.
Here are the most commonly used imports and how to use them."""

splitter=RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=0)
print(splitter.split_text(text))    