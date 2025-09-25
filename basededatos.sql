-- creamos la base de datos si no existe --
CREATE DATABASE IF NOT EXISTS Pre_certificacion;

-- Usamos la base de datos que acabamos de crear --
USE Pre_certificacion;

-- Tabla de usuario --
CREATE TABLE usuarios (
id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(45) NOT NULL,
	apellido VARCHAR(45) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
    )
   
ENGINE = InnoDB;

-- TABLA DE CITAS --
CREATE TABLE citas(
id INT NOT NULL AUTO_INCREMENT,
    cita TEXT NOT NULL,
    autor_id INT NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX fk_citas_usuarios_idx(autor_id ASC),
    CONSTRAINT fk_citas_usuarios    
	FOREIGN KEY (autor_id)
	REFERENCES usuarios (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
)
ENGINE = InnoDB;

-- TABLA DE FAVORITOS --
CREATE TABLE favoritos(
	id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    cita_id INT NOT NULL,
    PRIMARY KEY (id),
    INDEX fk_citas_usuarios_idx(usuario_id ASC),
    INDEX fk_favoritos_citas_idx(cita_id ASC),
    CONSTRAINT fk_favoritos_usuarios
		FOREIGN KEY (usuario_id)
		REFERENCES usuarios (id)
		ON DELETE CASCADE
		ON UPDATE NO ACTION,
	CONSTRAINT fk_favoritos_citas
		FOREIGN KEY (cita_id)
		REFERENCES citas (id)
		ON DELETE CASCADE
		ON UPDATE NO ACTION
)
CREATE TABLE viajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destino VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    planificador_id INT NOT NULL,
    FOREIGN KEY (planificador_id) REFERENCES usuarios(id)
);

CREATE TABLE viajes_usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    viaje_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (viaje_id) REFERENCES viajes(id)
);