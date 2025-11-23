from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import time

# Génération d'une paire de clés RSA (ici 4096 bits — remarque le commentaire ci-dessous)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096  # si tu veux 2048 remplace ici par 2048
)
public_key = private_key.public_key()
print("Les cles RSA ont ete generees avec succes !")

# Message à chiffrer
message = b"Blockchain et cryptographie asymetrique"

# --- Chiffrement (avec la clé publique) ---
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# --- Déchiffrement (avec la clé privée) ---
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Message initial  :", message)
print("Message dechiffre:", plaintext.decode())



#--------Exercice 2 : Signature numérique--------
message = b" Transaction : Alice -> Bob : 3 BTC"
# Signature avec la clé privée
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print("Signature (hex):", signature.hex()[:80],"...")
# Vérification de la signature 

try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature valide — le message est authentique.")
except Exception:
    print("Signature invalide.")


#Fonctions réutilisables 
# === Fonctions de signature et de vérification ===

def signer_message(privkey, msg: bytes) -> bytes:
    """Retourne la signature RSA du message donné."""
    return privkey.sign(
        msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )


def verifier_signature(pubkey, msg: bytes, sig: bytes) -> bool:
    """Retourne True si la signature est valide, False sinon."""
    try:
        pubkey.verify(
            sig,
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


# === Test ===

msg = b"Test de signature"
sig = signer_message(private_key, msg)
print("Valide ?", verifier_signature(public_key, msg, sig))

#---------------Exercice 3 : Arbre de Merkle

#1.Construction du Merkle Tree 

import hashlib


#   Fonctions utilitaires : hachage SHA-256


def sha256_hex(data: bytes) -> str:
    """Retourne le hash SHA-256 en hexadécimal."""
    return hashlib.sha256(data).hexdigest()


def hash_pair(left: str, right: str) -> str:
    """Concatène deux hash hex et renvoie le hash de la paire."""
    return sha256_hex(bytes.fromhex(left) + bytes.fromhex(right))



#   Construction du Merkle Tree


def make_leaf_hashes(transactions):
    """Hash chaque transaction pour créer les feuilles."""
    return [sha256_hex(tx.encode()) for tx in transactions]


def merkle_root(leaf_hashes):
    """Construit la racine Merkle à partir d'une liste de leaf hashes."""
    if not leaf_hashes:
        return ''

    current = leaf_hashes

    while len(current) > 1:
        # Si nombre impair, duplique la dernière feuille
        if len(current) % 2 == 1:
            current.append(current[-1])

        # Hash par paires
        current = [
            hash_pair(current[i], current[i + 1])
            for i in range(0, len(current), 2)
        ]

    return current[0]



#   Preuve d'inclusion (Merkle Proof)


def merkle_proof(leaf_hashes, index):
    """Construit la preuve Merkle pour une feuille donnée."""
    proof = []
    idx = index
    current = leaf_hashes.copy()

    while len(current) > 1:

        if len(current) % 2 == 1:
            current.append(current[-1])

        # Indice du frère (sibling)

        sibling_idx = idx ^ 1
        sibling_hash = current[sibling_idx]
        is_left = sibling_idx < idx

        proof.append((sibling_hash, is_left))

        # Passe au niveau supérieur
        idx //= 2
        current = [
            hash_pair(current[i], current[i + 1])
            for i in range(0, len(current), 2)
        ]

    return proof


def verify_proof(leaf_hash, proof, root):
    """Vérifie une preuve Merkle et reconstruit la racine attendue."""
    computed = leaf_hash

    for sibling, is_left in proof:
        if is_left:
            computed = hash_pair(sibling, computed)
        else:
            computed = hash_pair(computed, sibling)

    return computed == root



#   Exemple & tests


txs = ["Alice->Bob:5", "Bob->Charlie:3", "Dave->Eve:1"]

leaf_hashes = make_leaf_hashes(txs)
root = merkle_root(leaf_hashes)

print("Merkle Root :", root)

# Test d'une preuve
idx = 1  # vérifier la transaction "Bob->Charlie:3"
proof = merkle_proof(leaf_hashes, idx)

print("Transaction :", txs[idx])
print("Proof valide :", verify_proof(leaf_hashes[idx], proof, root))

#----Bloc signé avec Merkle Root
import time

class Block:
    def __init__(self, index, transactions, prev_hash, miner_private_key):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash

        # Calcul de la Merkle Root à partir des transactions
        self.merkle_root = merkle_root(make_leaf_hashes(transactions))

        # Construction du header du bloc
        header = f"{self.index}{self.timestamp}{self.merkle_root}{self.prev_hash}".encode()

        # Hash global du bloc
        self.hash = sha256_hex(header)

        # Signature du mineur (signature du hash du bloc)
        self.signature = signer_message(miner_private_key, self.hash.encode())

    def verify_block(self, miner_public_key):
        """Vérifie la signature et la validité interne du bloc."""
        
        # Recalcul du header pour vérifier l'intégrité
        header = f"{self.index}{self.timestamp}{self.merkle_root}{self.prev_hash}".encode()
        
        # Vérifier que la signature correspond bien au hash du bloc
        return verifier_signature(
            miner_public_key,
            sha256_hex(header).encode(),
            self.signature
        )


# =========================================================
# Simulation d'un bloc
# =========================================================

block = Block(
    1,
    ["Alice->Bob:2", "Bob->Charlie:1"],
    "000000abc",
    private_key
)

print("Hash du bloc     :", block.hash)
print("Merkle Root      :", block.merkle_root)
print("Signature valide :", block.verify_block(public_key))
