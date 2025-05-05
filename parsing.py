from langchain_ollama import OllamaLLM
from urllib.parse import urlparse
from langchain_core.prompts import ChatPromptTemplate
import google.generativeai as genai
from IPython.display import Image
from IPython.core.display import HTML

API_KEY = open('Geminikey').read()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# gets the base of a link (eg: https://www.google.com - click/access at your own risk) 
def get_base_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


# accepts a list of chunks/strings (dom_chunks) to be passed and a context prompt (parse_description)
# the results are added to a list (parsed_results) and are then joined and returned
def parsing_with_gemini(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = model.generate_content([parse_description, chunk])
        print(f"Parsed batch {i} of {len(dom_chunks)}")

        parsed_results.append(response.text)

    return "\n".join(parsed_results)

# This joins all the chunks prior to parsing
def parsing_with_gemininochunks(dom_chunks, parse_description):
    chunk = "\n".join(dom_chunks)

    response = model.generate_content([parse_description, chunk])


    return response.text

# Very important to prevent ...
def appreciate(message):
    print(message + '\n')
    print(model.generate_content(message).text)














# model = OllamaLLM(model='llama3.1')

# template = (
#     "You are tasked with extracting specific information from the following text content: {dom_content}. "
#     "Please follow these instructions carefully: \n\n"
#     "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Empty Response:** If no information matches the description, return an empty string ('')."
#     "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
# )

# def parsing_with_ollama(dom_chunks, parse_description):
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model

#     parsed_results = []

#     for i, chunk in enumerate(dom_chunks, start=1):
#         response = chain.invoke(
#             {"dom_content": chunk, "parse_description": parse_description}
#             )
        
#         print(f"Parsed batch {i} of {len(dom_chunks)}")

#         parsed_results.append(response)

#     return "\n".join(parsed_results)

