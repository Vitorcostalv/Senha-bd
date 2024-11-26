### Gerenciador de Senhas 

#### **Sobre o Projeto**
Olá! Meu nome é vitor e eu desenvolvi este **Gerenciador de Senhas** para praticar o uso de Python com banco de dados SQLite. O objetivo principal foi criar uma ferramenta simples e segura para gerenciar senhas de usuários, além de implementar uma camada de administração. Aqui estão os principais recursos que incluí:

1. **Registro de Usuários**:
   - É possível registrar usuários com senhas automáticas (geradas aleatoriamente) ou manuais.
   - As senhas precisam ter, no máximo, 12 caracteres.

2. **Gerenciamento de Administradores**:
   - Os administradores têm acesso a funções avançadas, como listar, excluir e restaurar usuários.
   - Por segurança, o número de administradores é limitado a três.

3. **Recuperação e Exclusão**:
   - Quando um usuário é excluído, seus dados vão para uma tabela de "lixo", onde podem ser restaurados em até 3 dias.
   - Após esse período, os dados são excluídos permanentemente.

4. **Segurança**:
   - Todas as senhas são criptografadas usando SHA-256, então ninguém pode recuperá-las, apenas redefini-las.

Foi um exercício interessante para reforçar conhecimentos de segurança, banco de dados e manipulação de dados sensíveis.

---

#### **Como Configurar**
O projeto não usa bibliotecas externas, então tudo que você precisa é do Python instalado no seu computador. Aqui está o que fazer:

1. **Baixar o projeto**:
   ```bash
    git clone https://github.com/Vitorcostalv/Senha-bd
    cd Senha-bd

   ```

2. **Executar o código**:
   - Se já tiver Python instalado, basta rodar:
     ```bash
     python gerenciador_senhas.py
     ```

3. **Configuração inicial**:
   - Um administrador inicial será criado automaticamente:
     - Login: **adm**
     - Senha: **adm123**
   - Você pode alterar isso diretamente no código, se preferir.

---

#### **Como o Gerenciador Funciona**
Assim que o programa inicia, ele cria o banco de dados `senhas.db`, caso ainda não exista. A partir daí, você verá um menu com duas opções principais:

1. **Registrar**:
   - Aqui você pode registrar novos usuários. Se preferir, pode deixar o sistema gerar uma senha aleatória para você.
   - Também é possível listar a senha de um usuário existente (apenas se você souber o login).

2. **Administrador**:
   - É necessário autenticar-se como administrador para acessar funções avançadas:
     - Listar usuários cadastrados.
     - Excluir usuários (com possibilidade de restaurar em até 3 dias).
     - Registrar novos administradores (limitado a três).

---

#### **Por que Desenvolvi Este Projeto**
Eu queria criar algo prático e desafiador que também pudesse ser útil no dia a dia. Ao desenvolver, pratiquei conceitos importantes como:

- Criptografia de dados sensíveis.
- Manipulação de bancos de dados SQLite.
- Controle de acesso baseado em permissões.

#### **Informações adcionais**
Ainda pretendo implementar:

- Uma api para verificar o horário
- Uma interface grafica
- Adcionar mais funções 