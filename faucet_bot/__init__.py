import os
import json
import time
import random
import string
from dotenv import load_dotenv
from web3 import Web3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from PIL import Image, ImageDraw, ImageFont
from web3.middleware import geth_poa_middleware

# Cargar variables de entorno
load_dotenv()

# Configuración inicial
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Verificar si las variables de entorno se cargaron correctamente
if not INFURA_PROJECT_ID or not TELEGRAM_BOT_TOKEN or not CONTRACT_ADDRESS or not PRIVATE_KEY:
    raise ValueError("Faltan algunas variables de entorno necesarias")

# Conexión a la blockchain
provider_url = "https://rpc.odyssey.storyrpc.io/" 
web3 = Web3(Web3.HTTPProvider(provider_url))

# Aplicar middleware si estamos en una red POA (como Polygon)
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Verificar conexión
if web3.isConnected():
    print("Conexión exitosa a Story")
else:
    print("Error al conectar con Story")

# ABI del contrato (esto debe ser el ABI real de tu contrato)
contract_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "recipient", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

# Dirección del contrato
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Crear instancia de la wallet
account = web3.eth.account.privateKeyToAccount(PRIVATE_KEY)

# Ruta del archivo donde se guardan los datos de los usuarios
USER_DB_PATH = 'users_db.json'

# Cargar la base de datos de usuarios
def load_users_db():
    try:
        with open(USER_DB_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Guardar los datos de los usuarios
def save_users_db(users_db):
    with open(USER_DB_PATH, 'w') as f:
        json.dump(users_db, f)

# Verificar si un usuario puede reclamar
def can_claim(user_id, wallet_address):
    users_db = load_users_db()
    current_time = time.time()
    
    if user_id in users_db:
        if wallet_address in users_db[user_id]:
            last_claim_time = users_db[user_id][wallet_address]['last_claim']
            if current_time - last_claim_time < 86400:
                return False  # Ya ha reclamado en las últimas 24 horas
    return True

# Registrar un nuevo claim para un usuario
def register_claim(user_id, wallet_address):
    users_db = load_users_db()
    current_time = time.time()
    
    if user_id not in users_db:
        users_db[user_id] = {}
    
    users_db[user_id][wallet_address] = {'last_claim': current_time}
    save_users_db(users_db)
    return True

# Función para enviar tokens
def send_tokens(to, amount):
    try:
        # Verificar saldo del contrato
        balance = contract.functions.balanceOf(account.address).call()
        if balance < amount:
            print("No tienes suficiente saldo para realizar esta transacción.")
            return False
        
        # Validar la dirección del destinatario
        if not web3.isAddress(to):
            print("La dirección proporcionada no es válida.")
            return False
        


        # Verificar la dirección del remitente
        print(f"Dirección de la cuenta remitente: {account.address}")

        # Verificar el saldo del remitente
        balance = web3.eth.get_balance(account.address)
        print(f"Saldo de la cuenta remitente: {web3.fromWei(balance, 'ether')} ETH")


        # Obtener el precio actual del gas
        current_gas_price = web3.eth.gas_price
        current_gas_price_gwei = web3.fromWei(current_gas_price, 'gwei')
        print(f"Precio actual del gas: {current_gas_price_gwei} gwei")

        # Establecer un rango aceptable de gas (30 a 300 gwei)
        if current_gas_price_gwei < 30 or current_gas_price_gwei > 300:
            print(f"El precio del gas es demasiado alto (actual: {current_gas_price_gwei} gwei). Intenta más tarde.")
            return False  # El gas está fuera del rango



        # Verificar el Chain ID conectado
        chain_id = web3.eth.chain_id
        print(f"Chain ID conectado: {chain_id}")




        # Realizar la transferencia
        nonce = web3.eth.getTransactionCount(account.address)
        tx = contract.functions.transfer(to, amount).buildTransaction({
            'chainId': 1516,  # Story Odissey testnet
            'gas': 200000,
            'gasPrice':current_gas_price,
            'nonce': nonce,
        })

        print(f"Transacción construida: {tx}")

       


        
        # Firmar la transacción
        signed_tx = web3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
        print(f"Transacción firmada: {signed_tx}")
        
        # Enviar la transacción
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transacción enviada! Hash: {web3.toHex(tx_hash)}")
        
        # Esperar la transacción
        web3.eth.waitForTransactionReceipt(tx_hash)
        print("Tokens enviados correctamente.")
        return True
    except Exception as e:
        print(f"Error al enviar tokens: {e}")
        return False

# Función para generar un CAPTCHA
def generate_captcha():
    characters = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(6))
    
    # Crear imagen con un tamaño más grande
    image = Image.new('RGB', (250, 100), color=(255, 255, 255))
    font = ImageFont.truetype("arial.ttf", 35)  # Fuente más grande
    draw = ImageDraw.Draw(image)

    # Dibujar líneas o ruido en el fondo
    for _ in range(10):
        start_pos = (random.randint(0, 250), random.randint(0, 100))
        end_pos = (random.randint(0, 250), random.randint(0, 100))
        draw.line([start_pos, end_pos], fill=(0, 0, 0), width=2)

    # Usar textbbox para obtener las dimensiones del texto
    text_bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Dibujar el texto (centrado)
    draw.text(((250 - text_width) / 2, (100 - text_height) / 2), captcha_text, fill=(0, 0, 0), font=font)
    
    # Guardar la imagen
    captcha_image_path = 'captcha_image.png'
    image.save(captcha_image_path)
    
    return captcha_text, captcha_image_path

# Función para manejar el comando /claim
async def claim(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)  # ID de Telegram
    wallet_address = context.args[0] if context.args else None
    
    if not wallet_address:
        await update.message.reply_text("Por favor, proporciona tu dirección de wallet. Ejemplo: /claim 0x123abc456def")
        return
    
    # Generar CAPTCHA
    captcha_text, captcha_image_path = generate_captcha()
    await update.message.reply_text(f"Por favor, ingresa el código CAPTCHA que aparece en la imagen:")
    await update.message.reply_photo(photo=open(captcha_image_path, 'rb'))
    
    # Guardar CAPTCHA para validación posterior
    context.user_data['captcha'] = captcha_text
    context.user_data['wallet_address'] = wallet_address

# Función para verificar el CAPTCHA
async def check_captcha(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    correct_captcha = context.user_data.get('captcha', None)
    wallet_address = context.user_data.get('wallet_address', None)
    
    if user_input == correct_captcha:
        user_id = str(update.message.from_user.id)
        await update.message.reply_text(f"Captcha contestado correctamente, en un momento se te enviaran los tokens!")
        if can_claim(user_id, wallet_address):
            amount = 10 * (10 ** 18)  # 10 tokens con 18 decimales (ajusta según tu token)
            if send_tokens(wallet_address, amount):
                await update.message.reply_text(f"Tokens enviados a {wallet_address}! Recuerda regresar en 24Hrs")
                register_claim(user_id, wallet_address)
            else:
                await update.message.reply_text("No se pudieron enviar los tokens. En este momento no hay fondos")
        else:
            await update.message.reply_text("Ya has reclamado tus tokens en las últimas 24 horas.")
    else:
        await update.message.reply_text("El código CAPTCHA es incorrecto. Intenta de nuevo.")

# Función para manejar el comando /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("¡Hola! Soy un bot de faucet en Polygon. Envía /claim para comenzar.")

# Función principal para ejecutar el bot
def main() -> None:
    # Crear aplicación con el token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("claim", claim))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_captcha))

    # Ejecutar el bot
    application.run_polling()

if __name__ == "__main__":
    main()
