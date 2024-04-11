import streamlit as st
import subprocess

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
        response = execute_command_with_input(file_contents+'generate graph data output and Jason data output for this angular code')

        # Display the response
        st.text_area("Response", value=response, height=200)


if __name__ == "__main__":
    main()

