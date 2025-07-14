import requests
import random
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://pengu.gaia.domains"
MODEL = "qwen2-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
    "What is Indonesia?",
    "Where is Indonesia located?",
    "What is the capital of Indonesia?",
    "How many islands does Indonesia have?",
    "Why is Indonesia called the Emerald of the Equator?",
    "What is the population of Indonesia?",
    "What is the official language of Indonesia?",
    "What are the major religions in Indonesia?",
    "What currency is used in Indonesia?",
    "Why is Indonesia a popular tourist destination?",
    "What is the national motto of Indonesia?",
    "What is the meaning of Bhinneka Tunggal Ika?",
    "What are the main ethnic groups in Indonesia?",
    "How is Indonesia's political system structured?",
    "What type of government does Indonesia have?",
    "Who is the current president of Indonesia?",
    "What is the national anthem of Indonesia?",
    "What are Indonesia’s neighboring countries?",
    "Why is Indonesia considered a biodiversity hotspot?",
    "What is the largest island in Indonesia?",
    "What is the smallest province in Indonesia?",
    "What is the most populous city in Indonesia?",
    "Why is Bali famous worldwide?",
    "What is the significance of Java Island?",
    "What are the traditional Indonesian houses called?",
    "What are the main traditional dances in Indonesia?",
    "What is batik and why is it important?",
    "What are some Indonesian UNESCO World Heritage Sites?",
    "What is the Komodo dragon and where is it found?",
    "What are the major volcanoes in Indonesia?",
    "Why is Indonesia prone to earthquakes?",
    "What is the Ring of Fire and how does it affect Indonesia?",
    "What is the traditional food of Indonesia?",
    "What is nasi goreng?",
    "What is rendang and why is it popular?",
    "What is satay and how is it made?",
    "What are Indonesian spices known for?",
    "What is Gado-Gado?",
    "What is the role of rice in Indonesian culture?",
    "What are the most spoken local languages in Indonesia?",
    "What is Bahasa Indonesia derived from?",
    "How did Indonesia gain independence?",
    "When did Indonesia declare independence?",
    "Who was Sukarno?",
    "What is the importance of Pancasila?",
    "Why did Indonesia experience the Reformasi period?",
    "What was the Dutch East Indies?",
    "What is the role of the MPR in Indonesia?",
    "Why is Papua a special region?",
    "What are special autonomous regions in Indonesia?",
    "What is the function of the DPR?",
    "How many provinces are there in Indonesia?",
    "What is the Indonesian archipelago?",
    "What is the importance of the Strait of Malacca to Indonesia?",
    "What are the natural resources of Indonesia?",
    "What is the economy of Indonesia based on?",
    "What are the main exports of Indonesia?",
    "What are some major Indonesian companies?",
    "What is the role of the palm oil industry in Indonesia?",
    "What is the education system like in Indonesia?",
    "What are the top universities in Indonesia?",
    "What is the role of religion in Indonesian society?",
    "What is Islam Nusantara?",
    "How are traditional beliefs still practiced in Indonesia?",
    "What is the significance of Nyepi in Bali?",
    "What is the role of gamelan music in Indonesia?",
    "What is wayang and how is it performed?",
    "What are the most popular sports in Indonesia?",
    "What is the Indonesian national football team called?",
    "Why is badminton important in Indonesia?",
    "What is the role of youth in Indonesian politics?",
    "What are the major political parties in Indonesia?",
    "What is the KPK and what does it do?",
    "How is corruption addressed in Indonesia?",
    "What is the role of military in Indonesian history?",
    "What is the role of women in Indonesian society?",
    "What are current environmental issues in Indonesia?",
    "What is Indonesia’s stance on climate change?",
    "What is the role of forests in Indonesia?",
    "What is deforestation and how does it affect Indonesia?",
    "What are the endangered species in Indonesia?",
    "What is the role of traditional markets in Indonesia?",
    "What is the digital economy like in Indonesia?",
    "What is the impact of startups in Indonesia?",
    "What is Gojek and how did it start?",
    "What is Tokopedia?",
    "How is e-commerce growing in Indonesia?",
    "What is the role of social media in Indonesian society?",
    "What are some popular Indonesian celebrities?",
    "What is the influence of Korean culture in Indonesia?",
    "What are Indonesian traditional ceremonies?",
    "What is Idul Fitri and how is it celebrated in Indonesia?",
    "What are the main public holidays in Indonesia?",
    "What is the significance of Independence Day in Indonesia?",
    "What are some popular travel destinations in Indonesia?",
    "What is the function of the Garuda symbol?",
    "What are the traditional weapons of Indonesia?",
    "What is the significance of the kris?",
    "What is the role of youth organizations in Indonesia?"
]

def chat_with_ai(api_key: str, question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    print("Title: GaiaAI Chatbot")
    print("Twitter: https://x.com/0xMoei")
    api_key = input("Enter your API key: ")
    run_bot(api_key)

if __name__ == "__main__":
    main()
