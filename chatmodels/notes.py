import streamlit as st
from langchain_perplexity import ChatPerplexity
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import io

# --- Load Environment Variables ---
load_dotenv()

# --- Helper Function for Text Extraction (No changes needed here) ---
def get_text_from_file(uploaded_file):
    text = ""
    try:
        file_bytes = io.BytesIO(uploaded_file.read())
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(file_bytes)
            for page in pdf_reader.pages:
                text += (page.extract_text() or "") + "\n"
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file_bytes)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif uploaded_file.type == "text/plain":
            text = file_bytes.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None
    return text

# --- A STRONGER, MORE DIRECT PROMPT TEMPLATE ---
# This version is more direct and uses clearer commands.
template_string = """
You are an expert academic assistant. Your task is to act as an instructional designer.
You MUST strictly follow all instructions below.

Source Document:

{document_text}


**Your Task:**
From the source document above, generate a complete study guide. The output MUST be organized into the exact four sections specified below, using Markdown for formatting.

### 1. Core Concepts & Key Points
- Summarize all main ideas, theories, and arguments.
- Use nested bullet points for sub-topics.
- Emphasize key terms in **bold**.

### 2. Important Formulas & Equations
- List all mathematical or scientific formulas found in the document.
- For each formula, explain its variables and its purpose.
- If no formulas are present, you MUST write: "No significant formulas were found in the document."

### 3. Figures & Diagrams Summary
- Describe any figures, charts, or diagrams mentioned. Explain what each one illustrates.
- If no figures are present, you MUST write: "No significant figures or diagrams were found in the document."

### 4. Comprehensive Question Bank
Generate a question bank based ONLY on the source document. You MUST create all three of the following question types:
- **10 Multiple Choice Questions (MCQs):** Each with four options (A, B, C, D). Indicate the correct answer for each.
- **5 Short Answer Questions:** Requiring concise, 1-3 sentence answers.
- **2 Long Answer Questions:** Requiring detailed, multi-paragraph responses.

Begin generating the study guide now.
"""

# --- Streamlit App UI ---
st.set_page_config(page_title="Study Guide Generator", layout="wide")
st.header("📚 Advanced Study Guide Generator")
st.markdown("Upload a document (PDF, DOCX, TXT) to generate detailed notes, summaries of formulas/figures, and a complete question bank.")

uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "txt"])

if st.button("✨ Generate Study Guide", type="primary") and uploaded_file is not None:
    with st.spinner("🧑‍🏫 Your expert assistant is analyzing the document and building your guide..."):
        # 1. Extract text
        extracted_text = get_text_from_file(uploaded_file)

        if extracted_text and len(extracted_text) > 10: # Check if text is substantial
            try:
                # 2. Set up the model
                model = ChatPerplexity(model="llama-3.1-sonar-small-128k-online")

                # 3. Create the LangChain PromptTemplate
                prompt_template = PromptTemplate(
                    template=template_string,
                    input_variables=["document_text"]
                )
                
                # 4. Create the LLMChain
                # This chain reliably combines the prompt template and the model.
                chain = LLMChain(llm=model, prompt=prompt_template)

                # 5. Run the chain with the extracted text
                # We use .invoke() on the chain itself now.
                result = chain.invoke({"document_text": extracted_text})
                
                # The output from a chain is a dictionary, so we access the 'text' key.
                st.success("Your study guide is ready!")
                st.markdown(result['text'])

            except Exception as e:
                st.error(f"An error occurred with the AI model: {e}")
        elif extracted_text:
            st.warning("The document contains very little text. Please upload a more substantial file.")
        else:
            st.error("Could not extract text from the document. The file might be empty, corrupted, or an image-based PDF that cannot be read.")
elif st.button("✨ Generate Study Guide", type="primary"):
    st.error("Please upload a document first.")
