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

👤 Gestão de Usuário (CRUD Completo): Cadastro, Login com autenticação via SQLite, "Minha Conta" e recuperação de senha.

💳 Gestão de Pagamentos (CRUD de Cartões): Cadastro, listagem, edição e exclusão de cartões de crédito/débito com mascaramento de dados sensíveis.

🛡️ Área Administrativa: Painel restrito para monitoramento de usuários e status do sistema.

📍 Localização de Eletropostos: Listagem dinâmica de pontos de recarga em Recife-PE, exibindo endereço, status de ocupação (Disponível/Ocupado) e preço por kWh.

🗺️ Menu Principal: Interface HUB intuitiva que conecta o perfil do motorista aos serviços de geolocalização e financeiro.

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

🚗 Check-in de Veículos: Validação de bateria e alertas de segurança.

🔋 Simulação de Recarga: Contador em tempo real e integração total com o station manager.

📊 Comparador de Preços: Ferramenta para comparar tarifas entre eletropostos concorrentes.

🏢 Portal do Proprietário: Cadastro de novos eletropostos por terceiros e gestão de preços.

⸻

👨‍💻 Autoras

    Ana Caroline B. Nunes 
    Maria Heloísa D. Tavares
