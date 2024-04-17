import streamlit as st
import subprocess
import json
import os

# Set Streamlit theme to dark
st.markdown(
    """
    <style>
    .reportview-container {
        background: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextInput>div>div>input {
        color: #FFFFFF;
    }
    .st-bm {
        background-color: #2E2E2E !important;
        color: #FFFFFF !important;
    }
    .st-bq {
        border-color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)
command = 'ollama run codellama'

def aggregate_js_files(folder_path):
    if not os.path.exists('aggregated_text'):
        os.makedirs('aggregated_text')
    
    with open(os.path.join('aggregated_text', 'aggregated_code.txt'), 'w') as aggregated_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.js','.ts')):
                    aggregated_file.write(f"\n\n// File: {file}\n\n")
                    with open(os.path.join(root, file), 'r') as js_file:
                        js_content = js_file.read()
                        aggregated_file.write(js_content)

def execute_command_with_input(input_string):
    try:
        proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc.stdin.write(input_string + '\n')
        proc.stdin.flush()
        output, error = proc.communicate()
        if proc.returncode != 0:
            return f"Error: {error}"
        return output
    except Exception as e:
        return f"Error: {e}"

def main():
    global command

    st.title("Code Summary Generator")

    folder_path = 'js_folder'

    if st.button("Parse JS Files"):
        aggregate_js_files(folder_path)

        with open(os.path.join('aggregated_text', 'aggregated_code.txt'), 'r') as aggregated_file:
            file_contents = aggregated_file.read()

        st.subheader("Uploaded File Contents")
        st.text_area("", value=file_contents, height=200, key="uploaded_file_contents")

        file_contents += 'generate graph data output, Json data output for this angular code'

        response = execute_command_with_input(file_contents)

        st.subheader("Response")
        st.text_area("", value=response, height=200, key="response_text_area")

        try:
            graph_data = json.loads(response)
            with open("graph_data.txt", "w") as json_file:
                json.dump(graph_data, json_file)
        except Exception as e:
            st.error(f"Error saving graph data: {e}")

    st.subheader("Query Chat")
    user_query = st.text_input("Ask a question:")
    if user_query:
        response = execute_command_with_input(user_query)
        st.text_area("", value=response, height=100, key="query_response_text_area")

if __name__ == "__main__":
    main()
