
import hashlib
import time

# ----- Classe Transaction -----
class Transaction:
    def __init__(self, from_addr, to_addr, amount):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount

# ----- Classe Block -----

class Block:
    def __init__(self, timestamp, transactions, previous_hash=''):
        self.timestamp = timestamp
        self.transactions = transactions  # Liste de transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.create_hash()

    def create_hash(self):
        block_string = (
            str(self.previous_hash)
            + str(self.timestamp)
            + str([t.__dict__ for t in self.transactions])
            + str(self.nonce)
        ).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.create_hash()
        print(f"Bloc mine ! Nonce={self.nonce}, Hash={self.hash}")


# ----- Classe Blockchain -----
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block("01/01/2020", [], "0")

    def get_last_block(self):
        return self.chain[-1]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        block = Block(time.time(), self.pending_transactions, self.get_last_block().hash)
        block.mine_block(self.difficulty)
        print("Bloc valide et ajoute a la chaine.")
        self.chain.append(block)

        # Réinitialise les transactions en attente avec la récompense pour le mineur
        self.pending_transactions = [
            Transaction(None, miner_address, self.mining_reward)
        ]

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            for trans in block.transactions:
                if trans.from_addr == address:
                    balance -= trans.amount
                if trans.to_addr == address:
                    balance += trans.amount
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.create_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

# ----- Section de test -----
if __name__ == "__main__":
    # Création de la blockchain
    mycoin = Blockchain()

    # Création de transactions
    mycoin.create_transaction(Transaction("Alice", "Bob", 50))
    mycoin.create_transaction(Transaction("Bob", "Charlie", 25))

    print("\n Debut du minage...")
    mycoin.mine_pending_transactions("Mineur1")

    print(f"\n Solde de Mineur1 : {mycoin.get_balance_of_address('Mineur1')}")
    print(" Deuxieme minage pour inclure la recompense precedente...")
    mycoin.mine_pending_transactions("Mineur1")

    print(f" Nouveau solde de Mineur1 : {mycoin.get_balance_of_address('Mineur1')}")

    print("\n Chaîne valide ?", mycoin.is_chain_valid())
