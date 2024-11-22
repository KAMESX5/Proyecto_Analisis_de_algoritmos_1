
def subastasFuerzaBruta(A, B, ofertas):    
    def subastasFuerzaBruta_aux(A, B, ofertas, i):
        # Si ya se calculó previamente la solución, simplemente retornamos
        #if memoria[i][A] != -1:
        #    return memoria[i][A], pasos[i][A]
        
        # Si ya no quedan más ofertas, retornar 0 (caso base)
        if len(ofertas) <= i:
            return 0, []

        precio, Mini, Maxi = ofertas[i]
        
        # Si no cumple las condiciones de oferta
        if Mini > A or precio < B:
            mejor_solucion, mejor_paso = subastasFuerzaBruta_aux(A, B, ofertas, i + 1)
            #memoria[i][A] = mejor_solucion
            #pasos[i][A] = mejor_paso
            return mejor_solucion, mejor_paso

        mejor_resultado = 0
        mejor_paso = []

        # Explorar asignar entre Mini y Maxi acciones
        for acciones_asignadas in range(Mini, min(A, Maxi) + 1):
            resultado, paso_actual = subastasFuerzaBruta_aux(A - acciones_asignadas, B, ofertas, i + 1)
            resultado += precio * acciones_asignadas
            
            # Si encontramos una mejor combinación, la guardamos
            if resultado > mejor_resultado:
                mejor_resultado = resultado
                mejor_paso = [f"Asignar {acciones_asignadas} acciones a {precio}"] + paso_actual
        
        no_comprar, no_comprar_paso = subastasFuerzaBruta_aux(A, B, ofertas, i + 1)
        # Guardar en memoria la mejor solución encontrada
        if no_comprar < mejor_resultado:
            #memoria[i][A] = mejor_resultado
            #pasos[i][A] = mejor_paso
            return mejor_resultado, mejor_paso
        if no_comprar > mejor_resultado:
            #memoria[i][A] = no_comprar
            #pasos[i][A] = no_comprar_paso
            return no_comprar, no_comprar_paso
    # Inicializamos la memoria y los pasos
    #n = len(ofertas)
    #memoria = [[-1] * (A + 1) for _ in range(n + 1)]
    #pasos = [[[] for _ in range(A + 1)] for _ in range(n + 1)]
    

    return subastasFuerzaBruta_aux(A, B, ofertas, 0)
        


def subastas_dinamico(A, B, ofertas):    
    def subastas_dinamico_aux(A, B, ofertas, i, memoria, pasos):
        # Si ya se calculó previamente la solución, simplemente retornamos
        if memoria[i][A] != -1:
            return memoria[i][A], pasos[i][A]
        
        # Si ya no quedan más ofertas, retornar 0 (caso base)
        if len(ofertas) <= i:
            return 0, []

        precio, Mini, Maxi = ofertas[i]
        
        # Si no cumple las condiciones de oferta
        if Mini > A or precio < B:
            mejor_solucion, mejor_paso = subastas_dinamico_aux(A, B, ofertas, i + 1, memoria, pasos)
            memoria[i][A] = mejor_solucion
            pasos[i][A] = mejor_paso
            return mejor_solucion, mejor_paso

        mejor_resultado = 0
        mejor_paso = []

        # Explorar asignar entre Mini y Maxi acciones
        for acciones_asignadas in range(Mini, min(A, Maxi) + 1):
            resultado, paso_actual = subastas_dinamico_aux(A - acciones_asignadas, B, ofertas, i + 1, memoria, pasos)
            resultado += precio * acciones_asignadas
            
            # Si encontramos una mejor combinación, la guardamos
            if resultado > mejor_resultado:
                mejor_resultado = resultado
                mejor_paso = [f"Asignar {acciones_asignadas} acciones a {precio}"] + paso_actual
        
        no_comprar, no_comprar_paso = subastas_dinamico_aux(A, B, ofertas, i + 1, memoria, pasos)
        # Guardar en memoria la mejor solución encontrada
        if no_comprar < mejor_resultado:
            memoria[i][A] = mejor_resultado
            pasos[i][A] = mejor_paso
            return mejor_resultado, mejor_paso
        if no_comprar > mejor_resultado:
            memoria[i][A] = no_comprar
            pasos[i][A] = no_comprar_paso
            return no_comprar, no_comprar_paso
    # Inicializamos la memoria y los pasos
    n = len(ofertas)
    memoria = [[-1] * (A + 1) for _ in range(n + 1)]
    pasos = [[[] for _ in range(A + 1)] for _ in range(n + 1)]
    

    return subastas_dinamico_aux(A, B, ofertas, 0, memoria, pasos)
        

def subastas_voraz(ofertas, A, B):
    # Ordenar ofertas por precio descendente
    ofertas_ordenadas = sorted(ofertas, key=lambda x: -x[0])
    cantidad_acciones = A
    compra_por_oferta = []

    # Recorrer las ofertas ordenadas
    for precio, minimo, maximo in ofertas_ordenadas:
        # Saltar ofertas con precio menor a B o si no se puede cumplir el mínimo
        if precio < B or minimo > cantidad_acciones:
            continue

        # Tomar la cantidad máxima posible para esta oferta
        acciones_tomadas = min(maximo, cantidad_acciones)
        compra_por_oferta.append(acciones_tomadas)
        cantidad_acciones -= acciones_tomadas

        # Terminar si ya no quedan acciones por asignar
        if cantidad_acciones == 0:
            break

    # Calcular ganancia máxima
    ganancia_maxima = sum(precio * acciones for (precio, _, _), acciones in zip(ofertas_ordenadas, compra_por_oferta))
    solucion = [f"Asignar {acciones} acciones a {precio}" for (precio, _, _), acciones in zip(ofertas_ordenadas, compra_por_oferta)]

    return ganancia_maxima, solucion

if __name__ == "__main__":
    # Definimos las ofertas en el formato (precio, mínimo, máximo)
    ofertas = [
        #(140, 200, 800), 
        (200, 300, 500),  
        (150, 200, 300),# 300 :v
        (50, 0 , 9000)

    ]

    A = 900  # Cantidad de acciones disponibles
    B = 50  # Precio mínimo aceptable por acción
    
    max_value, solucion_paso_paso = subastas_dinamico(A, B, ofertas)

    # Imprimimos los resultados
    print("Valor máximo recibido dinamico:", max_value)
    print("Paso a paso para llegar a la mejor solución:")
    for paso in solucion_paso_paso:
        print(paso)

    # Llamada al algoritmo
    resultado_final, paso_a_paso = subastas_voraz(ofertas, A, B)

    print(f"Valor máximo recibido voraz:", resultado_final)
    print("Las mejores ofertas y la cantidad de acciones asignadas son:")
    for paso in paso_a_paso:
        print(paso)



    

