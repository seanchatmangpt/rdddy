import ijson
import tiktoken

# Define the path to your large JSON file
json_file_path = "/Users/candacechatman/dev/rdddy/data/conversations.json"


from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Any
from decimal import Decimal

class Author(BaseModel):
    role: str
    name: Optional[str] = None
    metadata: dict

class ContentPart(BaseModel):
    content_type: str
    parts: List[str] | None

class Message(BaseModel):
    id: str
    author: Author
    content: ContentPart
    status: str
    metadata: dict

class Data(BaseModel):
    id: str
    message: Message | None
    parent: str | None
    children: List[str]


class Conversation(BaseModel):
    title: str
    mapping: dict


# Function to process each conversation chunk
def process_conversations_chunk(chunk):
    # Define Pydantic models as before
    from pydantic import BaseModel
    from typing import List

    # Process each conversation in the chunk
    for chunked in chunk:
        try:
            conversation = Conversation(**chunked)
            # Do whatever processing you need with the conversation
            # print(f"Title: {conversation.title}")
            for key in conversation.mapping:
                data = Data(**conversation.mapping[key])
                if data.message and data.message.author.role == "assistant":
                    for part in data.message.content.parts:
                        if "CoRL" in part:
                            print(part)
                        # encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
                        # print(len(encoding.encode(part)))
                        # print(part)
        except ValidationError as e:
            # print(e)
            pass



# Open the JSON file for streaming
with open(json_file_path, "rb") as json_file:
    conversations_generator = ijson.items(
        json_file, "item"
    )  # Assumes each conversation is a separate JSON object

    # Process the conversations in chunks (adjust the chunk size as needed)
    chunk_size = 10  # Define your desired chunk size
    chunk = []
    for conversation in conversations_generator:
        chunk.append(conversation)
        if len(chunk) >= chunk_size:
            process_conversations_chunk(chunk)
            chunk = []

    # Process any remaining conversations in the last chunk
    if chunk:
        process_conversations_chunk(chunk)
