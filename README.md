 # OPC_proyect


## Sistema de Monitoreo y Visualización de Datos PLC
### Descripción

Este proyecto, alojado en OPC_proyect, se centra en el monitoreo y visualización de datos provenientes de un PLC mediante un servidor OPC. El sistema está diseñado para trabajar con datos en tiempo real, capturando información directamente desde el PLC y presentándola de manera visual a través de una interfaz web.

### Características Principales
Integración con PLC a través de Servidor OPC: El sistema se conecta directamente con un PLC utilizando un servidor OPC, lo que permite una comunicación fluida y en tiempo real con el equipo.

Cliente OPC UA Multihilo en Python: Se ha implementado un cliente OPC UA en Python que utiliza múltiples hilos para optimizar la recopilación de datos.

Base de Datos MySQL: Todos los servidores y tags OPC UA se almacenan en una base de datos MySQL, lo que facilita la gestión y consulta de estos elementos.

Comunicación con Azure: El sistema cuenta con un programa que utiliza un cliente socket para inyectar los datos recopilados en una base de datos SQL Server alojada en Azure.

Interfaz Web en JavaScript: Se ha desarrollado una interfaz web que consume los datos almacenados y los presenta de forma gráfica y tabular para su análisis.

Seguridad y Confidencialidad: El repositorio en GitHub está configurado en modo privado para garantizar la protección de la información confidencial.

### Archivos Principales
Cliente OPC R - Servidor Socket W.py: Script principal para la comunicación con el servidor OPC y la gestión de datos.

Cliente Socket insertDB.py: Programa encargado de inyectar los datos en la base de datos de Azure.

index.php y leeazure.html: Archivos relacionados con la interfaz web para la visualización de datos.


## Contribuciones
Si estás interesado en contribuir o tienes alguna pregunta sobre el proyecto, no dudes en contactar al autor principal, Jorge Peñaloza, a través de su correo electrónico: jorge.penaloza.guerra@gmail.com.

### Desarrolladores
Este proyecto fue desarrollado por Jorge Peñaloza en colaboración con Ana Javiera Valdés.

### Conclusión
Este proyecto representa un esfuerzo significativo en la integración de tecnologías de automatización y sistemas de información. La combinación de PLCs, servidores OPC, bases de datos y tecnologías web proporciona una solución robusta y escalable para el monitoreo y análisis de datos en tiempo real.
