import random
import time

# Clase para representar un caballo
class Caballo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.posicion = 0
        self.velocidad = random.randint(1, 5)  # Velocidad base aleatoria
        self.cuota = round(random.uniform(1.5, 5.0), 2)  # Cuota aleatoria
        self.ganadas = 0  # Contador de carreras ganadas
        self.blesion = False  # Estado de lesión

    def avanzar(self, clima):
        if self.blesion:
            return  # Si está lesionado, no se le permite avanzar más

        # Modificar velocidad aleatoria en cada avance
        self.velocidad = random.randint(1, 5)

        # Modificar velocidad según el clima
        if clima == "Lluvia":
            self.velocidad = max(1, self.velocidad - 1)  # Reduce la velocidad en lluvia
        elif clima == "Niebla":
            self.velocidad = max(1, self.velocidad - 2)  # Reduce más la velocidad en niebla
        elif clima == "Nieve":
            self.velocidad = max(1, self.velocidad - 3)  # Reduce aún más la velocidad en nieve

        self.posicion += self.velocidad  # Solo avanza según su velocidad

# Función para generar nombres aleatorios para los caballos
def generar_nombre():
    silabas = ["Ra", "Le", "Ta", "Mi", "Bo", "Fo", "Lu", "Ki", "Sa", "Pa", "Me", "Na", "Ri", "Te"]
    return ''.join(random.choice(silabas) for _ in range(random.randint(2, 4)))  # Nombres de 2 a 4 sílabas

# Función para crear caballos con nombres aleatorios
def crear_caballos(num_caballos):
    return [Caballo(generar_nombre()) for _ in range(num_caballos)]

# Frases narrativas aleatorias
frases_narrativas = [
    "¡La carrera comienza con gran emoción!",
    "¡Los caballos se alinean y están listos para la acción!",
    "¡El público aplaude mientras suena el silbato!",
    "¡El ambiente está electrizante!",
]

# Función para determinar eventos aleatorios
def evento_aleatorio(caballos):
    if random.random() < 0.04:  # 4% de probabilidad de lesión
        caballo_lesionado = random.choice(caballos)
        if not caballo_lesionado.blesion:  # Verifica que el caballo no esté ya lesionado
            narracion = f"¡Cuidado! {caballo_lesionado.nombre} ha sufrido una lesión."
            print(f"\033[91m{narracion}\033[0m")  # Texto en rojo para lesiones
            caballo_lesionado.blesion = True  # Marca al caballo como lesionado

# Función para determinar clima aleatorio
def elegir_clima(excluir=None):
    climas = ["Sol", "Lluvia", "Niebla", "Nieve"]
    if excluir:
        climas.remove(excluir)  # Elimina el clima actual de las opciones
    return random.choice(climas)

# Función para determinar el clima durante la carrera
def gestionar_clima(clima_actual):
    if random.random() < 0.2:  # Hay un 20% de probabilidad de que el clima cambie
        nuevo_clima = elegir_clima(clima_actual)  # Pasar el clima actual para excluirlo
        print(f"El clima ha cambiado a {nuevo_clima}.")
        return nuevo_clima
    return clima_actual

# Función para iniciar la carrera de caballos
def iniciar_carrera(caballos):
    longitud_pista = 50  # Longitud de la pista

    # Reiniciar posiciones de los caballos
    for caballo in caballos:
        caballo.posicion = 0
        caballo.blesion = False  # Resetear el estado de lesión

    clima = elegir_clima()
    print(f"\nEl clima es {clima}.")

    print("¡Empieza la carrera!")
    narracion = random.choice(frases_narrativas)  # Seleccionar una frase narrativa inicial
    print(f"Narración: {narracion}")

    while max(caballo.posicion for caballo in caballos) < longitud_pista:
        for caballo in caballos:
            caballo.avanzar(clima)

        # Ejecutar evento aleatorio
        evento_aleatorio(caballos)

        # Cambiar el clima si es necesario
        clima = gestionar_clima(clima)

        # Verificar si todos los caballos están lesionados
        if all(caballo.blesion for caballo in caballos):
            print("¡Todos los caballos han sufrido lesiones! La carrera ha terminado.")
            return None  # Termina la carrera si todos están lesionados

        # Mostrar el estado de la carrera
        for caballo in caballos:
            nombre_caballo = f"\033[91m{caballo.nombre}\033[0m" if caballo.blesion else caballo.nombre
            print(f"{nombre_caballo}: {'-' * caballo.posicion}🐎")

        narracion = f"¡La carrera avanza! {max(caballos, key=lambda x: x.posicion).nombre} está en cabeza."
        time.sleep(1)
        print("\n" + "=" * 60 + "\n")

    # Determinación del ganador
    ganador = max(caballos, key=lambda x: x.posicion)
    print(f"¡El caballo {ganador.nombre} ha ganado la carrera!")
    return ganador  # Devuelve el caballo ganador

# Almacena resultados de las carreras
resultados = []  # Lista para almacenar ganadores

# Función para actualizar cuotas de forma simple
def actualizar_cuotas(caballos, ganador):
    for caballo in caballos:
        if caballo == ganador:
            # Disminuir la cuota del caballo ganador en un 10%
            caballo.cuota = round(caballo.cuota * 0.9, 2)
        else:
            # Aumentar la cuota de los caballos perdedores en un 10%
            caballo.cuota = round(caballo.cuota * 1.1, 2)

        # Asegurarse de que las cuotas se mantengan dentro del rango deseado
        caballo.cuota = max(1.01, min(caballo.cuota, 10.00))

# Bucle principal
pesetas = 100.00  # Cantidad inicial de pesetas
num_caballos = random.randint(4, 8)  # Número de caballos a crear
caballos_existentes = crear_caballos(num_caballos)  # Crear caballos al inicio

# Mostrar los caballos disponibles para apostar
def mostrar_caballos(caballos):
    print("Caballos disponibles para apostar:")
    for idx, caballo in enumerate(caballos):
        print(f"{idx + 1}: {caballo.nombre} (Cuota: {caballo.cuota:.2f}) - Carreras ganadas: {caballo.ganadas}")

mostrar_caballos(caballos_existentes)

while True:
    print(f"\nTienes \033[92m{pesetas:.2f}\033[0m pesetas.")  # Mostrar en verde
    while True:
        try:
            apuesta = float(input("¿Cuánto deseas apostar? (0 para salir): "))
            if apuesta < 0:
                print("La apuesta no puede ser negativa. Intenta de nuevo.")
                continue
            if apuesta > pesetas:
                print("No tienes suficientes pesetas para esa apuesta. Intenta de nuevo.")
                continue
            break  # Sale del bucle si la apuesta es válida
        except ValueError:
            print("Entrada no válida. Debes ingresar un número.")

    if apuesta == 0:
        print("Gracias por jugar. ¡Hasta luego!")
        break

    # Selección del caballo por parte del jugador
    while True:
        try:
            seleccion = int(input("Selecciona el número del caballo al que deseas apostar: ")) - 1
            if seleccion < 0 or seleccion >= len(caballos_existentes):
                raise ValueError("Selección no válida. Intenta de nuevo.")
            break  # Sale del bucle si la selección es válida
        except ValueError as e:
            print(e)

    caballo_seleccionado = caballos_existentes[seleccion]

    # Iniciar la carrera
    ganador = iniciar_carrera(caballos_existentes)

    # Guardar resultados
    if ganador is not None:
        resultados.append(ganador)
        ganador.ganadas += 1  # Incrementar las ganadas del caballo ganador

    # Actualizar cuotas después de cada carrera
    actualizar_cuotas(caballos_existentes, ganador)  # Pasar el caballo ganador

    if ganador is None:
        print(f"No hay ganador. Has perdido {apuesta:.2f} pesetas. Ahora tienes {pesetas:.2f} pesetas.")
    else:
        # Actualizar pesetas según el resultado de la carrera
        if caballo_seleccionado == ganador:
            ganancia = apuesta * caballo_seleccionado.cuota
            pesetas += ganancia  # Ganancias
            print(f"¡Felicidades! Tu caballo {ganador.nombre} ha ganado. Ganaste {ganancia:.2f} pesetas.")
        else:
            pesetas -= apuesta  # Pérdidas
            print(f"Lo siento, tu caballo {caballo_seleccionado.nombre} no ganó. Has perdido {apuesta:.2f} pesetas.")

    # Mostrar los resultados de la carrera
    print("\nResultados de la carrera:")
    for caballo in caballos_existentes:
        print(f"{caballo.nombre}: {caballo.ganadas} carrera(s) ganada(s) - Cuota: {caballo.cuota:.2f}")