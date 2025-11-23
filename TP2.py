import hashlib
import json

# --- Partie 1 : Définition de la classe Block ---
class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # Calcul automatique du hash à la création du bloc
        self.hash = self.create_hash()

    def create_hash(self):
        # Concatène les attributs du bloc en une seule chaîne encodée
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}".encode()
        # Calcule et retourne le hachage SHA-256
        return hashlib.sha256(block_string).hexdigest()


# --- Partie 2 : Création et affichage de la blockchain ---
# Initialisation de la blockchain (liste de blocs)
blockchain = []

# Ajout du bloc de genèse
blockchain.append(Block(0, "2025-10-12", "Bloc de genèse", "0"))

# Ajout de quelques blocs supplémentaires
blockchain.append(Block(1, "2025-10-12", "Alice envoie 5 BTC", blockchain[0].hash))
blockchain.append(Block(2, "2025-10-12", "Bob envoie 3 BTC", blockchain[1].hash))

# Affichage de la blockchain au format JSON
print(json.dumps([b.__dict__ for b in blockchain], indent=4, ensure_ascii=False))


