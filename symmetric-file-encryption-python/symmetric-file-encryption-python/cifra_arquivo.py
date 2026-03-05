#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cifra de arquivo texto com chave (128 e 256 bits) - modo didático com boas práticas:
- Derivação de chave a partir de senha (PBKDF2-HMAC-SHA256)
- Nonce (IV) aleatório
- Cifra tipo fluxo (XOR com keystream gerado via SHA-256)
- Autenticação (HMAC-SHA256) para detectar chave incorreta/arquivo alterado

Uso:
  Cifrar:
    python cifra_arquivo.py encrypt -i mensagem_original.txt -o mensagem_cifrada_128.txt -k 128
    python cifra_arquivo.py encrypt -i mensagem_original.txt -o mensagem_cifrada_256.txt -k 256

  Decifrar:
    python cifra_arquivo.py decrypt -i mensagem_cifrada_128.txt -o mensagem_decifrada.txt
    python cifra_arquivo.py decrypt -i mensagem_cifrada_256.txt -o mensagem_decifrada.txt

Observação:
- A senha é pedida no terminal (sem eco).
- O arquivo cifrado é salvo em BASE64 para ficar “texto” (não-binário).
"""

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os
import sys
from typing import Tuple


# ---------------------------
# Configurações do “formato” do arquivo cifrado
# ---------------------------
MAGIC = "TXTCRYPT1"          # Identificador do nosso formato
SALT_LEN = 16                # 16 bytes de salt (boa prática)
NONCE_LEN = 12               # nonce/IV (12 bytes é comum)
PBKDF2_ITERS = 200_000       # iterações PBKDF2 (segurança vs desempenho)


# ---------------------------
# Funções utilitárias
# ---------------------------
def die(msg: str, code: int = 1) -> None:
    """Encerra com mensagem de erro amigável."""
    print(f"[ERRO] {msg}", file=sys.stderr)
    sys.exit(code)


def read_file_bytes(path: str) -> bytes:
    """Lê arquivo como bytes com tratamento mínimo de erro."""
    if not os.path.isfile(path):
        die(f"Arquivo de entrada não encontrado: {path}")
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        die(f"Falha ao ler arquivo '{path}': {e}")


def write_file_bytes(path: str, data: bytes) -> None:
    """Grava arquivo como bytes com tratamento mínimo de erro."""
    try:
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        die(f"Falha ao gravar arquivo '{path}': {e}")


# ---------------------------
# Derivação de chaves a partir da senha (PBKDF2)
# ---------------------------
def derive_keys(password: str, salt: bytes, key_bits: int) -> Tuple[bytes, bytes]:
    """
    Deriva duas chaves a partir da senha:
    - enc_key: usada na cifra (16 bytes para 128-bit / 32 bytes para 256-bit)
    - mac_key: usada no HMAC (32 bytes fixos)

    Por que 2 chaves?
    - Boa prática: separar chave de cifra da chave de autenticação.
    """
    if key_bits not in (128, 256):
        die("Tamanho de chave inválido. Use 128 ou 256.")

    enc_len = 16 if key_bits == 128 else 32
    total_len = enc_len + 32  # +32 para mac_key

    # PBKDF2-HMAC-SHA256 (padrão e disponível na biblioteca padrão do Python)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERS,
        dklen=total_len
    )
    enc_key = dk[:enc_len]
    mac_key = dk[enc_len:]
    return enc_key, mac_key


# ---------------------------
# Geração de keystream (cifra de fluxo didática)
# ---------------------------
def keystream(enc_key: bytes, nonce: bytes, length: int) -> bytes:
    """
    Gera um fluxo de bytes pseudo-aleatório (keystream) de 'length' bytes.
    Fazemos blocos via SHA-256(enc_key || nonce || counter).

    Isso NÃO é AES/ChaCha20, mas é um modelo didático para entender:
    - Por que nonce/IV importa
    - Como o XOR com keystream cifra/decifra
    """
    out = bytearray()
    counter = 0

    while len(out) < length:
        counter_bytes = counter.to_bytes(4, "big")
        block = hashlib.sha256(enc_key + nonce + counter_bytes).digest()  # 32 bytes
        out.extend(block)
        counter += 1

    return bytes(out[:length])


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR byte a byte (tamanho igual)."""
    return bytes(x ^ y for x, y in zip(a, b))


# ---------------------------
# Cifra / Decifra
# ---------------------------
def encrypt(plaintext: bytes, password: str, key_bits: int) -> bytes:
    """
    Produz um “pacote” cifrado em JSON + BASE64.
    Inclui: magic, key_bits, salt, nonce, ciphertext, tag(HMAC)
    """
    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    enc_key, mac_key = derive_keys(password, salt, key_bits)

    ks = keystream(enc_key, nonce, len(plaintext))
    ciphertext = xor_bytes(plaintext, ks)

    # Autenticação: HMAC sobre os campos relevantes
    header = {
        "magic": MAGIC,
        "key_bits": key_bits,
        "salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "iters": PBKDF2_ITERS,
        "hash": "sha256",
    }

    # Montamos um “bytes_to_mac” estável (evita ambiguidade na serialização)
    header_bytes = json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    bytes_to_mac = header_bytes + b"." + ciphertext
    tag = hmac.new(mac_key, bytes_to_mac, hashlib.sha256).digest()

    package = {
        "header": header,
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
        "tag": base64.b64encode(tag).decode("ascii"),
    }

    # Salvamos como texto (JSON) e depois base64 “externo” (opcional, mas deixa tudo seguro em txt)
    raw_json = json.dumps(package, ensure_ascii=False, indent=2).encode("utf-8")
    return base64.b64encode(raw_json)


def decrypt(blob_b64: bytes, password: str) -> bytes:
    """
    Lê o “pacote” cifrado, valida HMAC e retorna o texto em claro.
    Se senha estiver errada (ou arquivo adulterado), dá erro.
    """
    try:
        raw_json = base64.b64decode(blob_b64)
        package = json.loads(raw_json.decode("utf-8"))
        header = package["header"]
        ciphertext = base64.b64decode(package["ciphertext"])
        tag = base64.b64decode(package["tag"])
    except Exception as e:
        die(f"Arquivo cifrado inválido/corrompido (falha ao parsear): {e}")

    if header.get("magic") != MAGIC:
        die("Formato inválido: MAGIC não confere (não é um arquivo gerado por este programa).")

    key_bits = int(header.get("key_bits", 0))
    iters = int(header.get("iters", 0))
    if iters != PBKDF2_ITERS:
        # Mantemos simples: esperamos o mesmo parâmetro do programa.
        # (Daria para aceitar iters do arquivo também.)
        die(f"Parâmetros inesperados: iters={iters}. (Esperado {PBKDF2_ITERS})")

    salt = base64.b64decode(header["salt"])
    nonce = base64.b64decode(header["nonce"])

    enc_key, mac_key = derive_keys(password, salt, key_bits)

    header_bytes = json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    bytes_to_mac = header_bytes + b"." + ciphertext
    expected_tag = hmac.new(mac_key, bytes_to_mac, hashlib.sha256).digest()

    # Comparação constante (evita leak por timing)
    if not hmac.compare_digest(tag, expected_tag):
        die("Chave/senha incorreta OU arquivo foi alterado (HMAC não confere).")

    ks = keystream(enc_key, nonce, len(ciphertext))
    plaintext = xor_bytes(ciphertext, ks)
    return plaintext


# ---------------------------
# CLI (linha de comando)
# ---------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cifra/Decifra arquivo texto com chave 128 ou 256 bits (didático)."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_enc = sub.add_parser("encrypt", help="Cifrar um arquivo .txt")
    p_enc.add_argument("-i", "--input", required=True, help="Arquivo de entrada (texto em claro)")
    p_enc.add_argument("-o", "--output", required=True, help="Arquivo de saída (texto cifrado)")
    p_enc.add_argument("-k", "--keybits", required=True, type=int, choices=[128, 256],
                       help="Tamanho da chave: 128 ou 256")

    p_dec = sub.add_parser("decrypt", help="Decifrar um arquivo gerado pelo programa")
    p_dec.add_argument("-i", "--input", required=True, help="Arquivo cifrado de entrada")
    p_dec.add_argument("-o", "--output", required=True, help="Arquivo de saída (texto decifrado)")

    args = parser.parse_args()

    # Solicita senha (sem mostrar)
    password = getpass.getpass("Digite a senha/chave: ").strip()
    if not password:
        die("Senha/chave vazia não é permitida. Defina uma senha com pelo menos 1 caractere.")

    if args.cmd == "encrypt":
        data = read_file_bytes(args.input)
        encrypted_b64 = encrypt(data, password, args.keybits)
        write_file_bytes(args.output, encrypted_b64)
        print(f"[OK] Arquivo cifrado gerado: {args.output} (chave {args.keybits} bits)")

    elif args.cmd == "decrypt":
        blob_b64 = read_file_bytes(args.input)
        plaintext = decrypt(blob_b64, password)
        write_file_bytes(args.output, plaintext)
        print(f"[OK] Arquivo decifrado gerado: {args.output}")

    else:
        die("Comando inválido.")


if __name__ == "__main__":
    main()