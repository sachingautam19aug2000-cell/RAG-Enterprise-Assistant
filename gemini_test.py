from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain RAG in one simple sentence."
)

print("=" * 60)
print("GEMINI CONNECTION TEST")
print("=" * 60)
print(response.text)
print("=" * 60)
