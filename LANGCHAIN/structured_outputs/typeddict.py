from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal

load_dotenv()
model=ChatOpenAI()

class Review(TypedDict):
    key_themes: Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
    summary:Annotated [str,"A breif summary of the review"]
    sentiment:Annotated [str,"Negative , postive ,Neutral"]
    rating:Annotated [int,"Maximum out of 10"]
    pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]

structured_model=model.with_structured_output(Review)

result=structured_model.invoke("""
I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful
""")
print(result)

#{'key_themes': ['Snapdragon 8 Gen 3 processor', '5000mAh battery', '45W fast charging', 'S-Pen integration', '200MP camera', 'Night mode', 'Zoom capabilities', 'One-handed use', 'Bloatware', 'Price tag'], 'summary': 'Samsung Galaxy S24 Ultra is an absolute powerhouse with a lightning-fast processor, long-lasting battery, stunning camera, and unique S-Pen support. However, it suffers from the weight and size for one-handed use, bloatware in the form of unnecessary Samsung apps, and a high price tag of $1,300.', 'sentiment': 'Positive', 'rating': 9, 'pros': ['Insanely powerful processor (great for gaming and productivity)', 'Stunning 200MP camera with incredible zoom capabilities', 'Long battery life with fast charging', 'S-Pen support is unique and useful'], 'cons': ['Weight and size make it uncomfortable for one-handed use', 'Bloatware with unnecessary Samsung apps', 'High price tag of $1,300']}   