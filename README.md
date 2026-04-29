⚡ VoltLink

Projeto para Disciplina de PISI1.

⸻

📌 VoltLink

Projeto desenvolvido para a disciplina de PISI1, com o objetivo de facilitar a vida de motoristas de veículos elétricos em Recife-PE, permitindo gerenciar recargas, localizar eletropostos e simular pagamentos por meio de um sistema em Python executado no terminal.

⸻

🎯 Objetivo do projeto

Desenvolver um sistema robusto de gerenciamento de eletropostos que conecte usuários aos pontos de recarga, aplicando conceitos de persistência de dados, modularização de código e tratamento de erros, focado na experiência do usuário (UX) no terminal.

⸻

🚀 RELEASE 1.0 (Principais Features)

👤 Cadastro de usuários e veículos: Registro de múltiplos carros por perfil.
🔐 Sistema de login: Autenticação com validação via banco de dados.
📍 Mapa de Eletropostos: Listagem real de pontos de recarga em Recife-PE.
🔋 Check-in Inteligente: Validação de bateria (0-100%) com alertas de nível (🚨 Crítico, ⚠️ Médio, ✅ Seguro).
💳 Integração de Pagamento: Cálculo automático de kWh e simulação de transação financeira.
⏳ Simulação em tempo real: Contador progressivo de carga (animação de carregamento).
⭐ Sistema de Avaliações: Feedback dos usuários sobre as estações de recarga.
⚠️ Tratamento de Exceções: Validações rigorosas para evitar entradas inválidas (ex: bateria > 100%).

⸻

🛠️ Tecnologias utilizadas

    Python 3

    SQLite3 (Banco de Dados Relacional)

⸻

📚 Bibliotecas utilizadas

    sqlite3 → Armazenamento e persistência de dados de usuários, veículos e postos.

    time → Utilizada para o contador progressivo de carga e controle de tempo das animações.

    os → Limpeza do terminal (cls/clear), garantindo uma interface mais limpa.

    sys → Gestão de caminhos (paths) para garantir a modularização das pastas.

    random → Geração de dados aleatórios, para criar a simulação de distâncias (1km a 15km) entre o usuário e os eletropostos mais próximos na busca.
    
    urllib.parse → Formatação de endereços e coordenadas em formato string para permitir a criação funcional de links da API web do Google Maps.

⸻

💪 Desafios de Desenvolvimento (Destaques Técnicos)

    Station Manager: Foi o coração do projeto. Exigiu uma lógica complexa para integrar os dados geográficos dos postos com a capacidade técnica de cada veículo cadastrado.

    Integração Telas x Pagamento: O maior desafio foi garantir que o fluxo de dados entre a interface de usuário (ui) e a lógica de processamento de pagamento (core) ocorresse sem perda de integridade, assegurando que o valor só fosse cobrado após todas as validações de bateria.

⸻

📌 Como iniciar o projeto:

1.  Pré-requisitos: Certifique-se de ter a linguagem Python 3 instalada em seu ambiente.
2.  Preparação: Faça o clone do repositório na sua máquina.
3.  Acesso ao Diretório: Pelo terminal, navegue até a pasta raiz do projeto.
4.  Executar o sistema: Digite o comando abaixo e pressione Enter:
    
    python main.py
    
5.  Banco de Dados: Na primeira execução, o sistema gera o arquivo `voltlink.db` criando automaticamente todas as tabelas e inserindo postos de teste.

Nota: Você pode acessar inicialmente o Painel de Gestão fazendo login com o e-mail: `admin@voltlink.com` e a senha: `admin123`.

⸻

📌 Melhorias Futuras para a RELEASE 2.0

Gestão de Tarifas: Implementar uma função para que o administrador do posto possa definir e atualizar o preço por kWh.

Comparador de Preços: Criar uma funcionalidade de busca que liste os postos em ordem de preço, permitindo ao usuário comparar os valores dos concorrentes em Recife.

Sistema de Favoritos: Permitir que o motorista salve os eletropostos com melhor custo-benefício em sua conta.

⸻

👨‍💻 Autoras

    Ana Caroline B. Nunes 
    Maria Heloísa D. Tavares
