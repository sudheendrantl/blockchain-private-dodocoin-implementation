from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json

from block import Block


class Node:
    def __init__(self, name, dodocoin, connected_node=None):
        self.node_name = name
        self.cryptocurrency = dodocoin
        self._chain = []

        # Problem Statement 3.a
        # adding a new variable to contain the number of transactions
        # in the block
        self.transaction_counter = 0

        # Problem Statement 4.a
        # Initialize the attribute connected_nodes as a blank list
        self.connected_nodes = []

        if connected_node is not None:
            self.connected_nodes.append(connected_node)

            # the following line of code ensures that caller is
            # connected to the called node and vice-versa
            # for e.g. if node3 initiates a connection with node1
            # then node1 marks node3 as one of its connected nodes too
            connected_node.connect_with_new_node(self)

        self._get_chain()

    def __str__(self):
        return f'\n-----Node summary-----' \
               f'\nNode - {self.node_name}' \
               f'\nNo of Connected nodes: {len(self.connected_nodes)}' \
               f'\nConnected nodes: {[item.node_name for item in self.connected_nodes]}' \
               f'\nTransaction Counter: {self.transaction_counter}' \
               f'\nNo of Blocks in node : {len(self._chain)}' \
               f'\nBlock chain - {self.get_chain_summary()}' \
               f'\nBlocks in node - \n{self._chain}' \
               f'\n-----Node summary ends-----\n'
        # return f'Node - {self.node_name} - Chain:\n{self._chain}'

    def __repr__(self):
        return self.__str__()

    def _get_chain(self, connected_node=None):
        # Problem Statement 4.b
        # Change the if statement to check for the length of connected_nodes
        if 0 == len(self.connected_nodes):
            if self.cryptocurrency.genesis_block is not None:
                self._chain.append(self.cryptocurrency.genesis_block)
        else:
            self._pull_chain_from_a_node(self.connected_nodes[0])

    def _pull_chain_from_a_node(self, node):
        self._chain = []
        if node:
            for chain_block in node._chain:
                self._chain.append(chain_block)

    def connect_with_new_node(self, node, sync_chain=False):

        # Problem Statement 4.c
        # Change the code to check for length and remove the unwanted code
        # Here as the parameter node is an instance of the class Node
        if node is not None:
            # self.connected_nodes.pop(0)
            if node not in self.connected_nodes:
                # as the node attempting to connect is not in the list
                # of connected nodes, we append the node to the connected_nodes list
                self.connected_nodes.append(node)
                # and also give the opportunity for the calling node to mark
                # the called node as a connected node too
                node.connect_with_new_node(self)

        if sync_chain is True:
            node_with_longest_chain = self._check_node_with_longest_chain()
            self._pull_chain_from_a_node(node_with_longest_chain)

    def _check_node_with_longest_chain(self):
        node_with_longest_chain = None
        chain_length = 0
        for node in self.connected_nodes:
            if len(node._chain) > chain_length:
                chain_length = len(node._chain)
                node_with_longest_chain = node
        return node_with_longest_chain

    def create_new_block(self):
        # Problem Statement 3.b.iv
        # Pass an argument current version to the block class
        new_block = Block(index=len(self._chain), transactions=self.cryptocurrency.mem_pool,
                          previous_block_hash=self._chain[-1].block_hash,
                          difficulty_level=self.cryptocurrency.difficulty_level,
                          version=self.cryptocurrency.current_version, metadata='')

        new_block.generate_hash()
        self._chain.append(new_block)
        self.cryptocurrency.mem_pool = []

        # Problem Statement 4.d
        # Change the code to check for length and remove the unwanted code
        if len(self.connected_nodes):
            self.propagate_new_block_to_connected_nodes(new_block)
        return new_block

    def show_chain(self):
        print(f"\nChain of node details - {self.node_name}")
        for chain_block in self._chain:
            print(chain_block)

    # added a new method of show the linked blocks visually
    # when the node summary is printed, this method is called to include the
    # blockchain summary too
    def get_chain_summary(self):
        return "".join(["Block" + str(self._chain[i]._index) + "->" for i in range(0, len(self._chain))])

    def add_new_transaction(self, transaction):
        try:
            self._validate_digital_signature(transaction)
        except InvalidSignature as e:
            print("\nInvalid signature. Cannot add this transaction")
            return

        if self._validate_receiver(transaction):
            transaction_bytes = transaction['transaction_bytes']
            transaction_data = json.loads(transaction_bytes)
            self.cryptocurrency.mem_pool.append(transaction_data)

    def _validate_digital_signature(self, transaction):
        sender_public_key = self.cryptocurrency.wallets[transaction['sender']]
        signature = transaction['signature']
        transaction_bytes = transaction['transaction_bytes']
        sender_public_key.verify(signature, transaction_bytes,
                                 padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                                 hashes.SHA256())

    def _validate_receiver(self, transaction):
        transaction_bytes = transaction['transaction_bytes']
        transaction_data = json.loads(transaction_bytes)
        # print(transaction_data)
        if transaction_data['receiver'] in self.cryptocurrency.wallets:
            return True
        return False

    def propagate_new_block_to_connected_nodes(self, new_block):
        for connected_node in self.connected_nodes:
            connected_node.add_new_block(new_block)

            for indirect_node in connected_node.connected_nodes:
                if new_block not in indirect_node._chain:
                    indirect_node.add_new_block(new_block)

    def add_new_block(self, new_block):
        if self.validate_block(new_block):
            self._chain.append(new_block)

    def show_connected_nodes(self):

        # Problem Statement 4.d
        # Change the code to check for length and remove the unwanted code
        if len(self.connected_nodes):
            print("\n-----------------------CONNECTED NODES INFO------------------------")
            print(f"{self.node_name} is connected with - ", end="")
            for _node in self.connected_nodes:
                print(_node.node_name, end=", ")
            print()

    # Problem Statement 2.a
    # Function to validate a block before it is propagated through the chain
    # Compare the hash of the last block of this chain against the previous_hash of the new block
    def validate_block(self, new_block):
        if len(self._chain):
            index = len(self._chain) - 1
            return self._chain[index].block_hash == new_block.get_previous_hash()
        else:
            return True


if __name__ == "__main__":
    from blockchain import DodoCoin
    from wallet import Wallet

    dodo = DodoCoin()
    node_1 = Node("Node_1", dodo)

    sunil_wallet = Wallet('Sunil', node_1)
    harsh_wallet = Wallet('Harsh', node_1)
    dodo.register_wallet(sunil_wallet.user, sunil_wallet.public_key)
    dodo.register_wallet(harsh_wallet.user, harsh_wallet.public_key)

    sunil_wallet.initiate_transaction("Harsh", 50)
    sunil_wallet.initiate_transaction("Harsh", 20)

    node_1.create_new_block()
    node_1.show_chain()

    node_2 = Node("Node_2", dodo, node_1)
    node_2.show_chain()

    dodo.update_difficulty_level(6)

    harsh_wallet.initiate_transaction("Sunil", 50)
    harsh_wallet.initiate_transaction("Sunil", 20)

    node_1.connect_with_new_node(node_2)
    node_1.create_new_block()
    node_1.show_chain()
    node_2.show_chain()
