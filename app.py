from flask import Flask, render_template, jsonify, session
import openai
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

openai.api_key = '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'

@app.route('/get_text', methods=['GET'])
def get_text():
    max_tokens = 1000
    random_num = random.randint(1, 100)



    if 'counter' not in session:
        session['counter'] = 0


    session['counter'] += 1


    if 'last_answer' not in session:
         
            prompt = f"Generate a question in a surreal and mystic manner (situation {random_num}):"
    else:
 
        prompt = f"The answer to the last question was '{session['last_answer']}'. Please generate a related question in a mystic and surreal manner (situation {random_num}):"

    response = openai.Completion.create(
        engine="text-curie-001",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=1
    )

    question = response.choices[0].text.strip()
    print("Generated Question:", question)


    prompt2 = f"The question '{question}' is asked. Please generate an answer"

    response = openai.Completion.create(
        engine="text-ada-001",
        prompt=prompt2,
        max_tokens= max_tokens,
        n=1,
        stop=None,
        temperature=1
    )

    answer = response.choices[0].text.strip()
    print("Answer:", answer)


    session['last_answer'] = answer
    session.modified = True

    return jsonify(question=question, answer=answer)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8001)
