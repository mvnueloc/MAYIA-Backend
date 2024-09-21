from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
import tempfile
import logging

# <-- Configuración -->
logging.basicConfig(level=logging.DEBUG)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)
CORS(app) 

# <-- Datos -->

SUPPORTED_FORMATS = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']

saldo_disponible = {"saldo_disponible": 3200.50}

transacciones = [
    {"id": 1, "tipo": "ingreso", "descripcion": "Salario mensual", "monto": 1500.00, "fecha": "2024-08-01"},
    {"id": 2, "tipo": "egreso", "descripcion": "Renta de agosto", "monto": 600.00, "fecha": "2024-08-05"},
    {"id": 3, "tipo": "ingreso", "descripcion": "Freelance Project", "monto": 400.00, "fecha": "2024-08-15"},
    {"id": 4, "tipo": "egreso", "descripcion": "Supermercado", "monto": 150.00, "fecha": "2024-08-20"},
    {"id": 5, "tipo": "ingreso", "descripcion": "Venta de equipo", "monto": 300.00, "fecha": "2024-09-10"},
    {"id": 6, "tipo": "egreso", "descripcion": "Renta de septiembre", "monto": 600.00, "fecha": "2024-09-05"},
    {"id": 7, "tipo": "egreso", "descripcion": "Gastos de viaje", "monto": 200.00, "fecha": "2024-09-15"},
    {"id": 8, "tipo": "egreso", "descripcion": "Suscripción Netflix", "monto": 15.99, "fecha": "2024-09-01"},
    {"id": 9, "tipo": "egreso", "descripcion": "Suscripción Spotify", "monto": 9.99, "fecha": "2024-09-05"},
    {"id": 10, "tipo": "egreso", "descripcion": "Café Starbucks", "monto": 5.00, "fecha": "2024-09-02"},
    {"id": 11, "tipo": "egreso", "descripcion": "Café Starbucks", "monto": 5.00, "fecha": "2024-09-04"},
    {"id": 12, "tipo": "egreso", "descripcion": "Café Starbucks", "monto": 5.00, "fecha": "2024-09-06"},
    {"id": 13, "tipo": "egreso", "descripcion": "Suscripción Amazon Prime", "monto": 12.99, "fecha": "2024-09-15"},
    {"id": 14, "tipo": "egreso", "descripcion": "Suscripción HBO Max", "monto": 14.99, "fecha": "2024-09-20"}
]

contactos_recurrentes = [
    {"id": 1, "nombre": "Carlos Pérez", "tipo_operacion": "Transferencia", "monto": 200.00, "frecuencia": "Mensual", "ultimo_pago": "2024-09-01"},
    {"id": 2, "nombre": "Ana Martínez", "tipo_operacion": "Transferencia", "monto": 150.00, "frecuencia": "Semanal", "ultimo_pago": "2024-09-15"},
    {"id": 3, "nombre": "Academia de Inglés", "tipo_operacion": "Pago de suscripción", "monto": 100.00, "frecuencia": "Mensual", "ultimo_pago": "2024-09-05"},
    {"id": 4, "nombre": "Gym Fitness", "tipo_operacion": "Pago de membresía", "monto": 50.00, "frecuencia": "Mensual", "ultimo_pago": "2024-09-01"},
    {"id": 5, "nombre": "Clases de Yoga", "tipo_operacion": "Transferencia", "monto": 30.00, "frecuencia": "Semanal", "ultimo_pago": "2024-09-14"},
    {"id": 6, "nombre": "Plataforma Educativa", "tipo_operacion": "Suscripción", "monto": 29.99, "frecuencia": "Mensual", "ultimo_pago": "2024-09-10"}
]

servicios_disponibles = [
    {"id": 1, "nombre": "Luz", "proveedor": "Compañía Eléctrica Nacional", "monto": 75.50, "fecha_vencimiento": "2024-09-30"},
    {"id": 2, "nombre": "Agua", "proveedor": "Servicio Municipal de Agua", "monto": 35.20, "fecha_vencimiento": "2024-09-25"},
    {"id": 3, "nombre": "Internet", "proveedor": "FastNet ISP", "monto": 45.00, "fecha_vencimiento": "2024-09-20"},
    {"id": 4, "nombre": "Teléfono", "proveedor": "Telefónica Global", "monto": 20.00, "fecha_vencimiento": "2024-09-22"},
    {"id": 5, "nombre": "Gas", "proveedor": "GasNatural", "monto": 55.00, "fecha_vencimiento": "2024-09-28"}
]

# <-- Funciones -->
def is_valid_audio_format(filename):
    _, extension = os.path.splitext(filename)
    extension = extension.lower().lstrip('.')
    return extension in SUPPORTED_FORMATS

# <-- Rutas -->

@app.route('/api/saldo', methods=['GET'])
def obtener_saldo():
    return jsonify(saldo_disponible)

@app.route('/api/saldo', methods=['PUT'])
def actualizar_saldo():
    nuevo_saldo = request.json.get('saldo_disponible')
    if nuevo_saldo is None:
        return jsonify({'error': 'Se requiere el campo saldo_disponible'}), 400
    
    try:
        nuevo_saldo = float(nuevo_saldo)
    except ValueError:
        return jsonify({'error': 'El saldo debe ser un número válido'}), 400

    saldo_disponible['saldo_disponible'] = nuevo_saldo
    return jsonify(saldo_disponible), 200

@app.route('/api/transacciones', methods=['GET'])
def obtener_transacciones():
    return jsonify(transacciones)

@app.route('/api/transacciones', methods=['POST'])
def agregar_transaccion():
    nueva_transaccion = request.json
    campos_requeridos = ['tipo', 'descripcion', 'monto', 'fecha']
    
    for campo in campos_requeridos:
        if campo not in nueva_transaccion:
            return jsonify({'error': f'Falta el campo requerido: {campo}'}), 400
    
    try:
        nueva_transaccion['monto'] = float(nueva_transaccion['monto'])
    except ValueError:
        return jsonify({'error': 'El monto debe ser un número válido'}), 400
    
    nueva_transaccion['id'] = max(t['id'] for t in transacciones) + 1
    transacciones.append(nueva_transaccion)
    
    return jsonify(nueva_transaccion), 201

@app.route('/api/contactos_recurrentes', methods=['GET'])
def obtener_contactos_recurrentes():
    return jsonify(contactos_recurrentes)

@app.route('/api/servicios_disponibles', methods=['GET'])
def obtener_servicios_disponibles():
    return jsonify(servicios_disponibles)

@app.route('/api/transacciones/<int:id>', methods=['DELETE'])
def borrar_transaccion(id):
    global transacciones
    transaccion_a_borrar = next((t for t in transacciones if t['id'] == id), None)

    if transaccion_a_borrar is None:
        return jsonify({'error': 'Transacción no encontrada'}), 404
    
    transacciones = [t for t in transacciones if t['id'] != id]
    return jsonify({'message': 'Transacción borrada exitosamente'}), 200


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se encontró el archivo de audio'}), 400

    audio_file = request.files['audio']
    logging.debug(f"Recibido archivo: {audio_file.filename}")

    if not is_valid_audio_format(audio_file.filename):
        return jsonify({'error': f'Formato de archivo no válido. Formatos soportados: {", ".join(SUPPORTED_FORMATS)}'}), 400

    try:
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            # Guardar el contenido del archivo de audio en el archivo temporal
            audio_file.save(temp_file)
            temp_file_path = temp_file.name

        logging.debug(f"Archivo temporal creado: {temp_file_path}")

        # Verificar el tamaño del archivo
        file_size = os.path.getsize(temp_file_path)
        logging.debug(f"Tamaño del archivo: {file_size} bytes")

        if file_size == 0:
            return jsonify({'error': 'El archivo de audio está vacío'}), 400

        # Abrir el archivo temporal en modo binario
        with open(temp_file_path, "rb") as audio_file:
            # Usar la API de OpenAI para transcribir el audio
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="es"  # Especificar el idioma español
            )
        
        # Eliminar el archivo temporal
        os.unlink(temp_file_path)

        text = transcription.text
        print(transcription)
        logging.debug(f"Transcripción obtenida: {text}")
        return jsonify({'text': text}), 200
    except Exception as e:
        logging.error(f"Error durante la transcripción: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error al transcribir el audio: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
