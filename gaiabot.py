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
BASE_URL = "https://donglaochoicoin.gaia.domains"
MODEL = "Llama-3.2-3B-Instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
        "Who is Do Kwon?",
    "What is Do Kwon’s full name?",
    "Where is Do Kwon from?",
    "Where did Do Kwon go to university?",
    "What did Do Kwon study?",
    "What company did Do Kwon work at before crypto?",
    "What is Terraform Labs?",
    "When was Terraform Labs founded?",
    "What is the Terra blockchain?",
    "What is the LUNA token?",
    "What was UST (TerraUSD)?",
    "What is an algorithmic stablecoin?",
    "How did UST maintain its peg?",
    "What was the relationship between LUNA and UST?",
    "What was the Anchor Protocol?",
    "What was the promised yield of Anchor?",
    "Why was Anchor attractive to investors?",
    "What was the total value locked (TVL) in Terra before collapse?",
    "What was the all-time high price of LUNA?",
    "What caused the UST depeg?",
    "What is a death spiral in crypto?",
    "When did Terra collapse?",
    "What was the timeline of the LUNA-UST crash?",
    "How much value was lost in the Terra collapse?",
    "How did Do Kwon respond to the crash?",
    "What is the 'LUNAtics' community?",
    "What did Do Kwon tweet during the crash?",
    "What was Do Kwon’s attitude before the collapse?",
    "What was the 'steady lads' tweet?",
    "What is the $UST reserve fund?",
    "What happened to the BTC reserves for UST?",
    "Who investigated the Terra collapse?",
    "What lawsuits has Do Kwon faced?",
    "What is the U.S. SEC’s charge against Do Kwon?",
    "What is South Korea’s legal case against Do Kwon?",
    "Was Do Kwon arrested?",
    "Where was Do Kwon captured?",
    "What are the extradition demands for Do Kwon?",
    "How long was Do Kwon in hiding?",
    "What passport did Do Kwon allegedly use?",
    "What is Interpol’s role in the case?",
    "What are the fraud accusations against Do Kwon?",
    "Did Do Kwon mislead investors?",
    "What is the public reaction to Do Kwon’s tweets?",
    "What happened to retail investors during the collapse?",
    "How did centralized exchanges respond to the collapse?",
    "What is the difference between LUNA and LUNC?",
    "What is Terra 2.0?",
    "What is Terra Classic (LUNC)?",
    "Did Do Kwon support Terra 2.0?",
    "What is the community’s role in reviving Terra?",
    "What is the impact of the Terra collapse on DeFi?",
    "What is Do Kwon’s current legal status?",
    "Has Do Kwon spoken publicly after the collapse?",
    "What are the most controversial quotes by Do Kwon?",
    "What documentaries feature the Terra collapse?",
    "What is the impact of Terra’s collapse on crypto regulation?",
    "Did Do Kwon cause the 2022 crypto crash?",
    "What is Do Kwon’s defense against legal claims?",
    "What are whistleblower claims against Terra?",
    "What role did Jump Crypto allegedly play?",
    "Was the UST peg ever sustainable?",
    "What was Do Kwon’s philosophy about decentralization?",
    "What was the design flaw in Terra?",
    "What lessons did the industry learn from Do Kwon’s failure?",
    "What is the community’s opinion on Do Kwon today?",
    "Are there class action lawsuits against Do Kwon?",
    "What was the psychological effect of the crash?",
    "What was the response from other crypto founders?",
    "What was Vitalik Buterin’s reaction to Terra?",
    "What is the 'crypto arrogance' meme about Do Kwon?",
    "What is the impact on Korean crypto regulation?",
    "What is the South Korean FSC’s position on Do Kwon?",
    "What is the Terra whistleblower account 'FatManTerra'?",
    "What is Terra Rebels?",
    "What is LUNA burning and who supports it?",
    "Did Terra have external audits?",
    "What happened to the Anchor treasury?",
    "How much BTC was lost or moved from Luna Foundation Guard?",
    "What is the Luna Foundation Guard (LFG)?",
    "Did Do Kwon face charges of money laundering?",
    "What were the Twitter spaces like with Do Kwon?",
    "Did Do Kwon face an Interpol Red Notice?",
    "What was Do Kwon’s relationship with Korean regulators?",
    "Did Terra ever fully decentralize?",
    "Did Do Kwon communicate with Binance before the crash?",
    "What is the future of Terra without Do Kwon?",
    "What are the best threads explaining the collapse?",
    "What is the meme culture around Do Kwon?",
    "Did Do Kwon influence how stablecoins are regulated?",
    "Is Do Kwon still active in crypto?",
    "How does Do Kwon compare to Sam Bankman-Fried?",
    "Will Do Kwon serve jail time?",
    "Is Do Kwon still on social media?",
    "Will investors ever recover losses?",
    "Is Terra an example of DeFi failure?",
    "How is the Terra case used by regulators globally?",
    "What would Do Kwon do differently, in his own words?"
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
    print("Twitter: https://x.com/richdo160")
    api_key = input("Enter your API key:"")
    run_bot(api_key)

if __name__ == "__main__":
    main()
