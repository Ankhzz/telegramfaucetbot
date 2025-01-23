# Faucet Bot

Este proyecto es un bot de Telegram que permite a los usuarios reclamar tokens de un faucet basado en la red **Story Odyssey**. El bot realiza verificaciones de CAPTCHA, asegura que los usuarios no reclamen tokens múltiples veces en un corto periodo, y maneja las transacciones en la blockchain utilizando Web3.

Aunque el proyecto está hecho para usarse en Story, se puede adaptar fácilmente a otras chains usando Infura. Solo tendrías que cambiar la URL RPC con la terminación de tu API key, y proporcionar tu API key en el archivo `.env`.

## Requisitos

- **Python 3.10+**
- **Dependencias de Python**: 
    - `web3` versión `5.29.0`
    - `python-telegram-bot` versión `^21.10`
    - `python-dotenv` versión `^1.0.1`
    - `pillow` versión `^11.1.0`

## Configuración

1. **Clona este repositorio**

    Primero, clona este repositorio en tu máquina local:

    ```bash
    git clone <url_del_repositorio>
    cd faucet-bot
    ```

2. **Crea un entorno virtual**

    Es recomendable usar un entorno virtual para gestionar las dependencias del proyecto. Para crear y activar el entorno virtual:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/MacOS
    venv\Scripts\activate  # En Windows
    ```

3. **Instala las dependencias**

    Instala las dependencias necesarias con Poetry:

    ```bash
    poetry install
    ```

    Si no tienes `poetry` instalado, puedes hacerlo mediante:

    ```bash
    pip install poetry
    ```

4. **Configura las variables de entorno**

    El bot necesita ciertas variables de entorno para funcionar correctamente. Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

    ```bash
    INFURA_PROJECT_ID=your_infura_project_id   # Solo si usas algún nodo de Infura
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    CONTRACT_ADDRESS=your_contract_address  # del token con el que interactuará
    PRIVATE_KEY=your_private_key
    ```

    - **INFURA_PROJECT_ID**: Obtén tu ID de proyecto de Infura para conectarte a la red Ethereum.
    - **TELEGRAM_BOT_TOKEN**: Crea un bot en Telegram y obtén el token. Usa [BotFather](https://core.telegram.org/bots#botfather) para esto.
    - **CONTRACT_ADDRESS**: La dirección de tu contrato en la blockchain de Story Odyssey.
    - **PRIVATE_KEY**: La clave privada de la cuenta que va a enviar los tokens.

5. **Ejecutar el bot**

    Una vez todo esté configurado, puedes ejecutar el bot con el siguiente comando:

    ```bash
    python bot.py
    ```

## Uso del bot

- **/start**: Muestra un mensaje de bienvenida.
- **/claim [wallet_address]**: El usuario proporciona una dirección de wallet y recibe un CAPTCHA que debe resolver para reclamar tokens.

## Estructura del Proyecto





Este `README.md` incluye instrucciones detalladas sobre cómo configurar el proyecto, las variables de entorno necesarias, y cómo ejecutar el bot. Puedes personalizarlo más según sea necesario.

