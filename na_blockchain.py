import hashlib
import json
from time import time

class BlockchainNA:
    def __init__(self, creator_address):
        self.chain = []
        self.pending_transactions = []
        self.creator_address = creator_address
        
        # --- RÈGLES ÉCONOMIQUES ET SÉCURITÉ ---
        self.MAX_SUPPLY = 10_000_000       # Limite absolue : 10M NA
        self.total_minted = 0              # Quantité totale créée
        self.total_volume_chf = 0.0        # Volume cumulé d'échanges
        self.VOLUME_THRESHOLD_CHF = 10000.0 # Seuil de décentralisation (10 000 CHF)
        self.is_locked = False             # État du verrouillage d'administration
        
        # --- RÈGLES ANTI-BALEINE ---
        self.MAX_WALLET_LIMIT = 200_000    # Max 2% par portefeuille
        self.MAX_TX_LIMIT = 50_000         # Max par transaction

        # Genesis Block + Allocation initiale (100 NA pour démarrer)
        self.mint_na(self.creator_address, 100)
        self.create_block(previous_hash="0")

    def get_balance(self, address):
        """Calcule le solde actuel d'un portefeuille."""
        balance = 0
        for block in self.chain:
            for tx in block['transactions']:
                if tx['recipient'] == address:
                    balance += tx['amount']
                if tx['sender'] == address:
                    balance -= tx['amount']
        for tx in self.pending_transactions:
            if tx['recipient'] == address:
                balance += tx['amount']
            if tx['sender'] == address:
                balance -= tx['amount']
        return balance

    def mint_na(self, recipient, amount):
        """Création de nouveaux NA (Seulement possible avant le verrouillage)."""
        if self.is_locked:
            print("[SÉCURITÉ] La blockchain est verrouillée. Impossible de générer des NA !")
            return False

        if self.total_minted + amount > self.MAX_SUPPLY:
            print("[ERREUR] Limite maximale de 10 millions de NA atteinte !")
            return False

        # Vérification Anti-Baleine
        recipient_balance = self.get_balance(recipient)
        if recipient_balance + amount > self.MAX_WALLET_LIMIT:
            print(f"[ANTI-BALEINE] Transaction refusée. {recipient} dépasserait la limite de 200 000 NA !")
            return False

        self.pending_transactions.append({
            'sender': "MINT_SYSTEM",
            'recipient': recipient,
            'amount': amount,
            'chf_value': 0
        })
        self.total_minted += amount
        return True

    def transfer(self, sender, recipient, amount_na, estimated_chf_value):
        """Effectue une transaction entre deux utilisateurs."""
        # Check limites Anti-Baleine
        if amount_na > self.MAX_TX_LIMIT:
            print(f"[ANTI-BALEINE] Impossible d'envoyer plus de {self.MAX_TX_LIMIT} NA d'un coup !")
            return False

        if self.get_balance(sender) < amount_na:
            print("[ERREUR] Solde insuffisant.")
            return False

        recipient_balance = self.get_balance(recipient)
        if recipient_balance + amount_na > self.MAX_WALLET_LIMIT:
            print("[ANTI-BALEINE] Le destinataire dépasserait la limite de 2 % de la masse totale !")
            return False

        # Ajout de la transaction
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount_na,
            'chf_value': estimated_chf_value
        })

        # Suivi du volume total d'échanges
        self.total_volume_chf += estimated_chf_value
        print(f"Transaction enregistrée. Volume cumulé : {self.total_volume_chf:.2f} CHF / {self.VOLUME_THRESHOLD_CHF:.2f} CHF")

        # Vérification du passage au mode autonome
        if self.total_volume_chf >= self.VOLUME_THRESHOLD_CHF and not self.is_locked:
            self.auto_decentralize()

        return True

    def auto_decentralize(self):
        """Réajuste le compte du créateur à 5% max et verrouille le système."""
        print("\n" + "="*50)
        print("SEUIL DES 10 000 CHF ATTEINT : DÉCENTRALISATION EN COURS")
        print("="*50)

        creator_bal = self.get_balance(self.creator_address)
        max_allowed = self.total_minted * 0.05  # Pile 5 % de ce qui est créé

        # Si le créateur a plus de 5 %, on détruit le surplus
        if creator_bal > max_allowed:
            surplus = creator_bal - max_allowed
            self.pending_transactions.append({
                'sender': self.creator_address,
                'recipient': "BURN_ADDRESS",
                'amount': surplus,
                'chf_value': 0
            })
            print(f"[AJUSTEMENT] {surplus} NA en trop ont été brûlés du compte créateur.")

        self.is_locked = True
        print("[SÉCURITÉ] La NA est désormais 100 % autonome. Plus aucune création possible !\n")

    def create_block(self, previous_hash=None):
        """Valide et enregistre les transactions dans un nouveau bloc."""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else "0"
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


# --- TEST ET DÉMONSTRATION ---
if __name__ == "__main__":
    # Lancement avec ton adresse
    na_coin = BlockchainNA(creator_address="Ali_Creator")

    print(f"Solde de départ Ali: {na_coin.get_balance('Ali_Creator')} NA")

    # Génération initiale pour le test entre amis
    na_coin.mint_na("Ali_Creator", 150_000) # Tu te génères un stock initial
    na_coin.mint_na("Ami_1", 20_000)
    na_coin.create_block()

    print(f"Solde Ali après MINT: {na_coin.get_balance('Ali_Creator')} NA")

    # Test d'une transaction avec valeur CHF
    # (Exemple: Ali vend 5 000 NA à Ami_2 pour un équivalent de 50 CHF)
    na_coin.transfer(sender="Ali_Creator", recipient="Ami_2", amount_na=5000, estimated_chf_value=50.0)
    na_coin.create_block()
