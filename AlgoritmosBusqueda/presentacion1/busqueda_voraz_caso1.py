# Importar

from grafos import Accion
from grafos import Estado
from grafos import Nodo
from grafos import Problema

# Crear metodos auxiliares

def crear_nodo_raiz(problema):
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, None, acciones_raiz, None)
    raiz.costo = 0
    raiz.heuristicas = problema.heuristicas[estado_raiz.nombre]
    raiz.valores = dict(raiz.heuristicas.items())
    return raiz

def crear_nodo_hijo(problema, padre, accion, agregar = True):
    nuevo_estado = problema.resultado(padre.estado, accion)
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    costo = padre.costo
    costo += problema.costo_accion(padre.estado, accion)
    hijo.costo = costo
    hijo.heuristicas = problema.heuristicas[hijo.estado.nombre]
    hijo.valores = {estado: heuristica + hijo.costo for estado, heuristica in hijo.heuristicas.items()}
    if agregar:
        hijo.padre = padre
        padre.hijos.append(hijo)
    return hijo

def sacar_siguiente(frontera, metrica = 'valor', criterio = 'menor', objetivos = None):
    mejor = frontera[0]
    for nodo in frontera[1:]:
        for objetivo in objetivos:
            if metrica == 'valor':
                valor_nodo = nodo.valores[objetivo.nombre]
                valor_mejor = mejor.valores[objetivo.nombre]
                if (criterio == 'menor' and valor_nodo < valor_mejor):
                    mejor = nodo
                elif (criterio == 'mayor' and valor_nodo > valor_mejor):
                    mejor = nodo
            elif metrica == 'heuristica':
                heuristica_nodo = nodo.heuristicas[objetivo.nombre]
                heuristica_mejor = mejor.heuristicas[objetivo.nombre]
                if (criterio == 'menor' and heuristica_nodo < heuristica_mejor):
                    mejor = nodo
                elif (criterio == 'mayor' and heuristica_nodo > heuristica_mejor):
                    mejor = nodo
            if metrica == 'costo':
                if (criterio == 'menor' and nodo.costo_camino < mejor.costo_camino):
                    mejor = nodo
                elif (criterio == 'mayor' and nodo.costo_camino > mejor.costo_camino):
                    mejor = nodo
    frontera.remove(mejor)
    return mejor         


def muestra_solucion(objetivo = None, problema_resolver = None):
    if not objetivo:
        print("No hay solucion")
        return
    nodo = objetivo
    while nodo:
        msg = "Estado {0}, Valor {1}"
        estado = nodo.estado.nombre
        valores = [nodo.valores[objetivo.nombre]
                   for objetivo
                   in problema_resolver.estado_objetivo]
        valor = min(valores)
        print(msg.format(estado, valor))
        msg = "  Costo: {0}"
        costo_total = nodo.costo
        print(msg.format(costo_total))
        msg = "  Heuristica: {0}"
        heuristicas_objetivos = [nodo.heuristicas[objetivo.nombre]
                                 for objetivo
                                 in problema_resolver.estado_objetivo]
        heuristica = min(heuristicas_objetivos)
        print(msg.format(heuristica))
        if nodo.accion:
            accion = nodo.accion.nombre
            padre = nodo.padre.estado
            costo = problema_resolver.costo_accion(padre, nodo.accion)
            if accion:
                msg = "<--- {0} [{1}] ---"
                print(msg.format(accion, costo))
        nodo = nodo.padre

# Crear la funcioon que ejecuta el problema

def voraz(problema):
    raiz = crear_nodo_raiz(problema)
    frontera = [raiz, ]
    explorados = set()
    
    while True:
        if not frontera:
            return None
            
        nodo = sacar_siguiente(frontera, 'heuristica',
                            objetivos=problema.estado_objetivo, 
                            criterio='menor')
                            
        if problema.es_objetivo(nodo.estado):
            return nodo
            
        explorados.add(nodo.estado)
        
        if not nodo.acciones:
            continue
            
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crear_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            
            if hijo.estado in explorados or hijo.estado in estados_frontera:
                buscar = [nodo for nodo in frontera
                        if nodo.estado == hijo.estado]
                if buscar:
                    heuristic_hijo = [hijo.heuristicas[objetivo.nombre]
                                    for objetivo
                                    in problema.estado_objetivo]
                    heuristic_buscar = [buscar[0].heuristicas[objetivo.nombre]
                                        for objetivo
                                        in problema.estado_objetivo]
                    minimo_hijo = min(heuristic_hijo)
                    minimo_buscar = min(heuristic_buscar)
                    if minimo_hijo < minimo_buscar:
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
            else:
                frontera.append(hijo)

'''Acciones: 

- 1. Ascender a coordinador de tecnologia 
- 2. Ascender a arquitecto de datos
- 3. Ascender a jefe de mesa de ayuda
- 4. Ascender a arquitecto de soluciones
- 5. Ascender a gerente de tecnologia
- 6. Ascender a director administrativo
- 7. Ascender a gerente general'''

if __name__ == '__main__':
    # Crear todas las acciones de ascenso
    acc1 = Accion('Ascender a coordinador de tecnologia')
    acc2 = Accion('Ascender a arquitecto de datos')
    acc3 = Accion('Ascender a jefe de mesa de ayuda')
    acc4 = Accion('Ascender a arquitecto de soluciones')
    acc5 = Accion('Ascender a gerente de tecnologia')
    acc6 = Accion('Ascender a director administrativo')
    acc7 = Accion('Ascender a gerente general')

    analista_tecnologia = Estado('analista de tecnologia', [acc1, acc2])
    coordniador_tecnologia = Estado('coordinador de tecnologia', [acc2, acc4, acc3])
    arquitecto_datos = Estado('arquitecto de datos', [acc5])
    jefe_mesa_ayuda = Estado('jefe de mesa de ayuda', [acc5, acc6])
    arquitecto_soluciones = Estado('arquitecto de soluciones', [acc3, acc5])
    gerente_tecnologia = Estado('gerente de tecnologia', [acc6, acc7])
    director_administrativo = Estado('director administrativo', [acc7])
    gerente_general = Estado('gerente general', [])

    acciones = {
      'analista de tecnologia': {
        'Ascender a coordinador de tecnologia': coordniador_tecnologia,
        'Ascender a arquitecto de datos': arquitecto_datos
      },
      'coordinador de tecnologia': {
        'Ascender a arquitecto de datos': arquitecto_datos,
        'Ascender a arquitecto de soluciones': arquitecto_soluciones,
        'Ascender a jefe de mesa de ayuda': jefe_mesa_ayuda
      },
      'arquitecto de datos': {
        'Ascender a gerente de tecnologia': gerente_tecnologia
      },
      'jefe de mesa de ayuda': {
        'Ascender a gerente de tecnologia': gerente_tecnologia,
        'Ascender a director administrativo': director_administrativo
      },
      'arquitecto de soluciones': {
        'Ascender a jefe de mesa de ayuda': jefe_mesa_ayuda,
        'Ascender a gerente de tecnologia': gerente_tecnologia
      },
      'gerente de tecnologia': {
        'Ascender a director administrativo': director_administrativo,
        'Ascender a gerente general': gerente_general
      },
      'director administrativo': {
        'Ascender a gerente general': gerente_general
      },
      'gerente general': {}
    }

    costos = {
      'analista de tecnologia': {
        'Ascender a coordinador de tecnologia': 10,
        'Ascender a arquitecto de datos': 50
      },
      'coordinador de tecnologia': {
        'Ascender a arquitecto de datos': 20,
        'Ascender a arquitecto de soluciones': 30,
        'Ascender a jefe de mesa de ayuda': 15
      },
      'arquitecto de datos': {
        'Ascender a gerente de tecnologia': 100
      },
      'jefe de mesa de ayuda': {
        'Ascender a gerente de tecnologia': 40,
        'Ascender a director administrativo': 150
      },
      'arquitecto de soluciones': {
        'Ascender a jefe de mesa de ayuda': 10,
        'Ascender a gerente de tecnologia': 60
      },
      'gerente de tecnologia': {
        'Ascender a director administrativo': 70,
        'Ascender a gerente general': 80
      },
      'director administrativo': {
        'Ascender a gerente general': 40
      },
      'gerente general': {}
    }

    heuristicas = {
      'analista de tecnologia': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 45,    # Primer rol de gestion, adaptacion significativa
        'arquitecto de datos': 135,          # Alta curva tecnica, menor gestion de personal
        'jefe de mesa de ayuda': 165,        # Salto grande en gestion de personas
        'arquitecto de soluciones': 90,     # Cambio tecnico significativo
        'gerente de tecnologia': 410,        # Salto muy grande en responsabilidad
        'director administrativo': 605,       # Cambio radical de rol y responsabilidad
        'gerente general': 780              # Maxima distancia organizacional
      },
      'coordinador de tecnologia': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 0,
        'arquitecto de datos': 40,          # Transicion tecnica moderada
        'jefe de mesa de ayuda': 120,        # Transicion natural en gestion
        'arquitecto de soluciones': 45,     # Cambio de enfoque tecnico
        'gerente de tecnologia': 355,        # Salto significativo en gestion
        'director administrativo': 510,
        'gerente general': 685
      },
      'arquitecto de datos': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 0,
        'arquitecto de datos': 0,
        'jefe de mesa de ayuda': 0,        # Cambio radical de enfoque
        'arquitecto de soluciones': 0,     # Transicion tecnica relacionada
        'gerente de tecnologia': 65,        # Cambio significativo a gestion
        'director administrativo': 145,
        'gerente general': 320
      },
      'jefe de mesa de ayuda': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 0,
        'arquitecto de datos': 0,
        'jefe de mesa de ayuda': 0,
        'arquitecto de soluciones': 0,     # Cambio de enfoque significativo
        'gerente de tecnologia': 60,        # Transicion natural en gestion
        'director administrativo': 215,       # Salto grande en responsabilidad
        'gerente general': 390
      },
      'arquitecto de soluciones': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 0,
        'arquitecto de datos': 0,
        'jefe de mesa de ayuda': 40,        # Cambio a gestion operativa
        'arquitecto de soluciones': 0,
        'gerente de tecnologia': 170,        # Gran cambio a gestion estrategica
        'director administrativo': 325,
        'gerente general': 500
      },
      'gerente de tecnologia': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 0,
        'arquitecto de datos': 0,
        'jefe de mesa de ayuda': 0,
        'arquitecto de soluciones': 0,
        'gerente de tecnologia': 0,
        'director administrativo': 80,       # Transicion ejecutiva significativa
        'gerente general': 255               # Maxima responsabilidad ejecutiva
      },
      'director administrativo': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 0,
        'arquitecto de datos': 0,
        'jefe de mesa de ayuda': 0,
        'arquitecto de soluciones': 0,
        'gerente de tecnologia': 0,
        'director administrativo': 0,
        'gerente general': 85               # ultimo paso ejecutivo
      },
      'gerente general': {
        'analista de tecnologia': 0,
        'coordinador de tecnologia': 0,
        'arquitecto de datos': 0,
        'jefe de mesa de ayuda': 0,
        'arquitecto de soluciones': 0,
        'gerente de tecnologia': 0,
        'director administrativo': 0,
        'gerente general': 0
      }
    }

    objetivo = [gerente_general]
    problema = Problema(analista_tecnologia, objetivo, acciones, costos, heuristicas)
    solucion = voraz(problema)
    muestra_solucion(solucion, problema)