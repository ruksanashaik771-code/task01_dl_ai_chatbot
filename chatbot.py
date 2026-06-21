from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

history = []

print("Chatbot Started")
print("Type exit to quit\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    history.append(
        {"role": "user", "content": user_input}
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=history
    )

    bot_reply = response.choices[0].message.content

    history.append(
        {"role": "assistant", "content": bot_reply}
    )

    print("\nBot:", bot_reply)
    print()