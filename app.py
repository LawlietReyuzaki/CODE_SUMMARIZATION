
import streamlit as st
import subprocess
import json

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

# Define the command globally
command = "ollama run codellama"

def execute_command_with_input(input_string):
    try:
        # Open a subprocess with the global command
        proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send input string to the process
        proc.stdin.write(input_string + '\n')
        proc.stdin.flush()
        
        # Read output and error
        output, error = proc.communicate()
        
        # Check if there was any error
        if proc.returncode != 0:
            return f"Error: {error}"
        
        return output
    except Exception as e:
        return f"Error: {e}"

def main():
    global command

    st.title("Code Summary Generator")

    # File upload section
    uploaded_file = st.file_uploader("Upload TXT file", type="txt")

    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")

        # Display uploaded file contents
        st.subheader("Uploaded File Contents")
        st.text_area("", value=file_contents, height=200, key="uploaded_file_contents")

        file_contents = file_contents + 'generate graph data output, Json data output for this angular code'

        # Execute the command with input string
        response = execute_command_with_input(file_contents)

        # Display the response
        st.subheader("Response")
        st.text_area("", value=response, height=200, key="response_text_area")
        
        # Save JSON graph data to a file
        try:
            graph_data = json.loads(response)
            with open("graph_data.txt", "w") as json_file:
                json.dump(graph_data, json_file)
        except Exception as e:
            st.error(f"Error saving graph data: {e}")

        # Allow user to ask queries
        st.subheader("Query Chat")
        user_query = st.text_input("Ask a question:")
        if user_query:
            response = execute_command_with_input(user_query)
            st.text_area("", value=response, height=100, key="query_response_text_area")



if __name__ == "__main__":
    main()
