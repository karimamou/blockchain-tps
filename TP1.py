class Block: 
    def __init__(self, index, timestamp, data, previous_hash=''): 
        # Position du bloc dans la blockchain 
        self.index = index       
        # Date de création du bloc 
        self.timestamp = timestamp   
        # Données du bloc (transactions, etc.) 
        self.data = data  
        # Hachage du bloc précédent               
        self.previous_hash = previous_hash  
        # Hachage du bloc courant (à calculer ultérieurement) 
        self.hash = '' 

# Créer le bloc initial (genesis block)
genesis_block = Block(0, "2025-10-12 00:00", "Bloc de genèse", previous_hash="0")
# Chaîne sous forme de liste Python
blockchain = [genesis_block]
# Afficher le bloc de genèse
print("index:",genesis_block.index)
print("Timestamp:",genesis_block.timestamp)
print("Données:",genesis_block.data)
print("Previous Hash :",genesis_block.previous_hash)
print("Hash:",genesis_block.hash)

# Créer un second bloc 
bloc1 = Block(1, "2025-10-12 00:00", "Alice envoie 5 BTC",previous_hash=genesis_block.hash)
blockchain.append(bloc1)
 
# Afficher la chaîne de blocs
for bloc in blockchain: 
    print(f"Bloc {bloc.index} : prev_hash={bloc.previous_hash}, hash={bloc.hash}")