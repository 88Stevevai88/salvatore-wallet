
import re

TOKEN_MAP = {
    "0x9d8c68f185a04314ddc8b8216732455e8dbb7e45": "LION",
    "0xf24409d155965ca87c45ad5bc084ad8ad3be4f39": "BARA",
    "0x96733708c4157218b6e6889eb9e16b1df7873061": "AGENTFUN",
    "0x9f3fbe80b822cd8fbe3dbaab845c9e77234eba5e": "BARA"
}

def estrai_token_da_input(input_data):
    if not input_data or input_data == "0x":
        return "Non rilevato"
    
    indirizzi = re.findall(r'(?<=000000000000000000000000)[0-9a-fA-F]{40}', input_data)
    for addr in indirizzi:
        token = TOKEN_MAP.get("0x" + addr.lower())
        if token:
            return token
    return "Non rilevato"
