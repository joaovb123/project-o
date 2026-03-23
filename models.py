filmes = []
avaliacoes = []

fmt = lambda t: t.strip().lower()

def formatar_nota_estrelas(nota):
    estrelas = int(round(nota))
    return "★" * estrelas + "☆" * (10 - estrelas) + f" ({nota:.1f})"

def verificar_duplicidade(titulo):
    return any(f['titulo'] == fmt(titulo) for f in filmes)

def adicionar_filme(titulo, genero, duracao):
    filmes.append({
        'titulo': fmt(titulo), 
        'genero': fmt(genero), 
        'duracao': duracao
    })

def registrar_avaliacao(titulo, nota, comentario):
    avaliacoes.append({
        'titulo': fmt(titulo), 
        'nota': float(nota), 
        'comentario': comentario
    })

def buscar_filme_por_titulo(titulo):
    return next((f for f in filmes if f['titulo'] == fmt(titulo)), None)

def calcular_media_geral():
    notas = [a['nota'] for a in avaliacoes]
    return round(sum(notas) / len(notas), 2) if notas else 0.0

def filtrar_por_genero(genero):
    return [f for f in filmes if f['genero'] == fmt(genero)]

def calcular_media_por_genero(genero):
    titulos = {f['titulo'] for f in filtrar_por_genero(genero)}
    notas = [a['nota'] for a in avaliacoes if a['titulo'] in titulos]
    return round(sum(notas) / len(notas), 2) if notas else 0.0

def obter_extremos():
    if not avaliacoes: 
        return None, None
    ordenadas = sorted(avaliacoes, key=lambda x: x['nota'])
    return ordenadas[-1], ordenadas[0]

def recomendar_top_3(genero, nota_minima):
    titulos = {f['titulo'] for f in filtrar_por_genero(genero)}
    validos = [a for a in avaliacoes if a['titulo'] in titulos and a['nota'] >= nota_minima]
    return sorted(validos, key=lambda x: x['nota'], reverse=True)[:3]

def gerar_ranking_geral():
    medias = {}
    for a in avaliacoes:
        if a['titulo'] not in medias:
            notas_filme = [av['nota'] for av in avaliacoes if av['titulo'] == a['titulo']]
            medias[a['titulo']] = round(sum(notas_filme) / len(notas_filme), 2)
    
    return sorted([{'titulo': k, 'media': v} for k, v in medias.items()], 
                  key=lambda x: x['media'], reverse=True)

def gerar_panorama_por_genero():
    generos = set(f['genero'] for f in filmes)
    panorama = []
    
    for genero in generos:
        filmes_genero = filtrar_por_genero(genero)
        media = calcular_media_por_genero(genero)
        total_avaliacoes = len([a for a in avaliacoes 
                               if a['titulo'] in {f['titulo'] for f in filmes_genero}])
        
        panorama.append({
            'genero': genero,
            'media': media,
            'total_filmes': len(filmes_genero),
            'total_avaliacoes': total_avaliacoes
        })
    
    return sorted(panorama, key=lambda x: x['media'], reverse=True)

def listar_filmes():
    return filmes.copy()

def listar_avaliacoes():
    return avaliacoes.copy()

def limpar_dados():
    global filmes, avaliacoes
    filmes.clear()
    avaliacoes.clear()