from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction
from solders.pubkey import Pubkey
from solana.rpc.core import RPCException  # Impor RPCException

RPC_URL = "https://api.mainnet-beta.solana.com"

client = Client(RPC_URL)

sender_keypair = Keypair.from_base58_string("ENTER YOUR PRIVATE KEY")

receiver_address = Pubkey.from_string("ENTER RECEIVER ADDRESS")

amount_sol = 1

amount_lamports = int(amount_sol * 1_000_000_000)

transfer_instruction = transfer(TransferParams(
    from_pubkey=sender_keypair.pubkey(),
    to_pubkey=receiver_address,
    lamports=amount_lamports
))
transaction = Transaction().add(transfer_instruction)

recent_blockhash = client.get_latest_blockhash().value.blockhash

transaction.recent_blockhash = recent_blockhash
transaction.sign(sender_keypair)

try:
    response = client.send_raw_transaction(transaction.serialize())
    print(f"Transaction Signature: https://solscan.io/tx/{response.value}")
except RPCException as e:
    print(f"Error: {e}")