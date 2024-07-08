from src.chatbot import ChatBot

# Set your OpenAI API key
from src.api_key import api_key
chatbot = ChatBot(api_key)

def main():
    print("Welcome to our e-commerce support chatbot!")
    while True:
        user_input = input("You: ")
        intent = chatbot.detect_intent(user_input)
        if "order status" == intent:
            order_status()
        elif "speak to a representative" == intent:
            speak_to_representive()
        elif "return policy" == intent:
            print("Chatbot:", chatbot.get_return_policy("return_policy"))
        elif "cannot be returned" == intent:
            print("Chatbot:", chatbot.get_return_policy("non_returnable_items"))
        elif "refund" == intent:
            print("Chatbot:", chatbot.get_return_policy("refund_method"))
        elif "quit" == intent:
            print("Chatbot: Goodbye!")
            break
        elif "other" == intent:
            pass
            print("Chatbot:", 'I can\'t help you with that. Please ask a different question.')


def order_status():
    order_id = input("Please provide your order ID: ")
    print("Chatbot:", chatbot.get_order_status(order_id))


def speak_to_representive():
    print("type quit to stop entering details.")
    output = None
    while not chatbot.waiting_for_human_representative():
        if not output and not chatbot.has_full_name():
            full_name = input("Please provide your full name: ")
            if full_name.lower() == "quit" or full_name.lower() == "exit":
                break
            output = chatbot.set_full_name(full_name)  # If the full name is not valid
        if not output and not chatbot.has_email():
            email = input("Please provide your email: ")
            if email.lower() == "quit" or email.lower() == "exit":
                break
            output = chatbot.set_email(email)  # If the email is not valid
        if not output and not chatbot.has_phone():
            phone = input("Please provide your phone number: ")
            if phone.lower() == "quit" or phone.lower() == "exit":
                break
            output = chatbot.set_phone(phone) # If the phone number is not valid

        if output:
            print("Chatbot:", output)
            output = None
        else:
            print("Chatbot:", chatbot.handle_request_human(full_name, email, phone))

if __name__ == "__main__":
    main()
