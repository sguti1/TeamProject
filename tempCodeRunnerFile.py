from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from etf_base import build_etf_table, show_top10_table, compute_etf_value
from openai_base import ask_about_etf_table

load_dotenv()

app = Flask(__name__)

IMF_CSV = 'data/imf_dataset.csv'
etf_table, wide_df = build_etf_table(IMF_CSV)
summary_df = show_top10_table(etf_table, wide_df)
etf_value = compute_etf_value(etf_table, wide_df)
summary_html = summary_df.to_html(classes='table table-striped', index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json() or {}
        question = data.get('question', '')
        answer = ask_about_etf_table(question, summary_html)
        return jsonify({'answer': answer})

    return render_template(
        'index.html',
        etf_value=etf_value,
        summary_html=summary_html
    )

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)