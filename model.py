import requests
import json
import pandas as pd
import sys

def chat_with_ollama(prompt, model="phi4"):
    """
    Sends a chat request to the Ollama API with the given prompt and model.
    """

    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True 
    }

    response = requests.post(url, json=payload, stream=True)

    content = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            content += data.get("message", {}).get("content", "")
    return content.strip()

def readJSON(filename, format_logs = False):
    """
    Simply reads a JSON file, formats file if needed.
    """
    with open(f"{filename}.json", "r") as file:
        file = json.load(file)

    return reformat_logs(file) if format_logs else file # Formats logs if needed.


def build_prompts(prompts, df):
    """
    Builds the prompt and adds the dataset as input.
    """
    res = []
    for category in prompts:
        for key, prompt in prompts[category].items():
            res.append((key ,f"{prompt} - {df}"))

    return res


def send_prompts(prompts):
    """
    Iterates over prompts list and sends to chat_with_ollama
    """
    for key, prompt in prompts:
        answer = chat_with_ollama(f"{prompt}", model="phi4")
        print(key, " - " , answer) 


def reformat_logs(test_failures):
    """
    Formats JSON prompts, allows the LLM to understand the prompts clearer.
    """
    log_lines = []
    for test in test_failures:
        log_entry = (
            f"[{test['test_id']}] {test['failure_type']} | "
            f"{test['error_message']} | "
            f"{test['last_code_change']} | "
            f"{test['environment']}"
        )
        log_lines.append(log_entry)
    log_lines = "\n".join(log_lines)

    return log_lines


def generateMetrics():
    print("---Execution Metrics---")
    df = pd.read_csv('qa_tests_dataset/test_results.csv') # Dataset of simple QA tests results.
    insights = readJSON("prompts/insights")               # Holds the engineered prompts. (You can modify to add more queries.)
    prompts = build_prompts(insights,df)                  # Builds the prompts.
    send_prompts(prompts)

def generateRecommendations():
    print("-- Failure Analysis --")
    test_failures = readJSON("qa_tests_dataset/test_failures", format_logs=True)  # Dataset of more complex QA tests results.
    recommend = readJSON("prompts/recommend")                                     # Holds the engineered prompts. (You can modify to add more queries.)
    prompts = build_prompts(recommend, test_failures)                             # Builds the prompts.
    send_prompts(prompts)


if __name__ == "__main__":

    generateMetrics()
    generateRecommendations()
    #chat_with_ollama("Hello")