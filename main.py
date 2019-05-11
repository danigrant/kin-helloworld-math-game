# This is the Kin SDK
import kin

# We'll be printing a few things to screen, so we also load pprint
from pprint import pprint

## for async await
import asyncio

## for random nums
import random

computer_account = ''
player_account = ''
player_keypair = ''

async def generate_math_problem():
    a = random.randint(2, 100) # between 2 and 100
    b = random.randint(2, 10)
    answer = input('{} x {} = '.format(a, b))
    await validate_math_answer(a, b, answer)

async def validate_math_answer(a, b, answer):
    if a * b == int(answer):
        # answer is correct
        print('🎉 correct! You get 10 Kin.')
        await transfer_kin()
    else:
        # answer is incorrect
        print('😳 not correct, the correct answer is {}'.format(a * b))
        await play_again()

async def setup_kin():
    client = kin.KinClient(kin.TEST_ENVIRONMENT)
    try:
        global computer_account
        global player_account
        global player_keypair
        keypair = kin.Keypair(seed="SAYWTBSMRBCPCATEPV3ETU5UVIWTBZJP53OBTEKVLSTLVZN7DPLMN3Z6")
        computer_account = client.kin_account(keypair.secret_seed)
        player_keypair = kin.Keypair()
        player_account = await computer_account.create_account(player_keypair.public_address, starting_balance=0, fee=100, memo_text='create player account')
    finally:
        await client.close()

async def transfer_kin():
    # async with kin.KinClient(kin.TEST_ENVIRONMENT) as client:
        # tx_hash = await computer_account.send_kin(player_keypair.public_address, amount=10, fee=100, memo_text='a prize!')
        # print('Sent 10 Kin to {}. Transaction hash: {}'. format(player_keypair.public_address, tx_hash))
    print('Successfully sent 10 Kin to {}.'. format(player_keypair.public_address))
    await play_again()

async def play_again():
    next_math_problem = input('Do you want to do another math problem? [y/n]:  ')
    if next_math_problem == 'y':
        await generate_math_problem()

# main
print('Welcome to Mathkin where you earn Kin by solving math problems.')
print('Hang on one moment while we setup your Kin account...')
asyncio.run(setup_kin())

print('We are Ready. Are you ready? 😻')

asyncio.run(generate_math_problem())
