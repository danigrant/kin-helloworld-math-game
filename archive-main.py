# This is the Kin SDK
import kin

# We'll be printing a few things to screen, so we also load pprint
from pprint import pprint

## for async await
import asyncio

async def kin_function():
    print('First we will create our KinClient object, and direct it to our test environment')
    async with kin.KinClient(kin.TEST_ENVIRONMENT) as client:

        print('\nEnvironment: ')
        print(client.environment)

        # Get keypair
        # Address: GABGTDCVQDME54Q2WMB45SNEYZN2WG4MLC2CPI35XQ6PMWAXDWNOI47A, Seed: SDTOH63RNOSXHIHA6SPDGUTG5T4VYM4PQYY76AE4VC4EBEGIA2U73UOT
        existing = input('Use existing seed? [y/n]:  ')
        if existing == 'y':
            seed = input('Input your seed: ')
            try:
                keypair = kin.Keypair(seed=seed)
            except kin.KinErrors.StellarSecretInvalidError:
                print('Your seed was not valid')
                raise
        else:
            print('\nNext we will generate a keypair')
            keypair = kin.Keypair()

        print('We are using the following keypair\n')
        print(keypair)

        print('Using the client, we can check if this account already exists on the blockchain')
        exist = await client.does_account_exists(keypair.public_address)
        if exist:
            print('The account already exist on the blockchain')
        else:
            print('The account does not exist on the blockchain')
            print('\nSince we are on the testnet blockchain, we can use the friendbot to create our account...\n')
            await client.friendbot(keypair.public_address)

        # Init KinAccount
        print('We can now create a KinAccount object, we will use it to interact with our account')
        account = client.kin_account(keypair.secret_seed)

        print('We can use our KinAccount object to get our balance')
        print('Our balance is {} KIN'.format(await account.get_balance()))

        # Create a different account
        print('\nWe will now create a different account')
        new_keypair = kin.Keypair()
        print('Creating account: {}'.format(new_keypair.public_address))
        tx_hash = await account.create_account(new_keypair.public_address, starting_balance=1000, fee=100, memo_text='Example')
        print('\nWe created the account and got the transaction id: {}'.format(tx_hash))

        # Get info about a tx
        print('\nWe can now use the client to get info about the transaction we did\n')
        transaction = await client.get_transaction_data(tx_hash=tx_hash)
        # We don't have __str__ for the transaction class, so we print it like this till we add it
        transaction.operation = vars(transaction.operation)
        pprint(vars(transaction))

        tx_hash = await account.send_kin(new_keypair.public_address, amount=10, fee=100, memo_text='Hello World')
        print('The transaction succeeded with the hash {}'.format(tx_hash))

asyncio.run(kin_function())
