# Importar

from grafos import Accion
from grafos import Estado
from grafos import Nodo
from grafos import Problema

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
    costo = padre.costo
    costo += problema.costo_accion(padre.estado, accion)
    hijo.costo = costo
    padre.hijos.append(hijo)
    return hijo

def muestra_solucion(objetivo = None, problema_resolver = None):
    if not objetivo:
        print('No hay solucion')
        return
    nodo = objetivo
    while nodo:
        msg = 'Estado: {0}, Costo Total: {1}'
        estado = nodo.estado.nombre
        costo_total = nodo.costo
        print(msg.format(estado, costo_total))
        if nodo.accion:
            accion = nodo.accion.nombre
            padre = nodo.padre.estado
            costo = problema_resolver.costo_accion(padre, nodo.accion)
            msg = "<----{0} [{1}]---->"
            print(msg.format(accion, costo))
            print('-----------')
        nodo = nodo.padre

def costo_uniforme(problema):
    raiz = crear_nodo_raiz(problema)
    frontera = [raiz,]
    explorados = set()
    while True:
        print('frontera: ', [(nodo.estado.nombre, nodo.costo) for nodo in frontera])
        if not frontera:
            return None
        nodo = frontera.pop(0)
        if problema.es_objetivo(nodo.estado):
            return nodo
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
                frontera.append(hijo)
            else:
                buscar = [nodo for nodo in frontera if nodo.estado == hijo.estado]
                if buscar:
                    if hijo.costo < buscar[0].costo:
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
            frontera.sort(key = lambda nodo: nodo.costo)

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

    
    objetivo = [gerente_general]
    problema = Problema(analista_tecnologia, objetivo, acciones, costos)
    solucion = costo_uniforme(problema)
    muestra_solucion(solucion, problema)