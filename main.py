
from pathlib import Path
from shutil import copytree


# Pasta que armazena as imagens do treinamento.
pasta_imagens = "dataset/images/train"
# Pasta que armazena as imagens de validacao.
imagens_validacao = "dataset/images/val"
# Pasta usada para armazenar resultados.
resultados_ia = "resultados"
# Pasta das anotacoes das imagens d treinamento.
pasta_anotacoes = "dataset/labels/train"
# Pasta das anotacoes das imagens de validacao.
anotacoes_validacao = "dataset/labels/val"



# 2. EXIBICAO DOS CAMINHOS CONFIGURADOS
# Mostra no Terminal os caminhos utilizados
print("Pasta de treinamento:", pasta_imagens)
print("Pasta de validacao:", imagens_validacao)
print("Pasta de resultados:", resultados_ia)

# 3. CRIACAO AUTOMATICA DOS DIRETORIOS

# parents=True permite criar pastas intermediarias.
# exist_ok=True evita erros caso as pastas ja existam.
Path(pasta_imagens).mkdir(
    parents=True,
    exist_ok=True
)

Path(imagens_validacao).mkdir(
    parents=True,
    exist_ok=True
)

Path(resultados_ia).mkdir(
    parents=True,
    exist_ok=True
)

Path(pasta_anotacoes).mkdir(
    parents=True,
    exist_ok=True
)

Path(anotacoes_validacao).mkdir(
    parents=True,
    exist_ok=True
)

# Criar as pastas do conjunto de teste.
Path("dataset/images/test").mkdir(
    parents=True,
    exist_ok=True
)

Path("dataset/labels/test").mkdir(
    parents=True,
    exist_ok=True
)

print("Pastas criadas com sucesso!")



# 4. ORGANIZACAO DO DATASET ORIGINAL
# Copia as imagens de treinamento.
copytree(
    "dados_originais/train/images",
    pasta_imagens,
    dirs_exist_ok=True
)

# Copia as imagens de validacao.
copytree(
    "dados_originais/valid/images",
    imagens_validacao,
    dirs_exist_ok=True
)

# Copia as imagens de teste.
copytree(
    "dados_originais/test/images",
    "dataset/images/test",
    dirs_exist_ok=True
)

# Copia as anotacoes de treinamento.
copytree(
    "dados_originais/train/labels",
    pasta_anotacoes,
    dirs_exist_ok=True
)

# Copia as anotacoes de validacao.
copytree(
    "dados_originais/valid/labels",
    anotacoes_validacao,
    dirs_exist_ok=True
)

# Copia as anotacoes de teste.
copytree(
    "dados_originais/test/labels",
    "dataset/labels/test",
    dirs_exist_ok=True
)

print("Dataset organizado com sucesso!")


# 5. VERIFICACAO DAS QUANTIDADES DE ARQUIVOS

# Conta os arquivos de imagem existentes em cada
# conjunto para verificar a organizacao do dataset.
print(
    "Imagens de treinamento:",
    len(list(Path(pasta_imagens).iterdir()))
)

print(
    "Imagens de validacao:",
    len(list(Path(imagens_validacao).iterdir()))
)

print(
    "Imagens de teste:",
    len(list(Path("dataset/images/test").iterdir()))
)

# Conta os arquivos de anotacao de cada conjunto.
print(
    "Anotacoes de treinamento:",
    len(list(Path(pasta_anotacoes).glob("*.txt")))
)

print(
    "Anotacoes de validacao:",
    len(list(Path(anotacoes_validacao).glob("*.txt")))
)

print(
    "Anotacoes de teste:",
    len(list(Path("dataset/labels/test").glob("*.txt")))
)


# 6. CONFIGURACAO DO TREINAMENTO YOLO

Path("dataset/data.yaml").write_text(
    f"""path: {Path("dataset").resolve().as_posix()}
train: images/train
val: images/val
test: images/test

nc: 1
names:
  0: street_light_0
""",
    encoding="utf-8"
)

print("Arquivo data.yaml configurado com sucesso!")
print("Preparacao do dataset LuzSegura finalizada!")
