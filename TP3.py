import hashlib


# Classe Block

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Ajout de l’attribut nonce
        self.hash = self.create_hash()

    def create_hash(self):
        # Calcule le hash du bloc
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        # Le hash doit commencer par un certain nombre de zéros
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.create_hash()
        print(f" Bloc miné ! Nonce : {self.nonce}, Hash : {self.hash}")



# Classe Blockchain (fusionnée)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Niveau de difficulté du minage

    def create_genesis_block(self):
        return Block(0, "2025-10-12", "Bloc de genèse", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.create_hash():
                print(f" Hash invalide pour le bloc {current.index}")
                return False
            if current.previous_hash != prev.hash:
                print(f" Mauvais lien entre les blocs {prev.index} et {current.index}")
                return False
        print(" La blockchain est valide !")
        return True



# Partie Test

if __name__ == "__main__":
    blockchain = Blockchain()

    blockchain.add_block(Block(1, "2025-10-31", "Transaction A → B : 50"))
    blockchain.add_block(Block(2, "2025-10-31", "Transaction B → C : 20"))

    print("\n=== Vérification de la validité de la blockchain ===")
    blockchain.is_chain_valid()

    # Falsification
    print("\n=== Falsification du bloc 1 ===")
    blockchain.chain[1].data = "Transaction A → B : 100"
    blockchain.chain[1].hash = blockchain.chain[1].create_hash()

    print("\n=== Vérification après falsification ===")
    blockchain.is_chain_valid()
