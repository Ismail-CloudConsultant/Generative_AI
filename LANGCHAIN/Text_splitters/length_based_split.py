from langchain_text_splitters import CharacterTextSplitter

text="""langchain.text_splitter is where most of LangChain’s built-in text splitters live.
Here are the most commonly used imports and how to use them."""

splitter=CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=0,
    separator=" ")
print(splitter.split_text(text))    