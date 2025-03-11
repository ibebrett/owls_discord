pizza_admins = {333064292737875968, 985018113919692820}

available_toppings = [
    "cheese",
    "pepperoni",
    "sausage",
    "meatball",
    "bacon",
    "chicken",
    "shrimp",
    "broccoli",
    "onion",
    "mushroom",
    "olive",
    "veggie_bomb",
    "roasted_pepper",
    "hot_pepper",
    "garlic",
    "basil",
]


class PizzaChat:
    def __init__(self):
        self.topping_votes = dict()
        self.already_voted = set()

    def process_message(self, message_content: str, author_id: str) -> str | None:
        """Returns a string if we wish to handle the message, otherwise None"""

        if "-pizza_start" in message_content.lower():
            if author_id not in pizza_admins:
                return "Unauthorized user."

            self.topping_votes = dict()
            self.already_voted = set()

            return "Authorized"

        if "-pizza_vote" in message_content.lower():

            if author_id in already_voted:
                return "You have already voted :("

            topping = message_content.lower().split()[1]

            if topping not in available_toppings:
                return f"Topping {topping} is not available."

            if topping not in topping_votes:
                self.topping_votes[topping] = 0
            self.topping_votes[topping] += 1
            self.already_voted.add(author_id)

            return f"Placed your vote for {topping}."

        if "-show_toppings" in message_content.lower():
            newMessage = []
            for i in available_toppings:
                newMessage.append(i)
            return ", ".join(newMessage)

        if "-show_votes" in message_content.lower():

            if not self.topping_votes:
                return "No votes cast yet."

            msg = []
            for k, v in self.topping_votes.items():
                msg.append(f"{k} : {v} vote(s)")

            return "\n".join(msg)

        if "-help" in message_content.lower():
            return "COMMANDS:\n\
    -show_toppings: shows all available pizza toppings.\n\
    -pizza_vote: vote for a topping using '-pizza_vote {topping name}'.\n\
    -show_votes: shows current pizza topping votes.\n"
