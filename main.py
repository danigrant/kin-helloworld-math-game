# This is the Kin SDK
import kin

# We'll be printing a few things to screen, so we also load pprint
from pprint import pprint

## for async await
import asyncio

## for random nums
import random

computer_account
player_account
player_keypair

async def generate_math_problem():
    a = random.randint(2, 100) # between 2 and 100
    b = random.randint(2, 10)
    answer = input('{} x {} = '.format(a, b))
    await validate_math_answer(a, b, answer)

async def validate_math_answer(a, b, answer):
    if a * b == int(answer):
        # answer is correct
        print('correct')
        await transfer_kin()
    else:
        # answer is incorrect
        print('not correct, the correct answer is {}'.format(a * b))
        await play_again()

async def setup_kin():
    async with kin.KinClient(kin.TEST_ENVIRONMENT) as client:
        global computer_account
        global player_account
        global player_keypair
        keypair = kin.Keypair(seed="SDTOH63RNOSXHIHA6SPDGUTG5T4VYM4PQYY76AE4VC4EBEGIA2U73UOT")
        computer_account = client.kin_account(keypair.secret_seed)
        player_keypair = kin.Keypair()
        player_account = await computer_account.create_account(player_keypair.public_address, starting_balance=0, fee=100, memo_text='create player account')

async def transfer_kin():
    tx_hash = await computer_account.send_kin(player_account.public_address, amount=10, fee=100, memo_text='Hello World')
    print('Sent 10 Kin to {}. Transaction hash: {}'. format(player_account.public_address, tx_hash))
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
