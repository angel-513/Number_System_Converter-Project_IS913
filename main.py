from anly_sint import parse_input

def main():
    print("Conversor de sistemas numericos.")
    print("Ejemplos validos: 0b1010 to decimal, 0x1F to binary, 123 to random, etc.")
    print("Escribie 'salir' para terminar.\n")

    while True:
        try:
            entrada = input(">>> ")
        except EOFError:
            break

        if entrada.lower() in ['salir', 'exit', 'quit']:
            print("Saliendo del programa.")
            break

        if entrada.strip() == "":
            continue

        print(parse_input(entrada))

if __name__ == "__main__":
    main()