import base64
import hashlib

def is_valid_onion_v3(address: str) -> bool:
  """
  Validates a Tor v3 onion address based on rend-spec-v3.
  Returns True if valid, False otherwise.
  """
  if not address.endswith(".onion"):
    return False

  raw_addres = address[:-6].upper()

  if len(raw_address) != 56:
    return False

  try:
    decoded = base64.b32decode(raw_address)
  except Exception:
    return False

  if len(decoded) != 35:
    return False

  pubkey = decoded[:32]
  checksum = decoded[32:34]
  version = decoded[34:35]

  if version != b"\x03":
    return False

  expected_checksum = hashlib.sha3_256(b".onion checksum" + pubkey + version).digest()[:2]

  return checksum == expected_checksum
