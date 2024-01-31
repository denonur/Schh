# tip.py
from highrise import*
from highrise.models import*
from highrise.webapi import*

async def tip_user(highrise, user, amount):
    # checks if the bot has the amount
    bot_wallet = await highrise.get_wallet()
    bot_amount = bot_wallet.content[0].amount
    if bot_amount <= amount:
        await highrise.chat("Not enough funds")
        return

    # converts the amount to a string of bars and calculates the fee
    bars_dictionary = {
        10000: "gold_bar_10k",
        5000: "gold_bar_5000",
        1000: "gold_bar_1k",
        500: "gold_bar_500",
        100: "gold_bar_100",
        50: "gold_bar_50",
        10: "gold_bar_10",
        5: "gold_bar_5",
        1: "gold_bar_1"
    }

    fees_dictionary = {
        10000: 1000,
        5000: 500,
        1000: 100,
        500: 50,
        100: 10,
        50: 5,
        10: 1,
        5: 1,
        1: 1
    }

    # loop to check the highest bar that can be used and the amount of it needed
    tip = []
    total = 0
    for bar in bars_dictionary:
        if amount >= bar:
            bar_amount = amount // bar
            amount = amount % bar
            for _ in range(bar_amount):
                tip.append(bars_dictionary[bar])
                total = bar + fees_dictionary[bar]

    if total > bot_amount:
        await highrise.chat("Not enough funds")
        return

    for bar in tip:
        await highrise.tip_user(user.id, bar)
