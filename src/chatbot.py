from openai import OpenAI
import csv
import os
import asyncio


class ChatBot:
    def __init__(self, api_key):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=api_key
        )
        self.api_key = api_key
        self.requested_human = False
        self.full_name = None
        self.email = None
        self.phone = None

    def has_full_name(self):
        return self.full_name is not None

    def set_full_name(self, full_name):
        if " " not in full_name:
            return "first name and last name must be separated by a space."
        self.full_name = full_name

    def has_email(self):
        return self.email is not None

    def set_email(self, email):
        if "@" not in email:
            return "Please enter @ in the email."
        if "." not in email:
            return "Please enter . in the email."
        self.email = email

    def has_phone(self):
        return self.phone is not None

    def set_phone(self, phone):
        if len(phone) != 10 and len(phone) != 13:
            return "incorrect amount of digits."
        if not phone.isdigit() and phone[0] != "+":
            return "phone number must contain only digits or + at the start"
        if phone[0] == "+" and len(phone) != 13:
            return "if there is + at the start, phone number must be 13 digits long."

        self.phone = phone

    def get_other(self):
        return "I can't help you with that. Please ask a different question."

    def get_goodbye(self):
        return "Goodbye!"
    def get_return_policy(self):
        return "You can return most items within 30 days of purchase for a full refund or exchange. Items must be in their original condition, with all tags and packaging intact. Please bring your receipt or proof of purchase when returning items."

    def get_non_returnable_items(self):
        return "Yes, certain items such as clearance merchandise, perishable goods, and personal care items are non-returnable. Please check the product description or ask a store associate for more details."

    def get_refund_method(self):
        return "Refunds will be issued to the original form of payment. If you paid by credit card, the refund will be credited to your card. If you paid by cash or check, you will receive a cash refund."

    def get_order_status(self, order_id):
        return "Your order with ID {} is being processed.".format(order_id)

    def detect_intent(self, user_input):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a chatbot that categorizes user input into predefined intents: order_status, representative_request, return_policy, items_cannot_be_returned, refund, other. Just return the detected intent."},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": "The user's intent is: [intent]"}  # Model will fill in the [intent] part
            ],
            max_tokens=10,
            model="gpt-3.5-turbo"
        )
        return response.choices[0].message.content

    def handle_request_human(self):
        self.requested_human = True

        # Save the contact information to a CSV file
        contact_info = [self.full_name, self.email, self.phone]
        with open('contact_info.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(contact_info)
        return "Your request has been submitted. Our representative will contact you soon."

    def waiting_for_human_representative(self):
        if self.requested_human:
            print(
                "Chatbot: You have already requested to speak to a representative. Please wait for our team to contact you.")
        return self.requested_human
