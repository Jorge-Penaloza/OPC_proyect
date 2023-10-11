<?php
header("Content-Type: application/json"); // Establecer el tipo de contenido a JSON
header('Access-Control-Allow-Origin: *'); // Permitir peticiones CORS desde cualquier dominio
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: X-Requested-With, Content-Type, Origin, Authorization, Accept, Client-Security-Token, Accept-Encoding');



$serverName = "opc-pruebas0001-server.database.windows.net,1433";
$database = "opc-pruebas0001";
$username = "";
$password = "";

$dsn = "sqlsrv:Server=$serverName;Database=$database";

$response = []; // Array para almacenar la respuesta

try {
    // Establecer conexión
    $conn = new PDO($dsn, $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Consultar datos de la tabla servidoresOPC
    $query = "SELECT TOP 1 [Fecha], [temperatura], [humedad], [motor]
    FROM [dbo].[excel]
    ORDER BY [Fecha] DESC;";
    $stmt = $conn->query($query);
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Agregar los datos al array de respuesta
    $response['data'] = $rows;

    // Ingestar (insertar) nuevos datos en la tabla servidoresOPC
    // (Esto está comentado en tu código original, así que lo dejaré comentado aquí también)
    /*
    $newData = array(
        'urlServerOPC' => 'opc://example.com',
        'nombreOPC' => 'ExampleOPC'
    );
    $insertQuery = "INSERT INTO [dbo].[servidoresOPC] (urlServerOPC, nombreOPC) VALUES (:urlServerOPC, :nombreOPC)";
    $stmt = $conn->prepare($insertQuery);
    $stmt->execute($newData);
    */

} catch (PDOException $e) {
    $response['error'] = "Error en la conexión: " . $e->getMessage();
}

// Imprimir la respuesta en formato JSON
echo json_encode($response,JSON_UNESCAPED_SLASHES);
?>
