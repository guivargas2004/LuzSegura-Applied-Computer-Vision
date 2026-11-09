
import cv2
import csv
import json
import time

from pathlib import Path
from datetime import datetime
from ultralytics import YOLO



# 1. CONFIGURACOES DO PROJETO


# Carregar o modelo personalizado
modelo_ia = YOLO(
    "modelos/luzsegura_yolo11n.pt"
)

# Arquivos de resultados
arquivo_deteccoes = Path("resultados/deteccoes_luzsegura.csv")
arquivo_json = Path("resultados/deteccoes_luzsegura.json")

# Criar a pasta de resultados, se precisar.
arquivo_deteccoes.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Criar o CSV com cabeçalho, se ainda náo existir
if not arquivo_deteccoes.exists():
    with open(
        arquivo_deteccoes,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            "data_hora",
            "quantidade_deteccoes",
            "confianca_media"
        ])



# 2. INICIAr A WEBCAM

deteccao_camera = cv2.VideoCapture(0)

if not deteccao_camera.isOpened():
    print("Erro ao conectar a camera!")
    raise SystemExit(1)

print("LuzSegura iniciado com sucesso!")
print("Registros salvos a cada 5 segundos.")
print("Pressione Q para encerrar.")

ultimo_registro = time.monotonic()



# 3. DETECCAO EM TEMPO REAL

try:
    while True:

        # Capturar imagem da webcam
        sucesso, imagem = deteccao_camera.read()

        if not sucesso:
            print("Erro ao capturar imagem da camera!")
            break

        # Executar a deteccao com YOLO
        resultados = modelo_ia.predict(
            source=imagem,
            imgsz=768,
            conf=0.25,
            device="mps",
            verbose=False
        )

        # Contar os objetos detectados
        detec_qtde_luminarias = len(resultados[0].boxes)

        # Calcular a confiança media das deteccoes
        if detec_qtde_luminarias > 0:
            confianca_media = (
                resultados[0].boxes.conf.mean().item()
            )
        else:
            confianca_media = 0.0

        # Desenhar as caixas de deteccao
        imagem_processada = resultados[0].plot()


        
        # 4. PAINEL VISUAL
        cv2.rectangle(
            imagem_processada,
            (0, 0),
            (460, 110),
            (30, 30, 30),
            -1
        )

        cv2.putText(
            imagem_processada,
            "LUZSEGURA",
            (15, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            imagem_processada,
            "IA ATIVA",
            (15, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            imagem_processada,
            f"Luminarias detectadas: {detec_qtde_luminarias}",
            (15, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        
        # 5. REGISTRAR RESULTADOS A CADA 5 SEGUNDOS
        if time.monotonic() - ultimo_registro >= 5:

            data_hora = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Salvar no CSV
            with open(
                arquivo_deteccoes,
                "a",
                newline="",
                encoding="utf-8"
            ) as arquivo:

                escritor = csv.writer(arquivo)

                escritor.writerow([
                    data_hora,
                    detec_qtde_luminarias,
                    round(confianca_media, 4)
                ])

            # Preparar dados para integracao
            dados_integracao = {
                "projeto": "LuzSegura",
                "status": "ativo",
                "data_hora": data_hora,
                "quantidade_deteccoes": detec_qtde_luminarias,
                "confianca_media": round(confianca_media, 4),
                "modelo": "YOLO11n",
                "origem": "webcam"
            }

            # Salvar JSON de forma segura
            arquivo_temporario = arquivo_json.with_suffix(".tmp")

            with open(
                arquivo_temporario,
                "w",
                encoding="utf-8"
            ) as arquivo:

                json.dump(
                    dados_integracao,
                    arquivo,
                    indent=4,
                    ensure_ascii=False
                )

            arquivo_temporario.replace(arquivo_json)

            print(
                f"Registro salvo: {data_hora} | "
                f"Deteccoes: {detec_qtde_luminarias} | "
                f"Confianca media: {confianca_media:.2%}"
            )

            ultimo_registro = time.monotonic()


       
        # 6. EXIBIR VIDEO
        cv2.imshow(
            "LuzSegura - Deteccao Inteligente",
            imagem_processada
        )

        # Encerrar quando apertar a tecla Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break



finally:
    deteccao_camera.release()
    cv2.destroyAllWindows()

print("LuzSegura encerrado.")
