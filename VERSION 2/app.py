import streamlit as st
import subprocess
import json

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

    st.title("Code summary generator")

    # File upload section
    uploaded_file = st.file_uploader("Upload TXT file", type="txt")

    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")

        # Display uploaded file contents
        st.text_area("Uploaded File Contents", value=file_contents, height=200)

        # Execute the command with input string
        response = execute_command_with_input(file_contents)

        # Display the response
        st.text_area("Response", value=response, height=200)

        # Allow user to ask queries
        st.subheader("Query Chat")
        user_query = st.text_input("Ask a question:")
        if user_query:
            response = execute_command_with_input(user_query)
            st.text_area("Response", value=response, height=100)

        # Save JSON graph data to a file
        try:
            graph_data = json.loads(response)
            with open("graph_data.json", "w") as json_file:
                json.dump(graph_data, json_file, indent=4)
        except Exception as e:
            st.error(f"Error saving graph data: {e}")

if __name__ == "__main__":
    main()

