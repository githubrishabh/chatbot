#This code is with having memory, trained on L12v2 (Sentence transformer) model and this ai chat also can execute on bases of similarity. Also integreted with custom chatgpt LLM (work for any organisation)
import os
from sentence_transformers import SentenceTransformer, util
import openai
import numpy as np
from dotenv import load_dotenv
from health_keywords import health_keywords

openai.api_key=os.getenv('KEY')

# Loading a Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

#Custom Sentence Filter
def is_health_and_fitness_query(user_input):    

    # Calculate embeddings for user input and keywords
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    keywords_embeddings = model.encode(health_keywords, convert_to_tensor=True)

    # Calculate cosine similarities
    similarity_scores = util.pytorch_cos_sim(user_embedding, keywords_embeddings).numpy()

    # If the maximum similarity score is above a 50% threshold, classify as a health and fitness query
    threshold = 0.35  # Adjusted to 50%
    return np.max(similarity_scores) > threshold

#Custom ChatBot
def chat_with_rishabh(user_input, conversation_history):
    # Your system message can be constant
    system_message = "You are a helpful assistant name FitFred work for AiTopFit company. Which can assist only regarding fitness related query. Prompt message Hey I am FitFred, your AI assistance available at your service :robot_face:  on every first user input"

    # Adding the system message to the conversation history
    conversation_history.append({"role": "system", "content": system_message})

    # Adding the user's input to the conversation history
    conversation_history.append({"role": "assistant", "content": "You are the Health and Fitness related chat bot name FitFred"})

    # Adding the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Check if the query is related to health and fitness
    if is_health_and_fitness_query(user_input):
        # Call OpenAI API with the conversation history
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        # Extract the assistant's reply
        reply = completion.choices[0].message.content

        # Adding the assistant's reply to the conversation history
        conversation_history.append({"role": "assistant", "content": reply})

        return reply
    else:
        return "Sorry, I can only answer queries related to health and fitness."

"""
  import sys
# Print the size of the conversation history
  print(f"Size of conversation history: {sys.getsizeof(conversation_history)} bytes")

"""