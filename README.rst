# Faucet Bot

Este proyecto es un bot de Telegram que permite a los usuarios reclamar tokens de un faucet 
basado en la red **Story Odyssey**. El bot realiza verificaciones de CAPTCHA, asegura que 
los usuarios no reclamen tokens múltiples veces en un corto periodo, y maneja las 
transacciones en la blockchain utilizando Web3.


Aun que el proyecto esta echo para usarse en story, se puede adaptar facil a otras chain
usando infura, solo tendrias que cambiar la rpc url con la terminacion en tu api key,
y proporcionar tu api key en el .env

## Requisitos

- **Python 3.10+**
- **Dependencias de Python**: 
    - `web3` versión `5.29.0`
    - `python-telegram-bot` versión `^21.10`
    - `python-dotenv` versión `^1.0.1`
    - `pillow` versión `^11.1.0`

## Configuración

1.- Clona este repositorio

Primero, clona este repositorio en tu máquina local.

```bash
git clone <url_del_repositorio>
cd faucet-bot


2.- Crea un entorno virtual

python3 -m venv venv
source venv/bin/activate  # En Linux/MacOS
venv\Scripts\activate  # En Windows



3.-Instala las dependencias
poetry install
(Si no tienes poetry instalado usa "pip install poetry")

4.- Configura las variables de entorno
INFURA_PROJECT_ID=your_infura_project_id   #Solo si usas algun nodo de infura
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
CONTRACT_ADDRESS=your_contract_address  #del token con el que interactuara
PRIVATE_KEY=your_private_key

5.- Ejecutar el bot
python bot.py



Este `README.md` incluye instrucciones detalladas sobre cómo configurar el proyecto, las variables de entorno necesarias, y cómo ejecutar el bot. Puedes personalizarlo más según sea necesario.

