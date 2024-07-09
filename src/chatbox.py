import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage

# A simple chatbot response function (replace with your detect_intent function)
def get_chatbot_response(user_input):
    # Placeholder response
    return "This is a placeholder response."

# Function to send the user's message to the chatbox and get a response
def send_message():
    user_input = user_entry.get()
    if user_input.strip():
        chatbox.config(state=tk.NORMAL)
        # Add user message with icon
        chatbox.window_create(tk.END, window=create_message_frame("You: " + user_input, user_icon))
        chatbox.insert(tk.END, "\n")
        user_entry.delete(0, tk.END)

        response = get_chatbot_response(user_input)
        # Add chatbot response
        chatbox.window_create(tk.END, window=create_message_frame("Chatbot: " + response, chatbot_icon))
        chatbox.insert(tk.END, "\n")
        chatbox.config(state=tk.DISABLED)
        chatbox.yview(tk.END)

def hello_message():
    chatbox.config(state=tk.NORMAL)
    chatbox.window_create(tk.END, window=create_message_frame("Chatbot: Hello! How can I help you today?", chatbot_icon))
    chatbox.insert(tk.END, "\n")
    chatbox.config(state=tk.DISABLED)
    chatbox.yview(tk.END)

# Function to create a message frame with optional icon
def create_message_frame(message, icon=None):
    frame = tk.Frame(chatbox, bg="white")
    if icon:
        icon_label = tk.Label(frame, image=icon, bg="white")
        icon_label.pack(side=tk.LEFT, padx=5, pady=5)
    message_label = tk.Label(frame, text=message, bg="white", anchor='w', justify='left', wraplength=400)
    message_label.pack(side=tk.LEFT, padx=5, pady=5)
    return frame

# Create the main window
root = tk.Tk()
root.title("Chatbot")

# Load the user icon
user_icon = PhotoImage(file="user_icon.png")
chatbot_icon = PhotoImage(file="chatbot_icon.png")

# change the root icon
root.iconphoto(False, chatbot_icon)

# Create the chatbox
chatbox = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, bg="white")
chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create the user input field
user_entry = tk.Entry(root, width=100)
user_entry.pack(padx=10, pady=5, fill=tk.X, expand=True)
user_entry.bind("<Return>", lambda event: send_message())

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)

hello_message()
# Run the application
root.mainloop()
