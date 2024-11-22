class Terminal:
    def __init__(self, costo_insert=2, costo_delete=2, costo_replace=3, costo_kill=1, costo_advance=1):
        self.costo_insert = costo_insert
        self.costo_delete = costo_delete
        self.costo_replace = costo_replace
        self.costo_kill = costo_kill
        self.costo_advance = costo_advance

    def cambiar_costos(self, insert, delete, replace, kill, advance):
        self.costo_insert = insert
        self.costo_delete = delete
        self.costo_replace = replace
        self.costo_kill = kill
        self.costo_advance = advance

    def obtener_costos(self):
        return {
            "insert": self.costo_insert,
            "delete": self.costo_delete,
            "replace": self.costo_replace,
            "kill": self.costo_kill,
            "advance": self.costo_advance
        }

    def terminal_fuerzaBruta(self, cadena1,cadena2):

        def terminal_fuerzaBruta_aux(i, j):
            #verificar que la solucion ya se calculo
            #if memoria[i][j] != -1:
            #    return memoria[i][j], pasos[i][j]

            # Si llegamos al final de cadena2
            if len(cadena2) == j:
                if i < len(cadena1):
                    #memoria[i][j] = self.costo_kill
                    #pasos[i][j] = ["kill"]
                    return self.costo_kill, ["kill"]
                return 0, []

            # Si llegamos al final de la terminal
            if len(cadena1) == i:
                #memoria[i][j] = len(cadena2[j:]) * self.costo_insert
                soluci = [f"insert {x}" for x in cadena2[j:]]
                #pasos[i][j] = soluci
                return len(cadena2[j:]) * self.costo_insert, soluci

            avanzar = float('inf')
            paso_avance = []

            # Si los caracteres son iguales, simplemente avanzamos
            if cadena1[i] == cadena2[j]:
                avanzar, paso_avance = terminal_fuerzaBruta_aux(i+1, j+1)
                avanzar += self.costo_advance 
            
            # 1. Opción de insertar
            costo_insertar, paso_insertar = terminal_fuerzaBruta_aux(i, j+1)
            costo_insertar += self.costo_insert

            # 2. Opción de eliminar
            costo_eliminar, paso_eliminar = terminal_fuerzaBruta_aux(i+1, j)
            costo_eliminar += self.costo_delete

            # 3. Opción de reemplazar
            costo_reemplazar, paso_reemplazar = terminal_fuerzaBruta_aux(i+1, j+1)
            costo_reemplazar += self.costo_replace

            # 4. Opción de matar (kill)
            costo_kill_op, paso_kill_op = terminal_fuerzaBruta_aux(len(cadena1), j)
            costo_kill_op += self.costo_kill

            # Seleccionar la opción con el costo mínimo
            min_costo, min_pasos = min(
                (costo_insertar, ["insert " + cadena2[j]] + paso_insertar),
                (costo_eliminar, ["delete " + cadena1[i]] + paso_eliminar),
                (costo_reemplazar, ["replace " + cadena1[i] + " with " + cadena2[j]] + paso_reemplazar),
                (costo_kill_op, ["kill"] + paso_kill_op),
                (avanzar,["advance"] + paso_avance),
                key=lambda x: x[0]
            )

            # Guardar la solución mínima
            #memoria[i][j] = min_costo
            #pasos[i][j] = min_pasos

            return min_costo, min_pasos

        return terminal_fuerzaBruta_aux(0,0)


    def terminal_dinamica(self, cadena1,cadena2):
        
        def terminal_dinamica_aux(i, j, memoria, pasos):
            #verificar que la solucion ya se calculo
            if memoria[i][j] != -1:
                return memoria[i][j], pasos[i][j]

            # Si llegamos al final de cadena2
            if len(cadena2) == j:
                if i < len(cadena1):
                    memoria[i][j] = self.costo_kill
                    pasos[i][j] = ["kill"]
                    return self.costo_kill, ["kill"]
                return 0, []

            # Si llegamos al final de la terminal
            if len(cadena1) == i:
                memoria[i][j] = len(cadena2[j:]) * self.costo_insert
                soluci = [f"insert {x}" for x in cadena2[j:]]
                pasos[i][j] = soluci
                return memoria[i][j], soluci

            avanzar = float('inf')
            paso_avance = []

            # Si los caracteres son iguales, simplemente avanzamos
            if cadena1[i] == cadena2[j]:
                avanzar, paso_avance = terminal_dinamica_aux(i+1, j+1, memoria, pasos)
                avanzar += self.costo_advance 
            
            # 1. Opción de insertar
            costo_insertar, paso_insertar = terminal_dinamica_aux(i, j+1, memoria, pasos)
            costo_insertar += self.costo_insert

            # 2. Opción de eliminar
            costo_eliminar, paso_eliminar = terminal_dinamica_aux(i+1, j, memoria, pasos)
            costo_eliminar += self.costo_delete

            # 3. Opción de reemplazar
            costo_reemplazar, paso_reemplazar = terminal_dinamica_aux(i+1, j+1, memoria, pasos)
            costo_reemplazar += self.costo_replace

            # 4. Opción de matar (kill)
            costo_kill_op, paso_kill_op = terminal_dinamica_aux(len(cadena1), j, memoria, pasos)
            costo_kill_op += self.costo_kill

            # Seleccionar la opción con el costo mínimo
            min_costo, min_pasos = min(
                (costo_insertar, ["insert " + cadena2[j]] + paso_insertar),
                (costo_eliminar, ["delete " + cadena1[i]] + paso_eliminar),
                (costo_reemplazar, ["replace " + cadena1[i] + " with " + cadena2[j]] + paso_reemplazar),
                (costo_kill_op, ["kill"] + paso_kill_op),
                (avanzar,["advance"] + paso_avance),
                key=lambda x: x[0]
            )

            # Guardar la solución mínima
            memoria[i][j] = min_costo
            pasos[i][j] = min_pasos
            return min_costo, min_pasos

        n = len(cadena1)+1  # Número de columnas
        m = len(cadena2)+1  # Número de filas
        matriz = [[-1 for _ in range(m)] for _ in range(n)]
        paso = [[-1 for _ in range(m)] for _ in range(n)]

        return terminal_dinamica_aux(0,0,matriz,paso)


    def terminal_voraz(self, ca1, ca2):
        def terminal_voraz_aux(cadena1, cadena2, pasos, costo_total):
            if len(cadena1) == 0:
                costo = self.costo_insert * len(cadena2)
                return costo + costo_total, pasos + [f"insert {x}" for x in cadena2]
            
            if len(cadena2) == 0:
                if self.costo_delete * len(cadena1) < self.costo_kill:
                    return costo_total + (self.costo_delete * len(cadena1)), pasos + [f"delete {x}" for x in cadena1]
                else:
                    return costo_total + self.costo_kill, pasos + ["kill"]
            
            # Calcular los costos directos de cada operación sin coincidencias
            beneficio_insertar = self.costo_insert
            beneficio_eliminar = self.costo_delete
            beneficio_reemplazar = self.costo_replace
            beneficio_avanzar = float("inf")
            
            if cadena1[0] == cadena2[0]:
                beneficio_avanzar = self.costo_advance

            # Elegir la operación con menor costo directo
            costo, pasos = min(
                (beneficio_insertar, pasos + ["insert " + cadena2[0]]),
                (beneficio_eliminar, pasos + ["delete"]),
                (beneficio_reemplazar, pasos + ["replace " + cadena1[0] + " with " + cadena2[0]]),
                (beneficio_avanzar, pasos + ["advance"]),
                key=lambda x: x[0]
            )

            if costo == beneficio_insertar:
                return terminal_voraz_aux(cadena1, cadena2[1:], pasos, costo_total + self.costo_insert)
            elif costo == beneficio_eliminar:
                return terminal_voraz_aux(cadena1[1:], cadena2, pasos, costo_total + self.costo_delete)
            elif costo == beneficio_reemplazar:
                return terminal_voraz_aux(cadena1[1:], cadena2[1:], pasos, costo_total + self.costo_replace)
            elif costo == beneficio_avanzar:
                return terminal_voraz_aux(cadena1[1:], cadena2[1:], pasos, costo_total + self.costo_advance)

        return terminal_voraz_aux(ca1, ca2, [], 0)

    
    

if __name__ == "__main__":
    cadena1 = "francesa"
    cadena2 = "ancestro"
    #5+2+3+8+1


    #print(terminal_fuerzaBruta(cadena1,cadena2))
    #print(terminal_dinamica(cadena1,cadena2))
    #print(terminal_voraz(cadena1,cadena2))




