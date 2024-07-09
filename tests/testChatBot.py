import os
import unittest
from contextlib import redirect_stdout
from src.chatbot import ChatBot
from src.main import main, speak_to_representive, order_status, return_policy, non_returnable_items, refund_method
from io import StringIO
import sys
from unittest.mock import patch
from dotenv import load_dotenv

load_dotenv()

class MyTestCase(unittest.TestCase):

    def setUp(self):

        self.chatbot = ChatBot("api_key")

    @patch('builtins.input', side_effect=[12345])
    def test_user_status(self, mock_input):
        """
        Test user status: user enters 'order status' and expects the chatbot to ask for order ID.
        """
        with StringIO() as buf, redirect_stdout(buf):
            order_status(self.chatbot)
            output = buf.getvalue()
            self.assertIn("Chatbot: Your order with ID 12345 is being processed.", output)

    def test_request_human_representive(self):
        """
        Test request human representative: user enters 'speak to a representative' and expects the chatbot to ask for full name, email, and phone number.
        """
        with patch('builtins.input', side_effect=['John Doe', 'a@a.com', '0555555555']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: Your request has been submitted. Our representative will contact you soon.", output)

    def test_request_human_twice(self):
        """
        Test request human representative twice: user enters 'speak to a representative' twice and expects the chatbot to ask for full name, email, and phone number.
        """
        with patch('builtins.input', side_effect=['John Doe', 'a@a.com', '0555555555']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: You have already requested to speak to a representative. Please wait for our team to contact you.", output)

    def test_incorrect_name(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect name.
        """
        with patch('builtins.input', side_effect=['John', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: first name and last name must be separated by a space.", output)

    def test_email_no_hash(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect name.
        """
        with patch('builtins.input', side_effect=['John Doe', 'aa', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: Please enter @ in the email.", output)

    def test_email_no_dot(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect name.
        """
        with patch('builtins.input', side_effect=['John Doe', 'aa.com', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: Please enter @ in the email.", output)

    def test_phone_not_long_enough(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect phone number.
        """
        with patch('builtins.input', side_effect=['John Doe', 'a@a.com', 'asdf', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: incorrect amount of digits.", output)

    def test_phone_local(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect phone number.
        """
        with patch('builtins.input', side_effect=['John Doe', 'a@a.com', '0585710693', 'exit','exit']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: Your request has been submitted. Our representative will contact you soon.", output)

    def test_phone_world(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect phone number.
        """
        with patch('builtins.input', side_effect=['John Doe', 'a@a.com', '+972585710693', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                speak_to_representive(self.chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: Your request has been submitted. Our representative will contact you soon.", output)

    def test_return_policy(self):
        """
        Test return policy: user enters 'return policy' and expects the chatbot to ask for the return policy.
        """
        with StringIO() as buf, redirect_stdout(buf):
            return_policy(self.chatbot)
            output = buf.getvalue()
            self.assertIn("Chatbot: You can return most items within 30 days of purchase for a full refund or exchange. Items must be in their original condition, with all tags and packaging intact. Please bring your receipt or proof of purchase when returning items.", output)

    def test_return_policy_non_returnable_items(self):
        """
        Test return policy: user enters 'return policy' and expects the chatbot to ask for the return policy.
        """
        with StringIO() as buf, redirect_stdout(buf):
            non_returnable_items(self.chatbot)
            output = buf.getvalue()
            self.assertIn("Chatbot: Yes, certain items such as clearance merchandise, perishable goods, and personal care items are non-returnable. Please check the product description or ask a store associate for more details.", output)

    def test_return_policy_refund_method(self):
        """
        Test return policy: user enters 'How will I receive my refund?' and expects the chatbot to ask for the refund policy.
        """
        with StringIO() as buf, redirect_stdout(buf):
            refund_method(self.chatbot)
            output = buf.getvalue()
            self.assertIn("Chatbot: Refunds will be issued to the original form of payment. If you paid by credit card, the refund will be credited to your card. If you paid by cash or check, you will receive a cash refund.", output)

    def test_intent_order_status(self):
        """
        Test intent order status: user enters 'order status' and expects the chatbot to determine the intent.
        """
        with patch('builtins.input', side_effect=['order status', 12345, 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                api_key = os.environ.get("OPENAI_API_KEY")
                chatbot = ChatBot(api_key)
                main(chatbot)
                output = buf.getvalue()
                self.assertIn("Chatbot: Your order with ID 12345 is being processed.", output)

    def test_accuracy(self):
        """
        Test accuracy: user enters 'return policy' and expects the chatbot to determine the intent.
        """
        api_key = os.environ.get("OPENAI_API_KEY")
        chatbot = ChatBot(api_key)
        tests = { 'order_status': [
            'where is my package?',
            'what is the status of my order?',
            'where is my order?',
            'can you track my package?',
            'has my order shipped yet?',
            'when will my package arrive?',
            'how can I track my order?',
            'show me the status of my order please',
            'I want to know where my package is',
            'give me an update on my order status',
            'is my order on its way?',
            'tell me the delivery status of my order',
            'check order status',
            'track my shipment',
            'locate my package'
        ],
            'representative_request': [
                'I need to speak with a representative',
                'how can I talk to someone?',
                'can I speak to a human?',
                'connect me to a live agent',
                'talk to customer service',
                'get me a representative please',
                'I want to chat with an agent',
                'need assistance from a person',
                'help from a real person',
                'transfer me to a representative',
                'contact customer support'
            ],
            'return_policy': [
                'what is your return policy?',
                'how do I return an item?',
                'can I return this?',
                'what are your policies on returns?',
                'I want to send back my purchase',
                'how long do I have to return?',
                'returning an item',
                'policy for returning items',
                'explanation of your return policy',
                'conditions for returns',
                'do you accept returns?',

            ],
            'items_cannot_be_returned': [
                'which items cannot be returned?',
                'what items are non-returnable?',
                'are there any items I cannot return?',
                'list of non-returnable items',
                'items that cannot be refunded',
                'non-returnable products',
                'what can\'t I return?',
                'items that are final sale',
                'cannot return these items'
            ],
            'refund': [
                'how do I get a refund?',
                'can I get my money back?',
                'what is your refund process?',
                'process for refunds?',
                'refund my purchase please',
                'I want a refund',
                'refund policy',
                'when will I get refunded?',
                'how long does a refund take?',
                'getting money back',
                'return and refund',
                'can I get a credit back?',
                'can I get a refund?'
            ],
            'quit': [
                'exit',
                'goodbye',
                'quit',
                'stop',
                'end chat',
                'leave',
                'close',
                'terminate chat',
                'done chat',
                'bye'
            ],
            'other': [
                'can you help me with something else?',
                'I have another question',
                'unrelated inquiry',
                'ask about something different',
                'different topic',
                'not related to previous',
                'something else',
                'other matter',
                'another issue',
                'different question',
                'additional assistance',
                'something unrelated'
            ]
        }
        total, true_intent = 0, 0
        for intent, test_case in tests.items():
            for test in test_case:
                total += 1
                chatbot_intent = chatbot.detect_intent(test)
                print(f'True intent:{intent}, Chatbot intent: {chatbot_intent}, Question: {test}', end=' ')
                if chatbot_intent == intent:
                    true_intent += 1

                accuracy = true_intent / total if total > 0 else 0
                accuracy_percent = accuracy * 100
                print(f",total: {total}, true_intent: {true_intent}, accuracy: {accuracy_percent:.2f}%")
        print(f'total questions: {total}, true_intent: {true_intent}, accuracy: {accuracy_percent:.2f}%')



if __name__ == '__main__':
    unittest.main()
