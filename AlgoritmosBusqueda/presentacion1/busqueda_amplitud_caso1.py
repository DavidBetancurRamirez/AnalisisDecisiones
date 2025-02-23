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
    return raiz

def crear_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    padre.hijos.append(hijo)
    return hijo

def muestra_solucion(objetivo = None):
    if not objetivo:
        print('No hay solucion')
        return
    nodo = objetivo
    while nodo:
        msg = 'Estado: {0}'
        print(msg.format(nodo.estado.nombre))
        if nodo.accion:
            msg = "<----{0}---->"
            print(msg.format(nodo.accion.nombre))
        nodo = nodo.padre


# Crear la funcion que ejecuta el problema

def amplitud(problema):
    raiz = crear_nodo_raiz(problema)
    if problema.es_objetivo(raiz.estado):
        return raiz
    frontera = [raiz,]
    explorados = set()
    while True:
        print('frontera: ', [nodo.estado.nombre for nodo in frontera])
        print('explorados: ', [estado.nombre for estado in explorados])
        if not frontera:
            return None
        nodo = frontera.pop(0)
        print('escoge: ', nodo.estado.nombre)
        print('------------')
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crear_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if (hijo.estado not in explorados and hijo.estado not in estados_frontera):
                if problema.es_objetivo(hijo.estado):
                    return hijo
                frontera.append(hijo)

# Definir las clases

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

    objetivo = [gerente_general]
    problema = Problema(analista_tecnologia, objetivo, acciones)
    solucion = amplitud(problema)
    muestra_solucion(solucion)