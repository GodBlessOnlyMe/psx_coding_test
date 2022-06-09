class Card:
    ranking = {
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "T": 9,
        "J": 10,
        "Q": 11,
        "K": 12,
        "A": 13,
    }
    def __init__(self, value_shape):
        self.value, self.shape = value_shape


class Hand:

    ranking = {
        "High Card": 1,
        "One Pair": 2,
        "Two Pairs": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
        "Royal Flush": 10,
    }

    def __init__(self, five_value_shapes):
        """initialize hand instance.

        :param five_value_shapes: five value_shape with delimeter one space
        :type five_value_shapes: str
        """
        self.cards = [Card(x) for x in five_value_shapes.split(" ")]
        self.rank = self.get_rank()

    def get_rank(self):
        ...

    def is_high_card(self):

    def __repr__(self):
        ...

    def __str__(self):
        ...



    def __lt__(self, another_cards):
        # different rank

        # same rank
        ...

    @staticmethod
    def tie_breaker(cards_one, cards_two):
        ...


    def get_card_order_by_value(self):
        ...


if __name__ == '__main__':
    #
    with open('poker.txt', 'r') as history:

