from .pizza import PizzaChat


def test_non_pizza_message():
    pizza_chat = PizzaChat()

    assert pizza_chat.process_message('some unrelated topic', '123') is None


def test_unauthorized():
    pizza_chat = PizzaChat()

    assert pizza_chat.process_message('-pizza_start', '123') == 'Unauthorized user.'

