
#print(menor_numero_pasos("papaya","paraguaya"))
costo_insert = 2
costo_delete = 2
costo_replace = 3
costo_kill = 1
costo_advance = 1

def terminal_fuerzaBruta(cadena1,cadena2):

    def terminal_fuerzaBruta_aux(i, j):
        #verificar que la solucion ya se calculo
        #if memoria[i][j] != -1:
        #    return memoria[i][j], pasos[i][j]

        # Si llegamos al final de cadena2
        if len(cadena2) == j:
            if i < len(cadena1):
                #memoria[i][j] = costo_kill
                #pasos[i][j] = ["kill"]
                return costo_kill, ["kill"]
            return 0, []

        # Si llegamos al final de la terminal
        if len(cadena1) == i:
            #memoria[i][j] = len(cadena2[j:]) * costo_insert
            soluci = [f"insert {x}" for x in cadena2[j:]]
            #pasos[i][j] = soluci
            return len(cadena2[j:]) * costo_insert, soluci

        avanzar = float('inf')
        paso_avance = []

        # Si los caracteres son iguales, simplemente avanzamos
        if cadena1[i] == cadena2[j]:
            avanzar, paso_avance = terminal_fuerzaBruta_aux(i+1, j+1)
            avanzar += costo_advance 
        
        # 1. Opción de insertar
        costo_insertar, paso_insertar = terminal_fuerzaBruta_aux(i, j+1)
        costo_insertar += costo_insert

        # 2. Opción de eliminar
        costo_eliminar, paso_eliminar = terminal_fuerzaBruta_aux(i+1, j)
        costo_eliminar += costo_delete

        # 3. Opción de reemplazar
        costo_reemplazar, paso_reemplazar = terminal_fuerzaBruta_aux(i+1, j+1)
        costo_reemplazar += costo_replace

        # 4. Opción de matar (kill)
        costo_kill_op, paso_kill_op = terminal_fuerzaBruta_aux(len(cadena1), j)
        costo_kill_op += costo_kill

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


def terminal_dinamica(cadena1,cadena2):
    
    def terminal_dinamica_aux(i, j, memoria, pasos):
        #verificar que la solucion ya se calculo
        if memoria[i][j] != -1:
            return memoria[i][j], pasos[i][j]

        # Si llegamos al final de cadena2
        if len(cadena2) == j:
            if i < len(cadena1):
                memoria[i][j] = costo_kill
                pasos[i][j] = ["kill"]
                return costo_kill, ["kill"]
            return 0, []

        # Si llegamos al final de la terminal
        if len(cadena1) == i:
            memoria[i][j] = len(cadena2[j:]) * costo_insert
            soluci = [f"insert {x}" for x in cadena2[j:]]
            pasos[i][j] = soluci
            return memoria[i][j], soluci

        avanzar = float('inf')
        paso_avance = []

        # Si los caracteres son iguales, simplemente avanzamos
        if cadena1[i] == cadena2[j]:
            avanzar, paso_avance = terminal_dinamica_aux(i+1, j+1, memoria, pasos)
            avanzar += costo_advance 
        
        # 1. Opción de insertar
        costo_insertar, paso_insertar = terminal_dinamica_aux(i, j+1, memoria, pasos)
        costo_insertar += costo_insert

        # 2. Opción de eliminar
        costo_eliminar, paso_eliminar = terminal_dinamica_aux(i+1, j, memoria, pasos)
        costo_eliminar += costo_delete

        # 3. Opción de reemplazar
        costo_reemplazar, paso_reemplazar = terminal_dinamica_aux(i+1, j+1, memoria, pasos)
        costo_reemplazar += costo_replace

        # 4. Opción de matar (kill)
        costo_kill_op, paso_kill_op = terminal_dinamica_aux(len(cadena1), j, memoria, pasos)
        costo_kill_op += costo_kill

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
        if i == 0 and j == 0:
            for x in memoria:
                print(x)

        return min_costo, min_pasos

    n = len(cadena1)+1  # Número de columnas
    m = len(cadena2)+1  # Número de filas
    matriz = [[-1 for _ in range(m)] for _ in range(n)]
    paso = [[-1 for _ in range(m)] for _ in range(n)]

    return terminal_dinamica_aux(0,0,matriz,paso)


def terminal_voraz(ca1,ca2):
    def coincidencias(cadena1,cadena2):      
        coincidencias = 0
        for i in range(0,min(2,len(cadena1),len(cadena2))):
            if cadena1[i] == cadena2[i]:
                coincidencias += 1
        return coincidencias
    def terminal_voraz_aux(cadena1,cadena2,pasos,costo_total):
        if len(cadena1) == 0:
            costo = costo_insert*len(cadena2)
            return costo+costo_total, pasos + [f"insert {x}" for x in cadena2]
        if len(cadena2) == 0:
            if len(cadena1) == 0:
                return costo_total,pasos
            else:
                if costo_delete * len(cadena1) < costo_kill:
                    return costo_total + (costo_delete*len(cadena1)), pasos + [f"delete {x}" for x in cadena1]
                else:
                    return costo_total+costo_kill, pasos + ["kill"]
        
        beneficio_insertar = costo_insert/(coincidencias(cadena1,cadena2[1:])+1+2)
        beneficio_eliminar = costo_delete/(coincidencias(cadena1[1:],cadena2)+1+2)
        beneficio_reemplazar = costo_replace/(coincidencias(cadena1[1:],cadena2[1:])+1+3)
        #beneficio_kill = (costo_kill+(costo_insert*len(cadena2)))/1
        beneficio_avanzar = float("inf")
        #print((len(cadena1)*100)/costo_kill+(costo_insert*len(cadena2)))
        #print(cadena1,cadena2)
        if cadena1[0] == cadena2[0]:
            beneficio_avanzar = costo_advance/(coincidencias(cadena1[1:],cadena2[1:])+1+3+1)

        #print(beneficio_insertar,beneficio_eliminar,beneficio_reemplazar,beneficio_avanzar)
        costo,pasos = min(
            (beneficio_insertar, pasos + ["insert " + cadena2[0]]),
            (beneficio_eliminar, pasos + ["delete"] ),
            (beneficio_reemplazar, pasos + ["replace " + cadena1[0] + " with " + cadena2[0]]),
            #(beneficio_kill, pasos + ["kill"]),
            (beneficio_avanzar, pasos + ["advance"]),
            key=lambda x: x[0]
        )
        if costo == beneficio_insertar:
            #print(cadena1,cadena2,"insertar")
            return terminal_voraz_aux(cadena1,cadena2[1:],pasos,costo_total+costo_insert)
        if costo == beneficio_eliminar:
            #print(cadena1,cadena2,"eliminar")
            return terminal_voraz_aux(cadena1[1:],cadena2,pasos,costo_total+costo_delete)
        if costo == beneficio_reemplazar:
            #print(cadena1,cadena2,"reemplazar")
            return terminal_voraz_aux(cadena1[1:],cadena2[1:],pasos,costo_total+costo_replace)
        if costo == beneficio_avanzar:
            #print(cadena1,cadena2,"avanzar")
            return terminal_voraz_aux(cadena1[1:],cadena2[1:],pasos,costo_total+costo_advance)
        else:
            costo = costo_kill + (costo_insert*len(cadena2))
            return costo+costo_total, pasos + [f"insert {x}" for x in cadena2]

    return terminal_voraz_aux(ca1,ca2,[],0)

    

        
    #return terminal_voraz_aux(0,0)

if __name__ == "__main__":
    cadena1 = "francesa"
    cadena2 = "ancestro"
    #5+2+3+8+1


    #print(terminal_fuerzaBruta(cadena1,cadena2))
    print(terminal_dinamica(cadena1,cadena2))
    print(terminal_voraz(cadena1,cadena2))




