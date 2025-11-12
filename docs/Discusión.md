## Discusión parámetros
Como se puede observar en la carpeta '/code/' para los tres controladores 
se define la velocidad 'V' de la misma forma.

V es una velocidad variable que se define con una función escalón que reduce la velocidad
cuanto mayor es el error, la idea detrás de esto es que si el coche está alineado con
la linea de forma estable, como por ejemplo en una recta, podemos aumentar la velocidad sin perder
mucha estabilidad, pero si el error es mayor nos interesa ir más lento para que el coche tenga
tiempo de alinearse con la recta.

Esto sin embargo tiene la contra de que en una curva pude alinearse momentanemente con la recta
y pegar un acelerón que desestabilice la trayectoria. La función definida V se ha definido teniendo en
cuenta la forma de la pista y los otros parámetros definidos a través de prueba y error.

Los parámetros definidos para la velocidad angular son:
kp = 0.008
ki = 0.000005
kd = 0.003


## Discusión métodos
A continuación discutiremos las ventajas y desventajas de los tres tipos de controladores
implementados estudiando los tiempos obtenidos.

Tabla tiempos

| Controlador | Tiempo (s) |
|-------------|------------|
| P           | 123,05     |
| PD          | 119,17     |
| PID         | 124,23     |

**PD aporta mayor estabilidad en esta pista:** 
La acción derivativa atenúa oscilaciones y mejora la respuesta ante cambios (principalmente las curvas), lo que reduce el tiempo total respecto a solo P.

**PID muestra más inestabilidad aquí debido a la acción integral:** 
La acumulación de error puede inducir correcciones excesivas en las curvas (Por el factor integral), provocando sobreimpulsos y peores tiempos repecto a P y PD.