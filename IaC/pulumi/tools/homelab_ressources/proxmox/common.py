

def get_mac_address(prefix, offset=0):
    # On décompose le préfixe en octets déjà définis
    parts = prefix.split(":")
    prefix_len = len(parts)

    if prefix_len >= 6:
        raise ValueError("Prefix must contain fewer than 6 octets.")

    # Nombre d'octets à compléter
    remaining = 6 - prefix_len

    # Base numérique pour commencer l'incrément
    max_value = 256 ** remaining

    if offset + 1 > max_value:
        raise ValueError("Requested number exceeds the available MAC space with this prefix.")
    
    block = []
    for _ in range(remaining):
        block.insert(0, f"{offset & 0xFF:02X}")
        offset >>= 8
    mac = parts + block
    return(":".join(mac))