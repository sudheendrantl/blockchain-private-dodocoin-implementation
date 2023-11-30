from dodocoin.blockchain import DodoCoin
from dodocoin.wallet import Wallet
from dodocoin.node import Node

print("\nCreating a new dodocoin blockchain...")
dodo = DodoCoin()

print("\nAdding a few wallets...")
# Sudheendran - Forcing the generate_key flag to False, so that
# the private and public keys for peter are fetched from the default
# filenames stored in the current directory.
# The custom filenames are also used later in this file in
# line numbers 150-161. Please take note.
peter_wallet = Wallet('Peter', generate_key=False)
tony_wallet = Wallet('Tony')
strange_wallet = Wallet('Strange')
bruce_wallet = Wallet('Bruce')
steve_wallet = Wallet('Steve')
carol_wallet = Wallet('Carol')
scarlet_wallet = Wallet('Scarlet')
nebula_wallet = Wallet('Nebula')
natasha_wallet = Wallet("Natasha")
shuri_wallet = Wallet('Shuri')

# Register each wallet with Blockchain
print("\nRegistering the wallets into the dodocoin blockchain...")
dodo.register_wallet(peter_wallet.user, peter_wallet.public_key)
dodo.register_wallet(tony_wallet.user, tony_wallet.public_key)
dodo.register_wallet(strange_wallet.user, strange_wallet.public_key)
dodo.register_wallet(bruce_wallet.user, bruce_wallet.public_key)
dodo.register_wallet(steve_wallet.user, steve_wallet.public_key)
dodo.register_wallet(carol_wallet.user, carol_wallet.public_key)
dodo.register_wallet(scarlet_wallet.user, scarlet_wallet.public_key)
dodo.register_wallet(nebula_wallet.user, nebula_wallet.public_key)
dodo.register_wallet(natasha_wallet.user, natasha_wallet.public_key)
dodo.register_wallet(shuri_wallet.user, shuri_wallet.public_key)

print("\nCreating node_1 on the dodocoin blockchain...")
node_1 = Node("Node-1", dodo)

print("\nCreating node_2 on the dodocoin blockchain...")
node_2 = Node("Node-2", dodo)

print("\nPrinting details of node_1 and node_2 created...")
print(node_1)
print(node_2)

# Show list of registered wallets.
print("\nList of registered wallets...")
dodo.list_wallets()

print("\nCreating 1 transaction for peter/tony wallet and adding it to node_1...")
transaction = peter_wallet.initiate_transaction(tony_wallet.user, 20)
node_1.add_new_transaction(transaction)
print("\nList of pending transactions on the entire dodocoin blockchain...")
dodo.list_pending_transactions()

print("\nCreating new block on node 1...")
node_1.create_new_block()
print(node_1)

print("\nCreating new node node_2...")
node_2 = Node("Node-2", dodo)
print(node_2)

print("\nCreating 3 more transactions and adding them to node_1...")
transaction = peter_wallet.initiate_transaction(bruce_wallet.user, 25)
node_1.add_new_transaction(transaction)
transaction = bruce_wallet.initiate_transaction(peter_wallet.user, 50)
node_1.add_new_transaction(transaction)
transaction = tony_wallet.initiate_transaction(bruce_wallet.user, 50)
node_1.add_new_transaction(transaction)
print("\nAdding a block on node_1...")
node_1.create_new_block()

print("\nPrinting node_1 details...")
print(node_1)

print("\nCreating node_3 and attaching it to node_1 as a connected node...")
node_3 = Node("Node-3", dodo, node_1)
print(node_3)

print("\nAttaching the existing node_2 to node_1 as a connected node...")
node_2.connect_with_new_node(node_1, True)
print(node_2)

# no need to explicitly connect node_1 to node_2 and node_3, as they get
# connected to node_1 automatically when node_2 and node_3 got connected to node_1
# node_1.connect_with_new_node(node_2, True)
# node_1.connect_with_new_node(node_3, True)
# print(node_1)

node_1.show_connected_nodes()
node_2.show_connected_nodes()
node_3.show_connected_nodes()

print("\nCreating 1 more transaction and adding it to node_3...")
transaction = peter_wallet.initiate_transaction(bruce_wallet.user, 222)
node_3.add_new_transaction(transaction)
print("\nAdding a block on node_3...")
node_3.create_new_block()

print("\nPrinting the state of all 3 nodes...")
print(node_1)
print(node_2)
print(node_3)

# update difficulty level to 3 instead of 4
print("\nReducing difficulty level to 3 instead of 4 for dodocoin...")
dodo.update_difficulty_level(3)

print("\nCreating 1 more transaction and adding it to node_2...")
transaction = peter_wallet.initiate_transaction(bruce_wallet.user, 333)
node_2.add_new_transaction(transaction)
print("\nAdding a block on node_2...")
node_2.create_new_block()

print("\nPrinting the state of all 3 nodes...")
print(node_1)
print(node_2)
print(node_3)

# let us serialize the private and public keys using default named file
print("\nSerializing private key for peter wallet user...")
peter_wallet.serialize_private_key()

print("\nSerializing public key for peter wallet user...")
peter_wallet.serialize_public_key()

print("\nDeserializing private key for peter wallet user...")
peter_wallet.deserialize_private_key()

print("\nDeserializing public key for peter wallet user...")
peter_wallet.deserialize_public_key()

print("\nAfter serialization/deserialization lets initiate a transaction and create a block ...")

print("\nCreating 1 more transaction and adding it to node_1...")
transaction = peter_wallet.initiate_transaction(bruce_wallet.user, 444)
node_1.add_new_transaction(transaction)
print("\nAdding a block on node_1...")
node_1.create_new_block()

print("\nPrinting the state of all 3 nodes...")
print(node_1)
print(node_2)
print(node_3)

# let us serialize the private and public keys for custom named file
print("\nSerializing private key for peter wallet user...")
peter_wallet.serialize_private_key_to_file("peter.private.pem")

print("\nSerializing public key for peter wallet user...")
peter_wallet.serialize_public_key_to_file("peter.public.pem")

print("\nDeserializing private key for peter wallet user...")
peter_wallet.deserialize_private_key_from_file("peter.private.pem")

print("\nDeserializing public key for peter wallet user...")
peter_wallet.deserialize_public_key_from_file("peter.public.pem")

print("\nAfter serialization/deserialization lets initiate a transaction and create a block ...")

print("\nCreating 1 more transaction and adding it to node_1...")
transaction = peter_wallet.initiate_transaction(bruce_wallet.user, 555)
node_1.add_new_transaction(transaction)
print("\nAdding a block on node_1...")
node_1.create_new_block()

print("\nPrinting the state of all 3 nodes...")
print(node_1)
print(node_2)
print(node_3)

print("\nAssociating a node to a wallet so that there is no need to explicitly add new transaction ...")
peter_wallet.associate_with_node(node_1)

print("\nCreating 1 more transaction ...")
peter_wallet.initiate_transaction(bruce_wallet.user, 666)
# node_1.add_new_transaction(transaction)
print("\nAdding a block on node_1...")
node_1.create_new_block()

print("\nPrinting the state of all 3 nodes at the end...")
print(node_1)
print(node_2)
print(node_3)

print("All done!")
