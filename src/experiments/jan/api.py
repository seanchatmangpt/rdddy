import openai

# Make a call to generate text
response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",  # Use the desired engine
    prompt="Translate the following English text to French: 'Hello, how are you?'",
    max_tokens=50,  # Adjust the number of tokens as needed
)

# Extract the generated text from the response
generated_text = response.choices[0].text

# Print the generated text
print(generated_text)
