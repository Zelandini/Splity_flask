import math
from domainmodel import models


def algo(users):
    net_balance = sum([user[1] for user in users])
    texts = []
    while net_balance != 0:
        amount_paid = sum([x[1] for x in users])
        average_share = amount_paid / len(users)
        print(amount_paid)
        debtors = []
        creditors = []
        print(users)
        for i in range(len(users)-1, -1, -1):
            users[i][1] -= average_share
            if users[i][1] < 0:
                debtors.append(users[i])
            elif users[i][1] > 0:
                creditors.append(users[i])
            else:
                users.pop(i)
        print("debtors ", end="")
        print(debtors)
        print("creditors ", end="")
        print(creditors)
        if debtors:
            largest_debtor = max(debtors, key=lambda x: x[1])
        else:
            largest_debtor = [[]]
        if creditors:
            largest_creditor = max(creditors, key=lambda d: d[1])
        else:
            largest_creditor = largest_debtor
        print(largest_creditor)
        amount_to_transfer = min(abs(largest_debtor[1]), abs(largest_creditor[1]))
        print(amount_to_transfer)
        print()
        for user in users:
            print(user)
            if user[0] == largest_creditor[0]:
                user[1] -= amount_to_transfer
            if user[0] == largest_debtor[0]:
                user[1] += amount_to_transfer
            print(user)
        print("user " + str(users))
        texts.append(f"{largest_debtor[0]} paid {amount_to_transfer} to {largest_creditor[0]}")
        net_balance = sum([abs(user[1]) for user in users])
        print(net_balance)
        print()
    print(texts)

user1 = ["Bob", 50]
user2 = ["David", 40]
user3 = ["Joe", 30]
user4 = ["Sam", 1000]
user5 = ["Bea", 400]
users_list = [user1, user2, user3, user4, user5]
algo(users_list)