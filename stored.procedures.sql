DELIMITER //

-- =============================================
-- STORED PROCEDURES  PARA USUARIOS
-- =============================================
CREATE PROCEDURE sp_crear_usuario(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255)
)
BEGIN
    INSERT INTO usuarios (username, email, password_hash) 
    VALUES (p_username, p_email, p_password_hash);
END//

CREATE PROCEDURE sp_listar_usuarios()
BEGIN
    SELECT id, username, email, creado_en FROM usuarios;
END//

CREATE PROCEDURE sp_actualizar_usuario(
    IN p_id INT,
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255)
)
BEGIN
    UPDATE usuarios 
    SET username = p_username, email = p_email, password_hash = p_password_hash
    WHERE id = p_id;
END//

CREATE PROCEDURE sp_eliminar_usuario(IN p_id INT)
BEGIN
    DELETE FROM usuarios WHERE id = p_id;
END//

-- =============================================
-- STORED PROCEDURES  PARA EMOCIONES
-- =============================================
CREATE PROCEDURE sp_crear_emocion(IN p_nombre VARCHAR(50))
BEGIN
    INSERT INTO emociones (nombre) VALUES (p_nombre);
END//

CREATE PROCEDURE sp_listar_emociones()
BEGIN
    SELECT id, nombre, emoji FROM emociones;
END//

CREATE PROCEDURE sp_actualizar_emocion(IN p_id INT, IN p_nombre VARCHAR(50))
BEGIN
    UPDATE emociones SET nombre = p_nombre WHERE id = p_id;
END//

CREATE PROCEDURE sp_eliminar_emocion(IN p_id INT)
BEGIN
    DELETE FROM emociones WHERE id = p_id;
END//

-- =============================================
-- STORED PROCEDURES  PARA ENTRADAS
-- =============================================
CREATE PROCEDURE sp_crear_entrada(
    IN p_usuario_id INT,
    IN p_fecha DATE,
    IN p_texto TEXT
)
BEGIN
    INSERT INTO entradas (usuario_id, fecha, texto) 
    VALUES (p_usuario_id, p_fecha, p_texto);
END//

CREATE PROCEDURE sp_listar_entradas()
BEGIN
    SELECT e.id, u.username, e.fecha, SUBSTRING(e.texto, 1, 50) as resumen 
    FROM entradas e 
    JOIN usuarios u ON e.usuario_id = u.id 
    ORDER BY e.fecha DESC;
END//

CREATE PROCEDURE sp_actualizar_entrada(
    IN p_id INT,
    IN p_usuario_id INT,
    IN p_fecha DATE,
    IN p_texto TEXT
)
BEGIN
    UPDATE entradas 
    SET usuario_id = p_usuario_id, fecha = p_fecha, texto = p_texto 
    WHERE id = p_id;
END//

CREATE PROCEDURE sp_eliminar_entrada(IN p_id INT)
BEGIN
    DELETE FROM entradas WHERE id = p_id;
END//

DELIMITER ;
