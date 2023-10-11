CREATE TABLE ServidorOPC (
    id INT PRIMARY KEY,
    url VARCHAR(255)
);

CREATE TABLE TagOPC (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    idServidor INT,
    FOREIGN KEY (idServidor) REFERENCES ServidorOPC(id)
);
