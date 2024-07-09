import os
import time
import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
from dotenv import load_dotenv
from src.chatbot import ChatBot

load_dotenv()
user_input = None
def main(chatbot):
    global user_input
    while True:
        user_input = wait_user_message()
        intent = chatbot.detect_intent(user_input)
        user_input = None
        if "order_status" == intent:
            order_status(chatbot)
        elif "representative_request" == intent:
            speak_to_representive(chatbot)
        elif "return_policy" == intent:
            return_policy(chatbot)
        elif "items_cannot_be_returned" == intent:
            non_returnable_items(chatbot)
        elif "refund" == intent:
            refund_method(chatbot)
        elif "quit" == intent:
            send_chatbot_message(chatbot.get_goodbye())
            quit()
        else:  # Other is also here
            send_chatbot_message(chatbot.get_other())
        user_input = None


def return_policy(chatbot):
    send_chatbot_message(chatbot.get_return_policy())

def non_returnable_items(chatbot):
    send_chatbot_message(chatbot.get_non_returnable_items())


def refund_method(chatbot):
    send_chatbot_message(chatbot.get_refund_method())


def order_status(chatbot):
    send_chatbot_message("Please provide your order ID: ")
    order_id = wait_user_message()
    global user_input
    user_input = None
    send_chatbot_message(chatbot.get_order_status(order_id))


def speak_to_representive(chatbot):
    global user_input
    send_chatbot_message("type quit to stop entering details.")
    output = None
    while not chatbot.waiting_for_human_representative():
        if not output and not chatbot.has_full_name():
            send_chatbot_message("Please provide your full name: ")
            full_name = wait_user_message()
            user_input = None
            if full_name.lower() in ["quit", "exit"]:
                break
            output = chatbot.set_full_name(full_name)  # If the full name is not valid
        if not output and not chatbot.has_email():
            send_chatbot_message("Please provide your email: ")
            email = wait_user_message()
            user_input = None
            if email.lower() in ["quit", "exit"]:
                break
            output = chatbot.set_email(email)  # If the email is not valid
        if not output and not chatbot.has_phone():
            send_chatbot_message("Please provide your phone number: ")
            phone = wait_user_message()
            user_input = None
            if phone.lower() in ["quit", "exit"]:
                break
            output = chatbot.set_phone(phone)  # If the phone number is not valid
        if output:
            send_chatbot_message(output)
            output = None
        else:
            send_chatbot_message(chatbot.handle_request_human())
            break

def wait_user_message():
    global user_input
    while not user_input:
        root.update()
        time.sleep(0.01)  # Optional: Add a small delay to reduce CPU load
    return user_input

def get_user_message():
    global user_input
    user_input = user_entry.get()
    chatbox.config(state=tk.NORMAL)
    # Add user message with icon
    chatbox.window_create(tk.END, window=create_message_frame("You: ",user_input, user_icon, color="blue"))
    chatbox.insert(tk.END, "\n")
    user_entry.delete(0, tk.END)
    chatbox.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)

def send_chatbot_message(response):
    chatbox.window_create(tk.END, window=create_message_frame("Chatbot:",response, chatbot_icon, color="red"))
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, "\n")
    chatbox.config(state=tk.DISABLED)
    chatbox.yview(tk.END) #jump the view to the end


# Function to create a message frame with optional icon
def create_message_frame(user, message, icon=None, color="black"):
    frame = tk.Frame(chatbox, bg="white")
    if icon:
        icon_label = tk.Label(frame, image=icon, bg="white")
        icon_label.pack(side=tk.LEFT, padx=5, pady=5)
    message_label = tk.Label(frame, text=user, bg="white", anchor='w', fg=color, justify='left', wraplength=400)
    message_label.pack(side=tk.LEFT, padx=5, pady=5)
    message_label = tk.Label(frame, text=message, bg="white", anchor='w', fg="black", justify='left', wraplength=400)
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

apikey = os.environ.get("OPENAI_API_KEY")
chatbot = ChatBot(apikey)

# Create the user input field
user_entry = tk.Entry(root, width=100)
user_entry.pack(padx=10, pady=5, fill=tk.X, expand=True)
user_entry.bind("<Return>", lambda event: get_user_message())

send_button = tk.Button(root, text="Send", command=get_user_message)
send_button.pack(padx=10, pady=5)

send_chatbot_message("Hello! How can I help you today?")
chatbox.tag_config('chatbot_prefix', foreground='red')
chatbox.tag_config('chatbot_response', foreground='black')
chatbox.tag_config('user_prefix', foreground='blue')
root.after(0, main, chatbot)
# Run the application
root.mainloop()

