# ☁️🔐 cloud-security-siem-aws

> Implementação de uma solução de SIEM open-source com Graylog integrado ao ecossistema AWS, com coleta, análise e monitoramento de eventos de segurança em nuvem.

---

## 📋 Sobre o Projeto

Este projeto implementa uma solução de **SIEM (Security Information and Event Management)** utilizando o **Graylog** (open-source), hospedado em uma instância **Amazon EC2**, integrado a serviços da AWS para coleta, armazenamento, processamento e envio de alertas de segurança em tempo real.

Projeto acadêmico desenvolvido na disciplina de **Computação em Nuvem** — **FATEC Jundiaí** (2025).

---

## 🏗️ Arquitetura do Sistema

```
[ Geração de Logs ]
        │
        ▼
[ Amazon S3 (bucket) ]
        │
        ▼ (gatilho)
[ AWS Lambda ] ──────────► [ AWS SNS ] ──────────► [ Alerta por E-mail ]
        │
        ▼
[ Graylog Server (EC2) ]
        │
        ▼
[ MongoDB (armazenamento interno) ]
```

**Fluxo de dados:** Coleta → Normalização → Armazenamento → Análise → Alerta

---

## ☁️ Serviços AWS Utilizados

| Serviço | Função |
|---|---|
| **Amazon VPC** | Rede segura e isolada para todos os serviços |
| **Amazon EC2** (Ubuntu Server 24.04 LTS) | Hospedagem do Graylog |
| **Amazon S3** | Recebimento e armazenamento de logs |
| **AWS Lambda** | Processamento automatizado via gatilho S3 |
| **AWS SNS** | Envio de alertas por e-mail em tempo real |
| **IAM** | Controle de permissões e roles |

---

## 🛠️ Ferramentas e Tecnologias

| Ferramenta | Uso |
|---|---|
| **Graylog** | Plataforma SIEM open-source para centralização e análise de logs |
| **MongoDB** | Banco de dados NoSQL para armazenamento interno do Graylog |
| **PowerShell / SSH** | Acesso remoto à instância EC2 para configuração do ambiente |
| **Docker** | Implantação padronizada e portável do Graylog |

---

## ✅ Funcionalidades

- Coleta centralizada de logs de múltiplos serviços AWS
- Análise e correlação de eventos de segurança em tempo real
- Dashboard interativo no Graylog para visualização dos logs
- Gatilho automático via S3 + Lambda para processamento de logs
- Alertas enviados por e-mail via AWS SNS
- Rede isolada com Amazon VPC seguindo boas práticas de segurança

---

## 🧪 Fluxo de Teste

1. Script gera o log de evento
2. Valida a identidade via IAM Role
3. Envia o log para o bucket S3
4. S3 aciona o gatilho do AWS Lambda
5. Lambda processa e publica mensagem no SNS
6. SNS envia alerta por e-mail

---

## 🔒 Segurança e Permissões

Devido às restrições do ambiente **AWS Learn Lab**, não foi possível aplicar políticas IAM personalizadas. Em um ambiente real, seriam aplicadas boas práticas como:

- Princípio do menor privilégio
- Uso de roles específicas por serviço
- Rotação de credenciais
- Logs de auditoria via CloudTrail

---

## 🚀 Melhorias Futuras

- Integração com AWS CloudTrail e GuardDuty
- Políticas IAM personalizadas com menor privilégio
- Automação de respostas a incidentes (SOAR)
- Dashboards mais avançados com correlação de eventos
- Migração para ambiente EKS (Kubernetes)

---

## 📚 Referências

- [Documentação AWS Security Lake](https://aws.amazon.com/security-lake/)
- [Graylog Docker](https://github.com/Graylog2/graylog-docker)
- [Deploying Graylog in AWS EKS](https://github.com/pmaxtim/deploying_graylog_in_aws_eks)

---

## 👨‍💻 Autores

**Bruno Neemias Mota** • **Alex Santos da Silva** • **Melquisedec Souza Assunção**

Projeto desenvolvido para fins acadêmicos como Atividade Avaliativa Final da disciplina de Computação em Nuvem — **FATEC Jundiaí**, orientado pelo Prof. **Matheus Guilherme Fuini**.

[![GitHub](https://img.shields.io/badge/GitHub-brunoneemias-181717?style=flat&logo=github)](https://github.com/brunoneemias)

---

> 💡 Este repositório documenta a implementação de um SIEM com Graylog na AWS, aplicando conceitos de segurança em nuvem, integração de serviços e monitoramento de eventos em tempo real.
