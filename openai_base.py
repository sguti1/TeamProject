import os
from dotenv import load_dotenv
from openai import OpenAI
from etf_base import build_etf_table, show_top10_table

load_dotenv()
APIKEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=APIKEY)

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about an ETF currency allocation table. "
    "Use only the information from the table provided. "
    "Do not reference or reveal any implementation details or code."
)


def get_etf_context(csv_path: str = 'data/imf_dataset.csv') -> str:
    """
    Builds the ETF allocation table, produces the top-10 summary, and returns it as a markdown string for context.
    """
    etf_table, wide_df = build_etf_table(csv_path)
    summary_df = show_top10_table(etf_table, wide_df)
    return summary_df.to_markdown(index=False)

def ask_about_etf_table(question: str, context_markdown: str, model: str = "gpt-4o") -> str:
    """
    Sends the ETF table (in markdown) + user question to OpenAI, returning the model's answer.
    """
    messages = [
        {"role": "system",    "content": SYSTEM_PROMPT},
        {"role": "user",      "content": f"Here is the ETF summary table in markdown:\n\n{context_markdown}"},
        {"role": "user",      "content": question},
    ]
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    md = get_etf_context()
    print("\nETF summary table:\n")
    print(md)

    q = input("\nYour question: ")
    print("\nAssistant’s answer:\n")
    print(ask_about_etf_table(q, md))
