import os
from src.chatbot import ChatBot
from dotenv import load_dotenv

load_dotenv()

def main(chatbot):
    print("Welcome to our e-commerce support chatbot!")
    while True:
        user_input = input("You: ")
        intent = chatbot.detect_intent(user_input)
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
            print("Chatbot:", chatbot.get_goodbye())
            break
        else:  # Other is also here
            print("Chatbot:", chatbot.get_other())


def return_policy(chatbot):
    print("Chatbot:", chatbot.get_return_policy())

def non_returnable_items(chatbot):
    print("Chatbot:", chatbot.get_non_returnable_items())


def refund_method(chatbot):
    print("Chatbot:", chatbot.get_refund_method())


def order_status(chatbot):
    order_id = input("Please provide your order ID: ")
    print("Chatbot:", chatbot.get_order_status(order_id))


def speak_to_representive(chatbot):

    output = None
    while not chatbot.waiting_for_human_representative():
        print("type quit to stop entering details.")
        if not output and not chatbot.has_full_name():
            full_name = input("Please provide your full name: ")
            if full_name.lower() in ["quit", "exit"]:
                break
            output = chatbot.set_full_name(full_name)  # If the full name is not valid
        if not output and not chatbot.has_email():
            email = input("Please provide your email: ")
            if email.lower() in ["quit", "exit"]:
                break
            output = chatbot.set_email(email)  # If the email is not valid
        if not output and not chatbot.has_phone():
            phone = input("Please provide your phone number: ")
            if phone.lower() in ["quit", "exit"]:
                break
            output = chatbot.set_phone(phone)  # If the phone number is not valid
        if output:
            print("Chatbot:", output)
            output = None
        else:
            print("Chatbot:", chatbot.handle_request_human())
            break


if __name__ == "__main__":
    apikey = os.environ.get("OPENAI_API_KEY")
    chatbot = ChatBot(apikey)
    main(chatbot)
