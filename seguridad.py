import clips #Importar la libreria de clips

env = clips.Environment()# Creación del entorno CLIPS
env.clear()  # Limpia cualquier regla previa en memoria

#Reglas
#El defrule para definir la regla
#?e representa una variable que almacena el nombre del equipo
#Luego empiezo a definir las reglas utilizando datos
#Ejemplo firewall ?e activo, antivirus ?e actualizado es decir funciona por condición-acción
#Imprime el diagnostico de seguridad segun datos
R1 = '(defrule sistema_seguro (and (firewall ?e activo) (antivirus ?e actualizado) (contrasena ?e segura) (red_publica ?e no)) => (printout t "El equipo " ?e " es un SISTEMA SEGURO." crlf))'

R2 = '(defrule riesgo_medio (and (firewall ?e activo) (antivirus ?e actualizado) (contrasena ?e debil)) => (printout t "El equipo " ?e " tiene RIESGO MEDIO." crlf))'

R3 = '(defrule riesgo_alto (and (firewall ?e inactivo) (antivirus ?e no_actualizado)) => (printout t "El equipo " ?e " tiene RIESGO ALTO." crlf))'

R4 = '(defrule vulnerabilidad_critica (and (firewall ?e inactivo) (antivirus ?e no_actualizado) (contrasena ?e debil) (red_publica ?e si)) => (printout t "El equipo " ?e " tiene VULNERABILIDAD CRITICA." crlf))'

R5 = '(defrule vulnerabilidad_alta_firewall (and (firewall ?e inactivo) (antivirus ?e actualizado) (contrasena ?e segura) (red_publica ?e no)) => (printout t "El equipo " ?e " tiene RIESGO ALTO POR FIREWALL DESACTIVADO." crlf))'

R6 = '(defrule critica_firewall_red (and (firewall ?e inactivo) (red_publica ?e si)) => (printout t "El equipo " ?e " tiene VULNERABILIDAD CRITICA por firewall inactivo y red publica." crlf))'

R7 = '(defrule riesgo_alto_antivirus_red (and (antivirus ?e no_actualizado) (red_publica ?e si)) => (printout t "El equipo " ?e " tiene RIESGO ALTO por antivirus desactualizado en red publica." crlf))'

R8 = '(defrule riesgo_medio_red_publica (and (firewall ?e activo) (antivirus ?e actualizado) (contrasena ?e segura) (red_publica ?e si)) => (printout t "El equipo " ?e " tiene RIESGO MEDIO por uso de red publica." crlf))'

R9 = '(defrule riesgo_alto_contrasena_red (and (contrasena ?e debil) (red_publica ?e si)) => (printout t "El equipo " ?e " tiene RIESGO ALTO por contraseña debil en red publica." crlf))'

R10 = '(defrule riesgo_medio_antivirus_desactualizado (and (firewall ?e activo) (antivirus ?e no_actualizado) (red_publica ?e no)) => (printout t "El equipo " ?e " tiene RIESGO MEDIO por antivirus desactualizado." crlf))'

#Utilizo salience para decir que esta regla tiene menor prioidad que las anteriores, por ello esta en el final

R11 = '(defrule evaluacion_general (declare (salience -10)) (and (firewall ?e ?f) (antivirus ?e ?a) (contrasena ?e ?c) (red_publica ?e ?r)) => (printout t "El equipo " ?e " requiere evaluacion adicional de seguridad." crlf))'

#Construcción de las reglas 
env.build(R1)
env.build(R2)
env.build(R3)
env.build(R4)
env.build(R5)
env.build(R6)
env.build(R7)
env.build(R8)
env.build(R9)
env.build(R10)
env.build(R11)

#Entradas usuario

print("=== SISTEMA EXPERTO DE SEGURIDAD ===")

pc = input("Nombre del equipo: ")

firewall = input("Firewall (activo/inactivo): ").lower()
antivirus = input("Antivirus (actualizado/no_actualizado): ").lower()
contrasena = input("Contraseña (segura/debil): ").lower()
red = input("¿Usa red pública? (si/no): ").lower()

#Validación de las reglas

valores_firewall = ["activo", "inactivo"]
valores_antivirus = ["actualizado", "no_actualizado"]
valores_contrasena = ["segura", "debil"]
valores_red = ["si", "no"]


#Uso de varios if para verificar si el dato ingresado por usuario es valido
if firewall not in valores_firewall:
    print("Valor inválido para firewall")
    exit()

if antivirus not in valores_antivirus:
    print("Valor inválido para antivirus")
    exit()

if contrasena not in valores_contrasena:
    print("Valor inválido para contraseña")
    exit()

if red not in valores_red:
    print("Valor inválido para red pública")
    exit()

#Los datos ingresados se convierten en hechos dentro del sistema experto.

env.assert_string(f'(firewall {pc} {firewall})')
env.assert_string(f'(antivirus {pc} {antivirus})')
env.assert_string(f'(contrasena {pc} {contrasena})')
env.assert_string(f'(red_publica {pc} {red})')

#Ejecución 

res = env.run()
print("Reglas ejecutadas:", res)