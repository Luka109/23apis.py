
from fastapi import FastAPI, HTTPException
from typing import Any
import random
import secrets
import string
import statistics

app = FastAPI(
    title="Projeto com 23 APIs",
    description="APIs de estudo desenvolvidas em Python",
    version="1.0.0"
)

# Bancos de dados temporários
banco = {
    "usuarios": [],
    "produtos": [],
    "tarefas": [],
    "livros": [],
    "filmes": [],
    "musicas": [],
    "receitas": [],
    "transacoes": [],
    "jogos": [],
    "animais": [],
    "treinos": [],
    "alunos": [],
    "destinos": [],
    "estoque": [],
    "mensagens": [],
    "noticias": [],
    "perguntas": [
        {
            "pergunta": "Quanto é 2 + 2?",
            "resposta": "4"
        }
    ]
}


def adicionar(categoria: str, dados: dict):
    item = {"id": len(banco[categoria]) + 1, **dados}
    banco[categoria].append(item)
    return item


def listar(categoria: str):
    return banco[categoria]


# 1. API CALCULADORA
@app.get("/calculadora")
def calculadora(a: float, b: float, operacao: str):
    if operacao == "somar":
        resultado = a + b
    elif operacao == "subtrair":
        resultado = a - b
    elif operacao == "multiplicar":
        resultado = a * b
    elif operacao == "dividir":
        if b == 0:
            raise HTTPException(400, "Divisão por zero")
        resultado = a / b
    else:
        raise HTTPException(400, "Operação inválida")
    return {"resultado": resultado}


# 2. API CLIMA (simulada)
@app.get("/clima/{cidade}")
def clima(cidade: str):
    return {
        "cidade": cidade,
        "temperatura": random.randint(18, 35),
        "condicao": random.choice(
            ["Ensolarado", "Nublado", "Chuvoso"]
        )
    }


# 3. API USUÁRIOS
@app.post("/usuarios")
def criar_usuario(dados: dict[str, Any]):
    return adicionar("usuarios", dados)


@app.get("/usuarios")
def listar_usuarios():
    return listar("usuarios")


# 4. API PRODUTOS
@app.post("/produtos")
def criar_produto(dados: dict[str, Any]):
    return adicionar("produtos", dados)


@app.get("/produtos")
def listar_produtos():
    return listar("produtos")


# 5. API TAREFAS
@app.post("/tarefas")
def criar_tarefa(dados: dict[str, Any]):
    dados.setdefault("concluida", False)
    return adicionar("tarefas", dados)


@app.patch("/tarefas/{id}")
def concluir_tarefa(id: int):
    for tarefa in banco["tarefas"]:
        if tarefa["id"] == id:
            tarefa["concluida"] = True
            return tarefa
    raise HTTPException(404, "Tarefa não encontrada")


@app.get("/tarefas")
def listar_tarefas():
    return listar("tarefas")


# 6. API LIVROS
@app.post("/livros")
def criar_livro(dados: dict[str, Any]):
    return adicionar("livros", dados)


@app.get("/livros")
def listar_livros():
    return listar("livros")


# 7. API FILMES
@app.post("/filmes")
def criar_filme(dados: dict[str, Any]):
    return adicionar("filmes", dados)


@app.get("/filmes")
def listar_filmes():
    return listar("filmes")


# 8. API MÚSICA
@app.post("/musicas")
def criar_musica(dados: dict[str, Any]):
    return adicionar("musicas", dados)


@app.get("/musicas")
def listar_musicas():
    return listar("musicas")


# 9. API RECEITAS
@app.post("/receitas")
def criar_receita(dados: dict[str, Any]):
    return adicionar("receitas", dados)


@app.get("/receitas")
def listar_receitas():
    return listar("receitas")


# 10. API FINANÇAS
@app.post("/financas")
def registrar_transacao(dados: dict[str, Any]):
    return adicionar("transacoes", dados)


@app.get("/financas/saldo")
def saldo_financeiro():
    entradas = sum(
        float(t.get("valor", 0))
        for t in banco["transacoes"]
        if t.get("tipo") == "entrada"
    )
    saidas = sum(
        float(t.get("valor", 0))
        for t in banco["transacoes"]
        if t.get("tipo") == "saida"
    )
    return {
        "entradas": entradas,
        "saidas": saidas,
        "saldo": entradas - saidas
    }


# 11. API CONVERSOR
@app.get("/conversor/temperatura")
def converter_temperatura(celsius: float):
    return {
        "celsius": celsius,
        "fahrenheit": celsius * 9 / 5 + 32,
        "kelvin": celsius + 273.15
    }


@app.get("/conversor/km-para-milhas")
def converter_distancia(km: float):
    return {"km": km, "milhas": km * 0.621371}


# 12. API CEP (base simulada)
@app.get("/cep/{cep}")
def consultar_cep(cep: str):
    enderecos = {
        "01001000": {
            "cidade": "São Paulo",
            "estado": "SP",
            "logradouro": "Praça da Sé"
        },
        "20040002": {
            "cidade": "Rio de Janeiro",
            "estado": "RJ",
            "logradouro": "Rua da Assembleia"
        }
    }
    cep = cep.replace("-", "")
    if cep not in enderecos:
        raise HTTPException(404, "CEP não encontrado na base simulada")
    return {"cep": cep, **enderecos[cep]}


# 13. API JOGOS
@app.post("/jogos")
def criar_jogo(dados: dict[str, Any]):
    return adicionar("jogos", dados)


@app.get("/jogos")
def listar_jogos():
    return listar("jogos")


# 14. API ANIMAIS
@app.post("/animais")
def cadastrar_animal(dados: dict[str, Any]):
    return adicionar("animais", dados)


@app.get("/animais")
def listar_animais():
    return listar("animais")


# 15. API ACADEMIA
@app.post("/treinos")
def registrar_treino(dados: dict[str, Any]):
    return adicionar("treinos", dados)


@app.get("/treinos")
def listar_treinos():
    return listar("treinos")


# 16. API ESCOLA
@app.post("/alunos")
def cadastrar_aluno(dados: dict[str, Any]):
    return adicionar("alunos", dados)


@app.get("/alunos/{id}/media")
def media_aluno(id: int):
    for aluno in banco["alunos"]:
        if aluno["id"] == id:
            notas = aluno.get("notas", [])
            if not notas:
                raise HTTPException(400, "Aluno sem notas")
            return {
                "aluno": aluno.get("nome", "Sem nome"),
                "media": sum(notas) / len(notas)
            }
    raise HTTPException(404, "Aluno não encontrado")


# 17. API NOTÍCIAS (simulada)
@app.post("/noticias")
def criar_noticia(dados: dict[str, Any]):
    return adicionar("noticias", dados)


@app.get("/noticias")
def listar_noticias():
    return listar("noticias")


# 18. API VIAGENS
@app.post("/destinos")
def cadastrar_destino(dados: dict[str, Any]):
    return adicionar("destinos", dados)


@app.get("/destinos")
def listar_destinos():
    return listar("destinos")


# 19. API ESTOQUE
@app.post("/estoque")
def cadastrar_item(dados: dict[str, Any]):
    dados.setdefault("quantidade", 0)
    return adicionar("estoque", dados)


@app.patch("/estoque/{id}/entrada")
def entrada_estoque(id: int, quantidade: int):
    if quantidade <= 0:
        raise HTTPException(400, "Quantidade deve ser positiva")
    for item in banco["estoque"]:
        if item["id"] == id:
            item["quantidade"] += quantidade
            return item
    raise HTTPException(404, "Item não encontrado")


@app.get("/estoque")
def listar_estoque():
    return listar("estoque")


# 20. API CHAT (mensagens simuladas)
@app.post("/chat")
def enviar_mensagem(dados: dict[str, Any]):
    return adicionar("mensagens", dados)


@app.get("/chat")
def listar_mensagens():
    return listar("mensagens")


# 21. API GERADORA DE SENHAS
@app.get("/senha")
def gerar_senha(tamanho: int = 12):
    if not 8 <= tamanho <= 128:
        raise HTTPException(400, "Use um tamanho entre 8 e 128")
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    return {
        "senha": "".join(
            secrets.choice(caracteres) for _ in range(tamanho)
        )
    }


# 22. API ESTATÍSTICAS
@app.post("/estatisticas")
def calcular_estatisticas(dados: dict[str, list[float]]):
    numeros = dados.get("numeros", [])
    if not numeros:
        raise HTTPException(400, "Informe uma lista de números")
    return {
        "quantidade": len(numeros),
        "media": statistics.mean(numeros),
        "mediana": statistics.median(numeros),
        "maior": max(numeros),
        "menor": min(numeros)
    }


# 23. API QUIZ
@app.get("/quiz")
def obter_perguntas():
    return [
        {"id": i, "pergunta": p["pergunta"]}
        for i, p in enumerate(banco["perguntas"], start=1)
    ]


@app.post("/quiz/{id}/responder")
def responder_quiz(id: int, dados: dict[str, str]):
    if id < 1 or id > len(banco["perguntas"]):
        raise HTTPException(404, "Pergunta não encontrada")

    correta = banco["perguntas"][id - 1]["resposta"]
    resposta = dados.get("resposta", "")

    return {
        "correta": resposta.strip().lower() == correta.lower(),
        "mensagem": (
            "Resposta correta!"
            if resposta.strip().lower() == correta.lower()
            else "Resposta incorreta!"
        )
    }


@app.get("/")
def inicio():
    return {
        "mensagem": "Servidor das 23 APIs funcionando!",
        "documentacao": "/docs"
    }
