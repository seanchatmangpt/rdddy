import ijson

# Define the path to your large JSON file
json_file_path = "/Users/candacechatman/Downloads/1dd9be16ec32302ab8cb0994090949c55e08baa435443c4b5e8f7f8279720e41-2024-01-12-05-55-50/conversations.json"


# Function to process each conversation chunk
def process_conversations_chunk(chunk):
    # Define Pydantic models as before
    from pydantic import BaseModel
    from typing import List

    class Message(BaseModel):
        author: str
        text: str

    class Conversation(BaseModel):
        title: str
        messages: List[Message]

    # Process each conversation in the chunk
    for data in chunk:
        conversation = Conversation(**data)
        # Do whatever processing you need with the conversation
        print(f"Title: {conversation.title}")
        for message in conversation.messages:
            print(f"Author: {message.author}")
            print(f"Text: {message.text}")


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
