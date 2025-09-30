-- STORED PROCEDURES para diario_emociones
DELIMITER //

-- =============================================
-- PROCEDIMIENTOS PARA USUARIOS
-- =============================================
CREATE PROCEDURE sp_crear_usuario(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255)
)
BEGIN
    INSERT INTO usuarios (username, email, password_hash) 
    VALUES (p_username, p_email, p_password_hash);
    SELECT LAST_INSERT_ID() as id;
END//

CREATE PROCEDURE sp_obtener_usuario(IN p_id INT)
BEGIN
    SELECT id, username, email, password_hash, creado_en 
    FROM usuarios WHERE id = p_id;
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

CREATE PROCEDURE sp_listar_usuarios()
BEGIN
    SELECT id, username, email, creado_en FROM usuarios ORDER BY username;
END//

-- =============================================
-- PROCEDIMIENTOS PARA EMOCIONES
-- =============================================
CREATE PROCEDURE sp_crear_emocion(IN p_nombre VARCHAR(50))
BEGIN
    INSERT INTO emociones (nombre) VALUES (p_nombre);
    SELECT LAST_INSERT_ID() as id;
END//

CREATE PROCEDURE sp_obtener_emocion(IN p_id INT)
BEGIN
    SELECT id, nombre FROM emociones WHERE id = p_id;
END//

CREATE PROCEDURE sp_actualizar_emocion(IN p_id INT, IN p_nombre VARCHAR(50))
BEGIN
    UPDATE emociones SET nombre = p_nombre WHERE id = p_id;
END//

CREATE PROCEDURE sp_eliminar_emocion(IN p_id INT)
BEGIN
    DELETE FROM emociones WHERE id = p_id;
END//

CREATE PROCEDURE sp_listar_emociones()
BEGIN
    SELECT id, nombre FROM emociones ORDER BY nombre;
END//

-- =============================================
-- PROCEDIMIENTOS PARA ENTRADAS
-- =============================================
CREATE PROCEDURE sp_crear_entrada(
    IN p_usuario_id INT,
    IN p_fecha DATETIME,
    IN p_texto TEXT,
    IN p_emociones_ids VARCHAR(255)
)
BEGIN
    DECLARE v_entrada_id INT;
    
    -- Insertar la entrada principal
    INSERT INTO entradas (usuario_id, fecha, texto) 
    VALUES (p_usuario_id, p_fecha, p_texto);
    
    SET v_entrada_id = LAST_INSERT_ID();
    
    -- Insertar relaciones con emociones si se proporcionan
    IF p_emociones_ids IS NOT NULL AND p_emociones_ids != '' THEN
        INSERT INTO entrada_emocion (entrada_id, emocion_id)
        SELECT v_entrada_id, id 
        FROM emociones 
        WHERE FIND_IN_SET(id, p_emociones_ids) > 0;
    END IF;
    
    SELECT v_entrada_id as id;
END//

CREATE PROCEDURE sp_obtener_entrada(IN p_id INT)
BEGIN
    SELECT e.*, u.username 
    FROM entradas e 
    JOIN usuarios u ON e.usuario_id = u.id 
    WHERE e.id = p_id;
END//

CREATE PROCEDURE sp_obtener_emociones_entrada(IN p_entrada_id INT)
BEGIN
    SELECT em.id, em.nombre 
    FROM entrada_emocion ee 
    JOIN emociones em ON ee.emocion_id = em.id 
    WHERE ee.entrada_id = p_entrada_id;
END//

CREATE PROCEDURE sp_actualizar_entrada(
    IN p_id INT,
    IN p_texto TEXT,
    IN p_emociones_ids VARCHAR(255)
)
BEGIN
    -- Actualizar el texto de la entrada
    UPDATE entradas SET texto = p_texto WHERE id = p_id;
    
    -- Actualizar las emociones (eliminar antiguas y agregar nuevas)
    IF p_emociones_ids IS NOT NULL THEN
        -- Eliminar emociones antiguas
        DELETE FROM entrada_emocion WHERE entrada_id = p_id;
        
        -- Insertar nuevas emociones
        IF p_emociones_ids != '' THEN
            INSERT INTO entrada_emocion (entrada_id, emocion_id)
            SELECT p_id, id 
            FROM emociones 
            WHERE FIND_IN_SET(id, p_emociones_ids) > 0;
        END IF;
    END IF;
END//

CREATE PROCEDURE sp_eliminar_entrada(IN p_id INT)
BEGIN
    DELETE FROM entradas WHERE id = p_id;
END//

CREATE PROCEDURE sp_listar_entradas_usuario(IN p_usuario_id INT)
BEGIN
    SELECT e.*, GROUP_CONCAT(em.nombre SEPARATOR ', ') as emociones
    FROM entradas e 
    LEFT JOIN entrada_emocion ee ON e.id = ee.entrada_id 
    LEFT JOIN emociones em ON ee.emocion_id = em.id 
    WHERE e.usuario_id = p_usuario_id 
    GROUP BY e.id 
    ORDER BY e.fecha DESC;
END//

-- =============================================
-- PROCEDIMIENTOS PARA REPORTES
-- =============================================
CREATE PROCEDURE sp_reporte_emociones_usuario(
    IN p_usuario_id INT,
    IN p_dias INT
)
BEGIN
    SELECT 
        em.nombre as emocion,
        COUNT(ee.emocion_id) as frecuencia,
        ROUND((COUNT(ee.emocion_id) * 100.0 / (
            SELECT COUNT(*) 
            FROM entrada_emocion ee2 
            JOIN entradas e2 ON ee2.entrada_id = e2.id 
            WHERE e2.usuario_id = p_usuario_id 
            AND e2.fecha >= DATE_SUB(CURDATE(), INTERVAL p_dias DAY)
        )), 2) as porcentaje
    FROM entrada_emocion ee 
    JOIN emociones em ON ee.emocion_id = em.id 
    JOIN entradas e ON ee.entrada_id = e.id 
    WHERE e.usuario_id = p_usuario_id 
    AND e.fecha >= DATE_SUB(CURDATE(), INTERVAL p_dias DAY)
    GROUP BY em.id, em.nombre
    ORDER BY frecuencia DESC;
END//

CREATE PROCEDURE sp_reporte_estadisticas_usuario(IN p_usuario_id INT)
BEGIN
    SELECT 
        COUNT(*) as total_entradas,
        COUNT(DISTINCT ee.emocion_id) as emociones_diferentes,
        MIN(e.fecha) as primera_entrada,
        MAX(e.fecha) as ultima_entrada,
        AVG(LENGTH(e.texto)) as longitud_promedio
    FROM entradas e 
    LEFT JOIN entrada_emocion ee ON e.id = ee.entrada_id 
    WHERE e.usuario_id = p_usuario_id;
END//

DELIMITER ;