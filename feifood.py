import os

# Arquivos
arq_usuarios = "usuarios.txt"
arq_alimentos = "alimentos.txt"
arq_pedidos = "pedidos.txt"
arq_itens_pedido = "pedidos_itens.txt"
arq_avaliacoes = "avaliacoes.txt"

# Autenticacao 

def cadastrar_usuario():
    print("\n--- Cadastro de Novo Usuário ---")
    login = input("Digite o nome de usuário (login): ").strip()
    senha = input("Digite a senha: ").strip()

    if not login or not senha:
        print("Login e senha não podem estar em branco.")
        return

    try:
        with open(arq_usuarios, "a", encoding="utf-8") as f:
            f.write(f"{login},{senha}\n")
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar usuário: {e}")

def login_usuario():
    print("\n--- Login de Usuário ---")
    login = input("Digite o nome de usuário (login): ").strip()
    senha = input("Digite a senha: ").strip()

    if not os.path.exists(arq_usuarios):
        print("Nenhum usuário cadastrado. Por favor, cadastre-se primeiro.")
        return None 

    try:
        with open(arq_usuarios, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    login_arq, senha_arq = partes
                    if login == login_arq and senha == senha_arq:
                        print(f"\nLogin bem-sucedido! Bem-vindo(a), {login_arq}!")
                        return login_arq 
            
            print("Usuário ou senha incorretos.")
            return None 
            
    except Exception as e:
        print(f"Erro ao ler arquivo de usuários: {e}")
        return None

# Alimentos 

def buscar_info_alimento(id_alimento_busca):
    try:
        with open(arq_alimentos, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) >= 4 and partes[0] == id_alimento_busca:
                    nome = partes[1]
                    preco = partes[-1]
                    return nome, preco
    except Exception:
        return None, None
    return None, None

#  Alimentos (Menu) 

def listar_alimentos():
    print("\n--- Cardápio Completo FEIFood ---")
    
    try:
        with open(arq_alimentos, "r", encoding="utf-8") as f: 
            print(f"{'ID':<3} | {'Nome':<20} | {'Preço (R$)':<10} | {'Descrição'}")
            print("-" * 65) 

            linhas = f.readlines()
            if not linhas:
                print("Cardápio vazio.")
                return

            for linha in linhas:
                partes = linha.strip().split(",")
                if len(partes) >= 4:
                    id_alimento = partes[0]
                    nome = partes[1]
                    preco = partes[-1] 
                    descricao = ",".join(partes[2:-1]) 
                    print(f"{id_alimento:<3} | {nome:<20} | {preco:<10} | {descricao}")
                else:
                    pass
            
    except Exception as e:
        print(f"Erro ao ler cardápio: {e}")

def buscar_alimento():
    print("\n--- Buscar Alimento ---")
    busca = input("Digite o nome (ou parte do nome) do alimento: ").lower().strip()

    encontrado = False
    try:
        with open(arq_alimentos, "r", encoding="utf-8") as f:
            print("\nResultados da busca:")
            print(f"{'ID':<3} | {'Nome':<20} | {'Preço (R$)':<10} | {'Descrição'}")
            print("-" * 65)

            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) >= 4:
                    id_alimento = partes[0]
                    nome = partes[1]
                    preco = partes[-1] 
                    descricao = ",".join(partes[2:-1]) 
                    
                    if busca in nome.lower():
                        print(f"{id_alimento:<3} | {nome:<20} | {preco:<10} | {descricao}")
                        encontrado = True
            
            if not encontrado:
                print("Nenhum alimento encontrado com esse nome.")
                
    except Exception as e:
        print(f"Erro ao buscar no cardápio: {e}")

#  Pedidos 

def obter_proximo_id_pedido():
    if not os.path.exists(arq_pedidos):
        return 1001 

    ultimo_id = 1000
    try:
        with open(arq_pedidos, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    try:
                        id_pedido = int(partes[0])
                        if id_pedido > ultimo_id:
                            ultimo_id = id_pedido
                    except ValueError:
                        continue 
        return ultimo_id + 1
    except Exception:
        return 1001 

def gerenciar_itens_pedido(id_pedido_atual):
    while True:
        print(f"\n--- Gerenciando Pedido Nº {id_pedido_atual} ---")
        print("1. Adicionar alimento ao pedido")
        print("2. Remover alimento do pedido")
        print("3. Ver itens do pedido")
        print("0. Concluir pedido (Voltar)")

        escolha_item = input("Escolha uma opção: ").strip()

        if escolha_item == '1':
            listar_alimentos() 
            id_alimento_add = input("Digite o ID do alimento que deseja ADICIONAR: ").strip()
            
            try:
                with open(arq_itens_pedido, "a", encoding="utf-8") as f:
                    f.write(f"{id_pedido_atual},{id_alimento_add}\n")
                print(f"Alimento (ID: {id_alimento_add}) adicionado ao pedido {id_pedido_atual}!")
            except Exception as e:
                print(f"Erro ao adicionar item: {e}")

        elif escolha_item == '2':
            id_alimento_rem = input("Digite o ID do alimento que deseja REMOVER: ").strip()
            
            itens_mantidos = []
            removido = False
            
            if not os.path.exists(arq_itens_pedido):
                print("Arquivo de itens não encontrado.")
                continue

            try:
                with open(arq_itens_pedido, "r", encoding="utf-8") as f:
                    for linha in f:
                        partes = linha.strip().split(",")
                        if len(partes) == 2:
                            id_ped, id_alim = partes
                            
                            if id_ped == str(id_pedido_atual) and id_alim == id_alimento_rem and not removido:
                                removido = True
                                continue 
                        
                        itens_mantidos.append(linha) 

                with open(arq_itens_pedido, "w", encoding="utf-8") as f:
                    f.writelines(itens_mantidos)
                
                if removido:
                    print(f"Alimento (ID: {id_alimento_rem}) removido do pedido {id_pedido_atual}.")
                else:
                    print("Item não encontrado nesse pedido.")

            except Exception as e:
                print(f"Erro ao remover item: {e}")

        elif escolha_item == '3':
            print(f"\n--- Itens no Pedido Nº {id_pedido_atual} ---")
            total_itens = 0
            if not os.path.exists(arq_itens_pedido):
                print("Pedido vazio.")
                continue
                
            try:
                with open(arq_itens_pedido, "r", encoding="utf-8") as f:
                    for linha in f:
                        partes = linha.strip().split(",")
                        if len(partes) == 2 and partes[0] == str(id_pedido_atual):
                            id_alim = partes[1]
                            nome_alim, preco_alim = buscar_info_alimento(id_alim)
                            if nome_alim:
                                print(f"   - {nome_alim} (R$ {preco_alim})")
                            else:
                                print(f"   - (Item ID: {id_alim} não encontrado)")
                            total_itens += 1
                if total_itens == 0:
                    print("Pedido vazio.")
            except Exception as e:
                print(f"Erro ao listar itens: {e}")

        elif escolha_item == '0':
            print(f"Pedido {id_pedido_atual} finalizado.")
            break
        else:
            print("Opção inválida.")


def criar_novo_pedido(usuario):
    print("\n--- Criando Novo Pedido ---")
    id_novo_pedido = obter_proximo_id_pedido()
    
    try:
        with open(arq_pedidos, "a", encoding="utf-8") as f:
            f.write(f"{id_novo_pedido},{usuario}\n")
        
        print(f"Pedido Nº {id_novo_pedido} criado para {usuario}.")
        gerenciar_itens_pedido(id_novo_pedido)
        
    except Exception as e:
        print(f"Erro ao criar novo pedido: {e}")

def ver_meus_pedidos(usuario):
    print(f"\n--- Pedidos de {usuario} ---")
    try:
        with open(arq_pedidos, "r", encoding="utf-8") as f_pedidos:
            pedidos_encontrados = False
            for linha_pedido in f_pedidos:
                partes_pedido = linha_pedido.strip().split(",")
                if len(partes_pedido) == 2 and partes_pedido[1] == usuario:
                    id_pedido = partes_pedido[0]
                    print(f"\n-- PEDIDO Nº {id_pedido} --")
                    pedidos_encontrados = True
                    
                    try:
                        with open(arq_itens_pedido, "r", encoding="utf-8") as f_itens:
                            itens_neste_pedido = 0
                            for linha_item in f_itens:
                                partes_item = linha_item.strip().split(",")
                                if len(partes_item) == 2 and partes_item[0] == id_pedido:
                                    id_alim = partes_item[1]
                                    nome_alim, preco_alim = buscar_info_alimento(id_alim)
                                    if nome_alim:
                                        print(f"   - {nome_alim} (R$ {preco_alim})")
                                    else:
                                        print(f"   - (Item ID: {id_alim} não encontrado)")
                                    itens_neste_pedido += 1
                            if itens_neste_pedido == 0:
                                print("   - Pedido vazio.")
                                
                    except FileNotFoundError:
                        print("   - Pedido vazio.")
            
            if not pedidos_encontrados:
                print("Você ainda não fez nenhum pedido.")
                
    except FileNotFoundError:
        print("Você ainda não fez nenhum pedido.")
    except Exception as e:
        print(f"Erro ao ler pedidos: {e}")

def excluir_pedido(usuario):
    ver_meus_pedidos(usuario)
    id_para_excluir = input("Digite o ID do pedido que deseja EXCLUIR: ").strip()
    
    pedido_valido = False
    pedidos_para_manter = [] 
    
    try:
        with open(arq_pedidos, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(",")
                
                if len(partes) == 2:
                    id_ped_arquivo = partes[0]
                    user_arquivo = partes[1]
                    
                    if id_ped_arquivo == id_para_excluir and user_arquivo == usuario:
                        pedido_valido = True
                    else:
                        pedidos_para_manter.append(linha)
                elif linha.strip(): 
                    pedidos_para_manter.append(linha)
                        
    except FileNotFoundError:
        print("Arquivo de pedidos não encontrado.")
        return

    if not pedido_valido:
        print("ID de pedido inválido ou não pertence a você.")
        return
    
    try:
        with open(arq_pedidos, "w", encoding="utf-8") as f:
            f.writelines(pedidos_para_manter)
    except Exception as e:
        print(f"Erro ao salvar o arquivo de pedidos: {e}")
        return

    linhas_mantidas = []
    try:
        with open(arq_itens_pedido, "r", encoding="utf-8") as f:
            for linha in f:
                if not linha.startswith(f"{id_para_excluir},"):
                    linhas_mantidas.append(linha)
        with open(arq_itens_pedido, "w", encoding="utf-8") as f:
            f.writelines(linhas_mantidas)
    except FileNotFoundError:
        pass 

    linhas_mantidas = []
    try:
        with open(arq_avaliacoes, "r", encoding="utf-8") as f:
            for linha in f:
                if not linha.startswith(f"{id_para_excluir},"):
                    linhas_mantidas.append(linha)
        with open(arq_avaliacoes, "w", encoding="utf-8") as f:
            f.writelines(linhas_mantidas)
    except FileNotFoundError:
        pass
        
    print(f"Pedido {id_para_excluir} excluído com sucesso.")

#  Avaliacoes 

def avaliar_pedido(usuario):
    print("\n--- Avaliar Pedido ---")
    ver_meus_pedidos(usuario)
    id_para_avaliar = input("Digite o ID do pedido que deseja AVALIAR: ").strip()

    pedido_valido = False
    try:
        with open(arq_pedidos, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    id_ped, user = partes
                    if id_ped == id_para_avaliar and user == usuario:
                        pedido_valido = True
                        break
    except FileNotFoundError:
        print("Arquivo de pedidos não encontrado.")
        return

    if not pedido_valido:
        print("ID de pedido inválido ou não pertence a você.")
        return
    
    while True:
        try:
            estrelas = int(input("Dê uma nota de 0 a 5 estrelas: "))
            if 0 <= estrelas <= 5:
                break
            else:
                print("Nota inválida. Digite um número entre 0 e 5.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
    
    try:
        with open(arq_avaliacoes, "a", encoding="utf-8") as f:
            f.write(f"{id_para_avaliar},{usuario},{estrelas}\n")
        print("Pedido avaliado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar avaliação: {e}")

# Menus 

def exibir_menu_inicial():
    print("\n--- BEM-VINDO AO FEIFOOD ---")
    print("1. Cadastrar novo usuário")
    print("2. Login de usuário") 
    print("0. Sair do sistema")
    try:
        escolha = int(input("Escolha uma opção: "))
        return escolha
    except ValueError:
        return -1 

def menu_gerenciar_pedidos(usuario):
    while True:
        print(f"\n--- Gerenciar Pedidos (Usuário: {usuario}) ---")
        print("1. Criar novo pedido")
        print("2. Ver meus pedidos")
        print("3. Excluir um pedido")
        print("0. Voltar ao menu principal")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            criar_novo_pedido(usuario)
        elif escolha == '2':
            ver_meus_pedidos(usuario)
        elif escolha == '3':
            excluir_pedido(usuario)
        elif escolha == '0':
            break 
        else:
            print("Opção inválida.")

def menu_principal_usuario(usuario):
    print(f"\n--- FEIFood (Logado como: {usuario}) ---")
    while True:
        print("\n1. Buscar por alimento")
        print("2. Listar todos os alimentos")
        print("3. Gerenciar meus pedidos (Criar, Editar, Excluir)")
        print("4. Avaliar um pedido")
        print("0. Deslogar (Voltar ao menu inicial)")
        
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            buscar_alimento() 
        elif escolha == '2':
            listar_alimentos() 
        elif escolha == '3':
            menu_gerenciar_pedidos(usuario)
        elif escolha == '4':
            avaliar_pedido(usuario)
        elif escolha == '0':
            print("Deslogando...")
            break 
        else:
            print("Opção inválida.")

#  Principal 

def main():
    while True:
        escolha_inicial = exibir_menu_inicial()
        
        if escolha_inicial == 1:
            cadastrar_usuario() 
            
        elif escolha_inicial == 2:
            usuario_logado = login_usuario() 
            if usuario_logado:
                menu_principal_usuario(usuario_logado)
                
        elif escolha_inicial == 0:
            print("Saindo do FEIFood... Até logo!")
            break 
            
        else:
            print("Opção inválida. Tente novamente.")

# Ponto de Entrada
if __name__ == "__main__":
    main()