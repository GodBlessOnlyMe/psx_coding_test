"""
생각한 점
- Shape에 order가 없으면(e.g.
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

"""
rank에 사용된 card먼저 비교해야함
따라서, rank에 사용된 카드의 index를 알아야함


"""


class Card:
    card_ranking = {**{str(x): x for x in range(2, 10, 1)},
                    **{"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}}

    def __init__(self, value_shape):
        self.value, self.shape = value_shape[0], value_shape[1]

    def __lt__(self, another_card):
        return self.card_ranking[self.value] < self.card_ranking[another_card.value]

    def __repr__(self):
        return f"{self.value}{self.shape}"


class FivePokerHand:
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
        self.cards = []
        self.value_to_count = dict()
        self.shape_to_count = dict()
        for value_shape in value_shapes:
            self.cards.append(Card(value_shape))
            value, shape = value_shape[0], value_shape[1]
            if value in self.value_to_count:
                self.value_to_count[value] += 1
            else:
                self.value_to_count[value] = 1
            if shape in self.shape_to_count:
                self.shape_to_count[shape] += 1
            else:
                self.shape_to_count[shape] = 1
        self.rank = self.get_rank()

    def get_rank(self):
        is_flush = len(self.shape_to_count) == 1
        first_frequent_count = 0
        second_frequent_count = 0
        for value, count in self.value_to_count.items():
            if first_frequent_count < count:
                first_frequent_count = count
            else:
                if second_frequent_count < count:
                    second_frequent_count = count
        if first_frequent_count == 1:
            if self.is_straight():
                if is_flush:
                    if "T" in self.value_to_count and "A" in self.value_to_count:
                        return "Royal Flush"
                    else:
                        return "Straight Flush"
                return "Straight"
            if is_flush:
                return "Flush"
            return "High Card"
        if first_frequent_count == 2:
            if second_frequent_count == 1:
                return "One Pair"
            if second_frequent_count == 2:
                return "Two Pairs"
        if first_frequent_count == 3:
            if second_frequent_count == 1:
                return "Three of a Kind"
            if second_frequent_count == 2:
                return "Full House"
        if first_frequent_count == 4:
            return "Four of a Kind"

    def is_straight(self):
        if ((Card.card_ranking[self.cards[1].value] - Card.card_ranking[self.cards[0].value] == 1) and
                (Card.card_ranking[self.cards[2].value] - Card.card_ranking[self.cards[1].value] == 1) and
                (Card.card_ranking[self.cards[3].value] - Card.card_ranking[self.cards[2].value] == 1) and
                (Card.card_ranking[self.cards[4].value] - Card.card_ranking[self.cards[3].value] == 1)):
            return True
        return self.value_to_count == {value: 1 for value in ['A', '2', '3', '4', '5']}

    def get_paired_preceeding_cards(self, pair_count):
        paired_cards = []
        unpaired_cards = []
        for card in self.cards:
            if self.value_to_count[card.value] == pair_count:
                paired_cards.append(card)
            else:
                unpaired_cards.append(card)
        return paired_cards + unpaired_cards

    def get_rearranged_cards_by_rank_case(self):
        if self.rank in ("High Card", "Flush", "Royal Flush"):
            self.cards = sorted(self.cards, reverse=True)
            return self.cards
        elif self.rank in ("One Pair", "Two Pairs", "Three of a Kind"):
            self.cards = sorted(self.cards, reverse=True)
            return self.get_paired_preceeding_cards(2)
        elif self.rank in ("Straight", "Straight Flush"):
            self.cards = sorted(self.cards, reverse=True)
            if self.value_to_count == {value: 1 for value in ['A', '2', '3', '4', '5']}:
                # self.cards = ['A', '5', '4', '3', '2']
                # rearranged = ['5', '4', '3', '2', 'A']
                return self.cards[1:] + self.cards[:1]
            return self.cards
        elif self.rank == "Full House":
            return self.get_paired_preceeding_cards(3)
        elif self.rank == "Four of a Kind":
            return self.get_paired_preceeding_cards(4)
        else:
            raise ValueError(f"{self.rank} is not appropriate.")

    def __str__(self):
        return f"{self.cards}"

    def __lt__(self, another_hand):
        if self.hand_ranking[self.rank] < self.hand_ranking[another_hand.rank]:
            return True
        if self.hand_ranking[self.rank] > self.hand_ranking[another_hand.rank]:
            return False

        rearranged_cards = self.get_rearranged_cards_by_rank_case()
        another_rearranged_cards = another_hand.get_rearranged_cards_by_rank_case()
        for ind in range(5):
            if rearranged_cards[ind] < another_rearranged_cards[ind]:
                return True
            if another_rearranged_cards[ind] < rearranged_cards[ind]:
                return False
        else:
            raise ValueError(f"{self.cards} and {another_hand.cards} makes split")


if __name__ == '__main__':
    # file_name = 'poker_test_1'
    file_name = 'poker.txt'
    # file_name = 'poker_test_2'
    result = 0

    with open(file_name, 'r') as history:
        for game in history.readlines():
            value_shapes = [x.replace("10", "T") for x in game.split()]
            player_1_value_shapes, player_2_value_shapes = value_shapes[:5], value_shapes[5:]
            player_1_hand, player_2_hand = FivePokerHand(*player_1_value_shapes), FivePokerHand(*player_2_value_shapes)
            print(player_1_hand, player_1_hand.rank)
            print(player_2_hand, player_2_hand.rank)
            # print(f"Player 1 Win: {player_2_hand < player_1_hand}")
            # print("-"*20)
            if player_2_hand < player_1_hand:
                result += 1

    print(result)
