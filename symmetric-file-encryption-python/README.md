# 🔐 Symmetric File Encryption (128-bit / 256-bit)

> Projeto acadêmico que demonstra criptografia simétrica aplicada a arquivos texto, com suporte a chaves de **128 bits** e **256 bits**.

---

## ✨ Funcionalidades

- 📂 Leitura de arquivos `.txt`
- 🔒 Cifragem com senha definida pelo usuário
- 🔑 Suporte a chaves de **128 bits** e **256 bits**
- 🔓 Decifragem protegida por senha
- ✅ Verificação de integridade via **HMAC-SHA256**

---

## 📚 Conceitos abordados

Este projeto coloca em prática conceitos fundamentais de segurança da informação:

| Conceito | Descrição |
|---|---|
| **Criptografia Simétrica** | Mesma chave para cifrar e decifrar |
| **PBKDF2** | Derivação segura de chave a partir de senha |
| **Salt** | Valor aleatório para evitar ataques de dicionário |
| **Nonce (IV)** | Vetor de inicialização para garantir unicidade |
| **Keystream + XOR** | Geração e aplicação da cifra de fluxo |
| **HMAC-SHA256** | Autenticação e verificação de integridade |

---

## 🛠 Tecnologias

- **Python 3** — sem dependências externas

Bibliotecas padrão utilizadas: `hashlib`, `hmac`, `os`, `base64`, `argparse`

---

## 📁 Estrutura do projeto

```
symmetric-file-encryption-python/
│
├── src/
│   └── cifra_arquivo.py       # Código principal
│
├── examples/
│   ├── mensagem_original.txt
│   ├── mensagem_cifrada_128.txt
│   └── mensagem_cifrada_256.txt
│
├── docs/
│   └── algoritmo.md           # Documentação técnica detalhada
│
└── README.md
```

---

## ▶️ Como executar

### Cifrar um arquivo

```bash
# Com chave de 128 bits
python src/cifra_arquivo.py encrypt \
  -i examples/mensagem_original.txt \
  -o mensagem_cifrada_128.txt \
  -k 128

# Com chave de 256 bits
python src/cifra_arquivo.py encrypt \
  -i examples/mensagem_original.txt \
  -o mensagem_cifrada_256.txt \
  -k 256
```

### Decifrar um arquivo

```bash
python src/cifra_arquivo.py decrypt \
  -i mensagem_cifrada_128.txt \
  -o mensagem_decifrada.txt
```

> ⚠️ A senha incorreta resulta em falha de verificação do HMAC e o programa retorna erro imediatamente.

---

## 🔑 Como o algoritmo funciona

```
Senha do usuário
      │
      ▼
  PBKDF2 (+ salt aleatório)
      │
      ▼
  Chave criptográfica (128 ou 256 bits)
      │
      ▼
  SHA-256 (+ nonce aleatório) → Keystream
      │
      ▼
  Texto original XOR Keystream → Texto cifrado
      │
      ▼
  HMAC-SHA256 → Verificação de integridade
```

1. O usuário fornece uma senha
2. A senha é transformada em chave via **PBKDF2** com um **salt aleatório**
3. Um **nonce aleatório** é combinado à chave para gerar o **keystream** via SHA-256
4. O texto é cifrado aplicando **XOR** entre o conteúdo e o keystream
5. Um **HMAC-SHA256** é calculado para garantir integridade na decifragem

---

## 🎓 Objetivo acadêmico

Projeto desenvolvido para consolidar na prática:

- Funcionamento de criptografia simétrica
- Impacto do tamanho da chave (128 vs 256 bits)
- Controle de acesso baseado em senha
- Boas práticas básicas de implementação criptográfica

---

## 🚀 Possíveis melhorias

- [ ] Substituir keystream XOR por **AES** (padrão da indústria)
- [ ] Suporte a modos de operação como **CBC** e **GCM**
- [ ] Autenticação integrada (AEAD)
- [ ] Suporte a arquivos binários e de grande porte
- [ ] Interface gráfica (GUI)

---

## 👨‍💻 Autor

**Bruno Neemias**  
Estudante de Segurança da Informação
