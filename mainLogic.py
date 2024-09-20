import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def analyze_finances():
    print("Analizando finanzas...")
    # Aquí iría la lógica real de análisis financiero
    return True

def make_transaction():
    print("Haciendo transacción...")
    # Aquí iría la lógica real de la transacción
    return True

def test_function():
    print("Función de prueba...")
    # Aquí iría la lógica real de la función de prueba
    return True

def confirm_operation(operation_name):
    confirmation = input(f"¿Desea confirmar la operación '{operation_name}'? (s/n): ")
    return confirmation.lower() == 's'

def show_operation_result(operation_name, success):
    operation_keywords = {
        "analizar_finanzas": "El análisis financiero",
        "hacer_transaccion": "La transacción",
        "funcion_prueba": "La prueba"
    }
    keyword = operation_keywords.get(operation_name, "La operación")
    
    if success:
        print(f"{keyword} se realizó correctamente.")
    else:
        print(f"{keyword} no se pudo completar.")

def llamar_api_openai(operacion: str):
    functions = {
        "analizar_finanzas": analyze_finances,
        "hacer_transaccion": make_transaction,
        "funcion_prueba": test_function
    }

    # Obtener la clave de API desde las variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la clave de API de OpenAI. Asegúrate de tener un archivo .env con OPENAI_API_KEY.")

    # Crear una instancia del cliente de OpenAI
    client = OpenAI(api_key=api_key)

    prompt = """
    Eres un asistente servicial. Para cada solicitud, responde con la acción a realizar como primera palabra. Las acciones disponibles son: 'analizar_finanzas', 'hacer_transaccion', y 'funcion_prueba'. Tu primera palabra no debe contener puntos, comas, acentos ni ninguna otra puntuación. No proporciones los pasos detallados para la acción. Ten en cuenta que realizar un depósito significa que quieres hacer una transacción.
    """

    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": operacion}
            ]
        )

        # Obtener el texto de la respuesta de ChatGPT
        res = respuesta.choices[0].message.content

        # Obtener la acción de la respuesta (primera palabra)
        action = res.split(" ")[0].lower()
        print(f"Acción: {action}")

        if action in functions:
            function = functions[action]
            print(f"Operación a realizar: {function.__name__}")
            
            if confirm_operation(function.__name__):
                print(f"Llamando a la función: {function.__name__}")
                success = function()  # Llamar a la función correspondiente
                show_operation_result(function.__name__, success)
            else:
                print("Operación cancelada por el usuario.")
        else:
            print("No se encontró una acción válida en la respuesta de ChatGPT")

        return res
    except Exception as e:
        return f"Error al llamar a la API de OpenAI: {str(e)}"

# Ejemplo de uso
if __name__ == "__main__":
    operacion = "Hola quiero hacer un deposito de 1000 pesos a la cuenta de Juan"
    resultado = llamar_api_openai(operacion)