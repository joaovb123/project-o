import models

def validar_nao_vazio(texto):
    return texto.strip() != ""

def validar_nota(valor):
    try:
        nota = float(valor)
        return 0 <= nota <= 10
    except ValueError:
        return False

def validar_duracao(valor):
    try:
        duracao = int(valor)
        return duracao > 0
    except ValueError:
        return False

def formatar_titulo(titulo):
    return titulo.strip().title()

def obter_entrada_valida(mensagem, validacao_func):
    while True:
        entrada = input(mensagem)
        if validacao_func(entrada):
            return entrada
        print("Valor inválido. Tente novamente.")

def exibir_menu_principal():
    print("\n" + "="*50)
    print("SISTEMA DE AVALIAÇÃO DE FILMES")
    print("="*50)
    print("1. Cadastrar filme")
    print("2. Avaliar filme")
    print("3. Estatísticas")
    print("4. Recomendações")
    print("5. Relatórios")
    print("6. Listar todos os filmes")
    print("7. Sair")
    print("="*50)

def cadastrar_filme():
    print("\n--- CADASTRO DE FILME ---")
    
    titulo = input("Título: ").strip()
    if not titulo:
        print("Título inválido.")
        return
    
    if models.verificar_duplicidade(titulo):
        print("Erro: Já existe um filme com este título cadastrado.")
        return
    
    genero = input("Gênero: ").strip()
    if not genero:
        print("Gênero inválido.")
        return
    
    duracao = obter_entrada_valida("Duração (minutos): ", validar_duracao)
    
    models.adicionar_filme(titulo, genero, int(duracao))
    print(f"Filme '{formatar_titulo(titulo)}' cadastrado com sucesso!")

def avaliar_filme():
    print("\n--- AVALIAÇÃO DE FILME ---")
    
    if not models.listar_filmes():
        print("Nenhum filme cadastrado ainda. Cadastre um filme primeiro.")
        return
    
    print("\nFilmes disponíveis para avaliação:")
    filmes = models.listar_filmes()
    for i, filme in enumerate(filmes, 1):
        print(f"{i}. {formatar_titulo(filme['titulo'])} - {filme['genero'].upper()}")
    
    titulo = input("\nTítulo do filme: ").strip()
    if not titulo:
        print("Título inválido.")
        return
    
    filme = models.buscar_filme_por_titulo(titulo)
    if not filme:
        print("Filme não encontrado.")
        return
    
    nota = obter_entrada_valida("Nota (0-10): ", validar_nota)
    nota_float = float(nota)
    
    print(f"Preview: {models.formatar_nota_estrelas(nota_float)}")
    
    confirmar = input("Confirmar avaliação? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Avaliação cancelada.")
        return
    
    comentario = input("Comentário (opcional): ").strip()
    
    models.registrar_avaliacao(titulo, nota_float, comentario)
    print(f"Avaliação para '{formatar_titulo(titulo)}' registrada com sucesso!")

def exibir_estatisticas():
    print("\n--- ESTATÍSTICAS ---")
    
    media_geral = models.calcular_media_geral()
    print(f"Média geral de avaliações: {models.formatar_nota_estrelas(media_geral)}")
    
    melhor, pior = models.obter_extremos()
    if melhor and pior:
        print(f"\nMelhor avaliado: {formatar_titulo(melhor['titulo'])}")
        print(f"  Nota: {models.formatar_nota_estrelas(melhor['nota'])}")
        if melhor['comentario']:
            print(f"  Comentário: {melhor['comentario']}")
        
        print(f"\nPior avaliado: {formatar_titulo(pior['titulo'])}")
        print(f"  Nota: {models.formatar_nota_estrelas(pior['nota'])}")
        if pior['comentario']:
            print(f"  Comentário: {pior['comentario']}")
    else:
        print("\nNenhuma avaliação registrada ainda.")

def exibir_recomendacoes():
    print("\n--- RECOMENDAÇÕES ---")
    
    if not models.listar_filmes():
        print("Nenhum filme cadastrado ainda.")
        return
    
    genero = input("Digite o gênero para recomendação: ").strip()
    if not genero:
        print("Gênero inválido.")
        return
    
    nota_minima = obter_entrada_valida("Nota mínima (0-10): ", validar_nota)
    nota_minima = float(nota_minima)
    
    recomendacoes = models.recomendar_top_3(genero, nota_minima)
    
    if recomendacoes:
        print(f"\nTop 3 filmes do gênero '{genero}' com nota ≥ {nota_minima:.1f}:")
        for i, rec in enumerate(recomendacoes, 1):
            print(f"{i}. {formatar_titulo(rec['titulo'])}")
            print(f"   {models.formatar_nota_estrelas(rec['nota'])}")
            if rec['comentario']:
                print(f"   Comentário: {rec['comentario']}")
    else:
        print(f"Nenhum filme do gênero '{genero}' com nota ≥ {nota_minima:.1f} encontrado.")

def exibir_relatorios():
    print("\n--- RELATÓRIOS ---")
    print("1. Ranking geral de filmes")
    print("2. Panorama por gênero")
    
    opcao = input("Escolha uma opção: ").strip()
    
    if opcao == "1":
        ranking = models.gerar_ranking_geral()
        if ranking:
            print("\n=== RANKING GERAL DE FILMES ===")
            for i, filme in enumerate(ranking, 1):
                print(f"{i}. {formatar_titulo(filme['titulo'])}")
                print(f"   {models.formatar_nota_estrelas(filme['media'])}")
        else:
            print("Nenhuma avaliação registrada ainda.")
    
    elif opcao == "2":
        panorama = models.gerar_panorama_por_genero()
        if panorama:
            print("\n=== PANORAMA POR GÊNERO ===")
            for gen in panorama:
                print(f"\nGênero: {gen['genero'].upper()}")
                print(f"  Média: {models.formatar_nota_estrelas(gen['media'])}")
                print(f"  Total de filmes: {gen['total_filmes']}")
                print(f"  Total de avaliações: {gen['total_avaliacoes']}")
        else:
            print("Nenhum filme cadastrado ainda.")
    else:
        print("Opção inválida.")

def listar_filmes_com_avaliacoes():
    print("\n--- LISTA COMPLETA DE FILMES ---")
    
    filmes = models.listar_filmes()
    if not filmes:
        print("Nenhum filme cadastrado.")
        return
    
    for filme in filmes:
        print(f"\n{formatar_titulo(filme['titulo'])}")
        print(f"  Gênero: {filme['genero'].upper()}")
        print(f"  Duração: {filme['duracao']} minutos")
        
        avaliacoes_filme = [a for a in models.listar_avaliacoes() 
                           if a['titulo'] == filme['titulo']]
        
        if avaliacoes_filme:
            print("  Avaliações:")
            for av in avaliacoes_filme:
                print(f"    {models.formatar_nota_estrelas(av['nota'])}")
                if av['comentario']:
                    print(f"      Comentário: {av['comentario']}")
            
            notas = [a['nota'] for a in avaliacoes_filme]
            media = sum(notas) / len(notas)
            print(f"  Média: {models.formatar_nota_estrelas(media)}")
        else:
            print("  Sem avaliações ainda.")

def main():
    while True:
        try:
            exibir_menu_principal()
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                cadastrar_filme()
            
            elif opcao == "2":
                avaliar_filme()
            
            elif opcao == "3":
                exibir_estatisticas()
            
            elif opcao == "4":
                exibir_recomendacoes()
            
            elif opcao == "5":
                exibir_relatorios()
            
            elif opcao == "6":
                listar_filmes_com_avaliacoes()
            
            elif opcao == "7":
                print("\nSaindo do sistema...")
                break
            
            else:
                print("Opção inválida. Tente novamente.")
        
        except Exception as e:
            print(f"\nErro inesperado: {e}")