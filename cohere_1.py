
import cohere
co = cohere.Client(api_key="api key")
user_content = input("Enter your prompt: ")

response = co.chat(
  model="command-r-plus-08-2024",
  message=user_content
)

print("Response content:", response.text)  
