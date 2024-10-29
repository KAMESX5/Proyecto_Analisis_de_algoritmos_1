
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
    #usamos Timsort para ordenar la lista por el precio
    ofertas_ordenadas = sorted(ofertas, key=lambda x: -x[0])# peso = O(nlogn)
    cantidad_acciones = A
    compra_por_oferta = []
    # Recorrer las ofertas ordenadas
    for i in range(len(ofertas_ordenadas)):
        precio, minimo, maximo = ofertas_ordenadas[i]
        # Saltar si la oferta no cumple con el mínimo o si el precio es menor que B
        if precio < B:
            continue
        
        # verificar si es mejor quitarle aciones al anterior
        if (minimo > cantidad_acciones or cantidad_acciones == 0) and i > 0:
            precio_an, minimo_an, maximo_an = ofertas_ordenadas[i-1]
            faltantes = minimo - cantidad_acciones
            if compra_por_oferta[-1] - faltantes < maximo_an:
                ganancia_antes = precio_an * compra_por_oferta[-1]
                ganacia_quitando = (precio_an * (compra_por_oferta[-1] - faltantes)) + (precio * minimo_an)
                if ganacia_quitando > ganancia_antes:
                    compra_por_oferta[-1] = compra_por_oferta[-1] - faltantes
                    cantidad_acciones += faltantes
                else:
                    continue
            else:
                continue
        # Si la oferta puede tomar todas las acciones restantes
        if maximo > cantidad_acciones:
            compra_por_oferta.append(cantidad_acciones)
            cantidad_acciones = 0
        else:
            # Asignar el máximo permitido por la oferta
            cantidad_acciones -= maximo
            compra_por_oferta.append( maximo)
            
    ganancia_maxima = 0
    indice = 0
    solucion = []
    for precio, minimo, maximo in ofertas_ordenadas:
        if indice >= len(compra_por_oferta):
            break
        ganancia_maxima += precio * compra_por_oferta[indice]
        solucion.append(f"Asignar {compra_por_oferta[indice]} acciones a {precio}")
        indice += 1


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



    

