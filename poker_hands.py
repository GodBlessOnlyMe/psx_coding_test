"""
해야할 일
- 같은 one pair일 때, highest value가 pair에 해당하는 값인지 다시 확
- get hand's rank
- invalid error raise(e.g. two royal flushes), 즉 Card shape의 order도 줘야하는지
- total_ordering decorator사용하면 더 편리
- private
- 주석
- type hinting
- 디버깅 모드
- if문의 순서가 확률적으로...
- 10이 있는데, poker data 주는 쪽에서 처리해서 줘야하지 않나
- card repr 바꾸기
- test case 만들기
"""


class Card:
    card_ranking = {
        "2": 0,
        "3": 1,
        "4": 2,
        "5": 3,
        "6": 4,
        "7": 5,
        "8": 6,
        "9": 7,
        "T": 8,
        "J": 9,
        "Q": 10,
        "K": 11,
        "A": 12,
    }

    def __init__(self, value_shape):
        self.value, self.shape = value_shape[0], value_shape[1]

    def __lt__(self, another_card):
        return self.card_ranking[self.value] < self.card_ranking[another_card.value]

    def __repr__(self):
        return f"{self.value}{self.shape}"


class Hand:
    hand_ranking = {
        "High Card": 0,
        "One Pair": 1,
        "Two Pairs": 2,
        "Three of a Kind": 3,
        "Straight": 4,
        "Flush": 5,
        "Full House": 6,
        "Four of a Kind": 7,
        "Straight Flush": 8,
        "Royal Flush": 9,
    }

    def __init__(self, *value_shapes):
        self.cards = sorted([Card(value_shape) for value_shape in value_shapes], reverse=True)
        self.values_counter = dict()
        self.shapes_counter = dict()
        for card in self.cards:
            if card.value in self.values_counter:
                self.values_counter[card.value] += 1
            else:
                self.values_counter[card.value] = 1
            if card.shape in self.shapes_counter:
                self.shapes_counter[card.shape] += 1
            else:
                self.shapes_counter[card.shape] = 1
        self.shape_repeated_count_descending = sorted(self.shapes_counter.values(), reverse=True)
        self.value_repeated_count_descending = sorted(self.values_counter.values(), reverse=True)
        self.rank = self.get_rank()

    def get_rank(self):
        is_flush = self.shape_repeated_count_descending[0] == 5
        first_frequent_value_count = self.value_repeated_count_descending[0]
        second_frequent_value_count = self.value_repeated_count_descending[1]
        if first_frequent_value_count == 1:
            if self.is_straight():
                if is_flush:
                    if "T" in self.values_counter and "A" in self.values_counter:
                        return "Royal Flush"
                    else:
                        return "Straight Flush"
                return "Straight"
            if is_flush:
                return "Flush"
            return "High Card"
        if first_frequent_value_count == 2:
            if second_frequent_value_count == 1:
                return "One Pair"
            if second_frequent_value_count == 2:
                return "Two Pairs"
        if first_frequent_value_count == 3:
            if second_frequent_value_count == 1:
                return "Three of a Kind"
            if second_frequent_value_count == 2:
                return "Full House"
        if first_frequent_value_count == 4:
            return "Four of a Kind"

    def is_straight(self):
        if ((Card.card_ranking[self.cards[1].value] - Card.card_ranking[self.cards[0].value] == 1) and
                (Card.card_ranking[self.cards[2].value] - Card.card_ranking[self.cards[1].value] == 1) and
                (Card.card_ranking[self.cards[3].value] - Card.card_ranking[self.cards[2].value] == 1) and
                (Card.card_ranking[self.cards[4].value] - Card.card_ranking[self.cards[3].value] == 1)):
            return True
        if ((self.cards[0].value == "2") and
                (self.cards[1].value == "3") and
                (self.cards[2].value == "4") and
                (self.cards[3].value == "5") and
                (self.cards[4].value == "A")):
            return True
        return False

    def __str__(self):
        return f"{self.cards}"

    def __lt__(self, another_hand):
        if self.hand_ranking[self.rank] < self.hand_ranking[another_hand.rank]:
            return True
        if self.hand_ranking[self.rank] > self.hand_ranking[another_hand.rank]:
            return False
        for ind in range(len(self.cards)):
            if self.cards[ind] < another_hand.cards[ind]:
                return True
            elif another_hand.cards[ind] < self.cards[ind]:
                return False


if __name__ == '__main__':
    nth_poker = 5
    result = 0

    with open('poker.txt', 'r') as history:
        for game in history.readlines():
            value_shapes = [x.replace("10", "T") for x in game.split()]
            player_1_value_shapes, player_2_value_shapes = value_shapes[:nth_poker], value_shapes[nth_poker:]
            player_1_hand, player_2_hand = Hand(*player_1_value_shapes), Hand(*player_2_value_shapes)
            print(player_1_hand, player_1_hand.rank)
            print(player_2_hand, player_2_hand.rank)
            print(f"Player 1 Win: {player_2_hand < player_1_hand}")
            print("-"*20)
            if player_2_hand < player_1_hand:
                result += 1

    print(result)
