# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables from the .env file
# load_dotenv()

# # Configure the API key for the Google Generative AI SDK
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("API key is not set. Please set the GEMINI_API_KEY environment variable.")

# genai.configure(api_key=api_key)

# # Define the generation configuration for the chatbot
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 150,  # Adjusted to a smaller value for practical responses
#     "response_mime_type": "text/plain",
# }

# # Create the model instance
# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config=generation_config,
#     # safety_settings = Adjust safety settings
#     # See https://ai.google.dev/gemini-api/docs/safety-settings
# )

# # Start a chat session
# chat_session = model.start_chat()

# # Define a function to handle user input and get responses
# def chat_with_bot(user_message):
#     response = chat_session.send_message(user_message)
#     return response.text

# # Main loop for user interaction
# if __name__ == "__main__":
#     print("Chatbot: Hello! How can I assist you today? Type 'exit' to end the conversation.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "bye"]:
#             print("Chatbot: Goodbye!")
#             break
#         bot_response = chat_with_bot(user_input)
#         print(f"Chatbot: {bot_response}")


from flask import Flask, request, jsonify, send_from_directory
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Configure the API key for the Google Generative AI SDK
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key is not set. Please set the GEMINI_API_KEY environment variable.")

genai.configure(api_key=api_key)

# Define the generation configuration for the chatbot
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Helper function to generate test cases for code
def generate_test_cases(code_input):
    prompt = (
        "You are a code testing assistant. Please generate test cases for the following code:\n\n"
        f"{code_input}\n\n"
        "Provide the number of test cases possible followed by the test cases."
    )
    response = model.start_chat().send_message(prompt)
    return response.text

# Route to serve the HTML file
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Route to handle file upload and test case generation
@app.route('/upload-and-generate', methods=['POST'])
def upload_and_generate():
    code_input = None

    # Check if a file was uploaded
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        with open(file_path, 'r') as f:
            code_input = f.read()

    # Check if a code snippet was submitted
    elif 'code_snippet' in request.form:
        code_input = request.form['code_snippet']

    # If neither was provided, return an error
    if not code_input:
        return jsonify({"error": "No code provided"}), 400

    # Generate test cases
    result = generate_test_cases(code_input)

    # Extract number of test cases and test cases from result
    num_test_cases = result.split('\n', 1)[0]  # First line is the number of test cases
    test_cases = result.split('\n', 1)[1] if '\n' in result else result

    return jsonify({
        "num_test_cases": num_test_cases.strip(),
        "test_cases": test_cases.strip()
    }), 200

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    # Run the Flask application
    app.run(debug=True)

