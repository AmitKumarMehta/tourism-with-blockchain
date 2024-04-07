import hashlib
import json
from time import time

def transform_data(data):
    transformation_map = {
        'A': 'z', 'B': 'y', 'C': 'x', 'D': 'w', 'E': 'v', 'F': 'u', 'G': 't', 'H': 's', 'I': 'r', 'J': 'q',
        'K': 'p', 'L': 'o', 'M': 'n', 'N': 'm', 'O': 'l', 'P': 'k', 'Q': 'j', 'R': 'i', 'S': 'h', 'T': 'g',
        'U': 'f', 'V': 'e', 'W': 'd', 'X': 'c', 'Y': 'b', 'Z': 'a',
        '1': '9', '2': '8', '3': '7', '4': '6', '5': '5', '6': '4', '7': '3', '8': '2', '9': '1', '0': '0',
        'a': 'Z', 'b': 'Y', 'c': 'X', 'd': 'W', 'e': 'V', 'f': 'U', 'g': 'T', 'h': 'S', 'i': 'R', 'j': 'Q',
        'k': 'P', 'l': 'O', 'm': 'N', 'n': 'M', 'o': 'L', 'p': 'K', 'q': 'J', 'r': 'I', 's': 'H', 't': 'G',
        'u': 'F', 'v': 'E', 'w': 'D', 'x': 'C', 'y': 'B', 'z': 'A',
        '!': '~', '@': '`', '#': '!', '$': '*', '%': '$', '^': '#', '&': '%', '*': '^', '(': '&', ')': '(',
        '[': '}', ']': '{', '{': ']', '}': '[', '<': '>', '>': '<', '.': ',', ',': '.'
    }
    transformed_data = ''.join(transformation_map.get(char, char) for char in data)
    return transformed_data

# def transform_data(data):
#     transformation_map = {
#         'A': 'z', 'B': 'y', 'C': 'x', 'D': 'w', 'E': 'v', 'F': 'u', 'G': 't', 'H': 's', 'I': 'r', 'J': 'q',
#         'K': 'p', 'L': 'o', 'M': 'n', 'N': 'm', 'O': 'l', 'P': 'k', 'Q': 'j', 'R': 'i', 'S': 'h', 'T': 'g',
#         'U': 'f', 'V': 'e', 'W': 'd', 'X': 'c', 'Y': 'b', 'Z': 'a',
#         '1': '9', '2': '8', '3': '7', '4': '6', '5': '5', '6': '4', '7': '3', '8': '2', '9': '1', '0': '0'
#     }
#     transformed_data = ''.join(transformation_map.get(char, char) for char in data)
#     return transformed_data

def reverse_transform_data(data):
    reverse_transformation_map = {v: k for k, v in transformation_map.items()}
    original_data = ''.join(reverse_transformation_map.get(char, char) for char in data)
    return original_data

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else None,
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, data):
        transformed_data = {key: transform_data(value) if key in ['email', 'identity_card', 'contact_no', 'payment_id'] else value for key, value in data.items()}
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'data': transformed_data,
            'original_data': data
        })
        return self.last_block['index'] + 1

    def get_block_by_index(self, index):
        if 0 < index <= len(self.chain):
            return self.chain[index - 1]
        else:
            return None

    @staticmethod
    def hash(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

blockchain = Blockchain()

def get_user_input():
    email = input("Enter Your Email: ")
    identity_card = input("Enter Your Identity Card no: ")
    contact_no = input("Enter Your Contact number: ")
    payment_id = input("Enter Your Payment ID: ")
    return {
        'email': email,
        'identity_card': identity_card,
        'contact_no': contact_no,
        'payment_id': payment_id
    }

while True:
    user_data = get_user_input()
    blockchain.new_transaction("system", "user", user_data)
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    print("Previous Hash Value:", previous_hash)
    print("New Hash Value:", blockchain.hash(block))
    aa = input('''\nblock added! Do you want to show by index? (Enter index no or leave blank to exit)''')
    if aa.lower() != "":
        index = int(aa)
        if index == -1:
            break
        block = blockchain.get_block_by_index(index)
        if block:
            for transaction in block['transactions']:
                print("Transaction Data (Manipulated):", transaction['data'])
                print("Hash Value:", blockchain.hash(block))
                reveal_original = input("Do you want to reveal original data? (yes/no): ")
                if reveal_original.lower() == "yes":
                    print("Original Data:", transaction['original_data'])
            print("Hash Value:", blockchain.hash(block))
        else:
            print("Block not found!")
