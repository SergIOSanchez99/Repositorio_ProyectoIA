import random

def tirar_dado():
    return random.randint(1, 6)

def turno_jugador(nombre, es_maquina=False):
    dados = []
    
    # Lanzar los dados uno por uno
    for i in range(3):
        if es_maquina:
            print(f"La máquina está lanzando el dado {i + 1}...")
        else:
            input(f"{nombre}, presiona Enter para lanzar el dado {i + 1}...")

        dado = tirar_dado()
        dados.append(dado)
        print(f"Dado {i + 1} de {nombre}: {dado}")
    
    print(f"Dados finales de {nombre}: {dados}")

    # Comprobar si hay dos dados iguales
    if len(set(dados)) == 2:
        print(f"{nombre} tiene dos dados iguales.")
        if es_maquina:
            decision = 's' if random.choice([True, False]) else 'n'
            print(f"La máquina decide {'relanzar' if decision == 's' else 'no relanzar'} el tercer dado.")
        else:
            decision = input("¿Quieres relanzar el tercer dado? (s/n): ").strip().lower()
        
        if decision == 's':
            indice_a_relanzar = [i for i in range(3) if dados.count(dados[i]) == 1][0]
            dados[indice_a_relanzar] = tirar_dado()
            print(f"Nuevo resultado de los dados de {nombre}: {dados}")

    # Comprobar si hay tres dados iguales
    if len(set(dados)) == 1:
        print(f"¡Felicidades! Los tres dados de {nombre} tienen el mismo puntaje. ¡Ganas automáticamente!")
        return dados, True

    return dados, False

def calcular_puntaje(dados):
    return sum(dados)

def main():
    print("¡Bienvenido al juego de dados TRIKAS!")
    
    jugador_comienza = input("¿Quieres empezar tú? SI (s) o NO (n) : ").strip().lower() == 's'
    jugador_nombre = "Usuario"
    maquina_nombre = "Máquina"

    if jugador_comienza:
        print("El usuario comenzará primero.")
    else:
        print("La máquina comenzará primero.")

    jugadores = [(jugador_nombre, jugador_comienza), (maquina_nombre, not jugador_comienza)]
    
    resultados = {}
    for nombre, turno in jugadores:
        print(f"\nTurno de {nombre}:")
        dados, victoria_automatica = turno_jugador(nombre, es_maquina=(nombre == maquina_nombre))
        if victoria_automatica:
            print(f"{nombre} gana el juego con una victoria automática!")
            return
        resultados[nombre] = calcular_puntaje(dados)

    print("\nResultados finales:")
    print(f"{jugador_nombre}: {resultados[jugador_nombre]} puntos")
    print(f"{maquina_nombre}: {resultados[maquina_nombre]} puntos")

    if resultados[jugador_nombre] > resultados[maquina_nombre]:
        print("¡El usuario gana!")
    elif resultados[jugador_nombre] < resultados[maquina_nombre]:
        print("¡La máquina gana!")
    else:
        print("¡Es un empate!")

if __name__ == "__main__":
    main()
