import unittest
from contextlib import redirect_stdout
from src.chatbot import ChatBot
from src.main import main
from io import StringIO
import sys
from unittest.mock import patch

class MyTestCase(unittest.TestCase):
    @patch('builtins.input', side_effect=['order status.', 12345, 'exit'])
    def test_user_status(self, mock_input):
        """
        Test user status: user enters 'order status' and expects the chatbot to ask for order ID.
        """
        with StringIO() as buf, redirect_stdout(buf):
            main()
            output = buf.getvalue()
            self.assertIn("Chatbot: Your order with ID 12345 is being processed.", output)

    def test_request_human_representive(self):
        """
        Test request human representative: user enters 'speak to a representative' and expects the chatbot to ask for full name, email, and phone number.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John Doe', 'a@a.com', '05555555555', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: Your request has been submitted. Our representative will contact you soon.", output)

    def test_request_human_twice(self):
        """
        Test request human representative twice: user enters 'speak to a representative' twice and expects the chatbot to ask for full name, email, and phone number.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John Doe', 'a@a.com', '05555555555','speak to a representative','exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: You have already requested to speak to a representative. Please wait for our team to contact you.", output)

    def test_incorrect_name(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect name.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John', 'exit', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: first name and last name must be separated by a space.", output)

    def test_email_no_hash(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect name.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John Doe', 'aa', 'exit', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: Please enter @ in the email.", output)

    def test_email_no_dot(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect name.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John Doe', 'aa.com', 'exit', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: Please enter @ in the email.", output)

    def test_phone_not_long_enough(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect phone number.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John Doe', 'a@a.com', 'asdf', 'exit','exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: incorrect amount of digits.", output)

    def test_phone_local(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect phone number.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John Doe', 'a@a.com', '0585710693', 'exit','exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: Your request has been submitted. Our representative will contact you soon.", output)

    def test_phone_world(self):
        """
        Test incorrect name: user enters 'speak to a representative' and enters an incorrect phone number.
        """
        with patch('builtins.input', side_effect=['speak to a representative', 'John Doe', 'a@a.com', '+972585710693', 'exit','exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: Your request has been submitted. Our representative will contact you soon.", output)

    def test_return_policy(self):
        """
        Test return policy: user enters 'return policy' and expects the chatbot to ask for the return policy.
        """
        with patch('builtins.input', side_effect=['What is the return policy for items purchased at our store?', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: You can return most items within 30 days of purchase for a full refund or exchange. Items must be in their original condition, with all tags and packaging intact. Please bring your receipt or proof of purchase when returning items.", output)

    def test_return_policy_non_returnable_items(self):
        """
        Test return policy: user enters 'return policy' and expects the chatbot to ask for the return policy.
        """
        with patch('builtins.input', side_effect=['Are there any items that cannot be returned under this policy?', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: Yes, certain items such as clearance merchandise, perishable goods, and personal care items are non-returnable. Please check the product description or ask a store associate for more details.", output)

    def test_return_policy_refund_method(self):
        """
        Test return policy: user enters 'How will I receive my refund?' and expects the chatbot to ask for the refund policy.
        """
        with patch('builtins.input', side_effect=['How will I receive my refund?', 'exit']):
            with StringIO() as buf, redirect_stdout(buf):
                main()
                output = buf.getvalue()
                self.assertIn("Chatbot: Refunds will be issued to the original form of payment. If you paid by credit card, the refund will be credited to your card. If you paid by cash or check, you will receive a cash refund.", output)

if __name__ == '__main__':
    unittest.main()
