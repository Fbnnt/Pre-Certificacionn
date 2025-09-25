from base.config.mysqlconection import connectToMySQL
from flask import flash

class Viaje:
    db = "proyecto_crud"

    def __init__(self, data):
        self.id = data['id']
        self.destino = data['destino']
        self.descripcion = data['descripcion']
        self.fecha_inicio = data['fecha_inicio']
        self.fecha_fin = data['fecha_fin']
        self.planificador_id = data['planificador_id']
        self.planificador = data.get('planificador', None)

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO viajes (destino, descripcion, fecha_inicio, fecha_fin, planificador_id)
            VALUES (%(destino)s, %(descripcion)s, %(fecha_inicio)s, %(fecha_fin)s, %(planificador_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def obtener_todos(cls):
        query = """
            SELECT viajes.*, usuarios.nombre AS planificador
            FROM viajes
            JOIN usuarios ON viajes.planificador_id = usuarios.id;
        """
        resultados = connectToMySQL(cls.db).query_db(query)
        return [cls(row) for row in resultados]

    @classmethod
    def obtener_por_id(cls, viaje_id):
        query = """
            SELECT viajes.*, usuarios.nombre AS planificador
            FROM viajes
            JOIN usuarios ON viajes.planificador_id = usuarios.id
            WHERE viajes.id = %(id)s;
        """
        data = {'id': viaje_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def unirse(cls, usuario_id, viaje_id):
        query = "INSERT INTO viajes_usuarios (usuario_id, viaje_id) VALUES (%(usuario_id)s, %(viaje_id)s);"
        data = {'usuario_id': usuario_id, 'viaje_id': viaje_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def cancelar_union(cls, usuario_id, viaje_id):
        query = "DELETE FROM viajes_usuarios WHERE usuario_id = %(usuario_id)s AND viaje_id = %(viaje_id)s;"
        data = {'usuario_id': usuario_id, 'viaje_id': viaje_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def eliminar(cls, viaje_id):
        query = "DELETE FROM viajes WHERE id = %(id)s;"
        data = {'id': viaje_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def viajes_usuario(cls, usuario_id):
        query = """
            SELECT viajes.*, usuarios.nombre AS planificador
            FROM viajes
            JOIN usuarios ON viajes.planificador_id = usuarios.id
            LEFT JOIN viajes_usuarios ON viajes.id = viajes_usuarios.viaje_id
            WHERE viajes.planificador_id = %(usuario_id)s OR viajes_usuarios.usuario_id = %(usuario_id)s
            GROUP BY viajes.id;
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(cls.db).query_db(query, data)
        return [cls(row) for row in resultados]

    @classmethod
    def viajes_otros(cls, usuario_id):
        query = """
            SELECT viajes.*, usuarios.nombre AS planificador
            FROM viajes
            JOIN usuarios ON viajes.planificador_id = usuarios.id
            WHERE viajes.id NOT IN (
                SELECT viaje_id FROM viajes_usuarios WHERE usuario_id = %(usuario_id)s
                UNION
                SELECT id FROM viajes WHERE planificador_id = %(usuario_id)s
            );
        """
        data = {'usuario_id': usuario_id}
        resultados = connectToMySQL(cls.db).query_db(query, data)
        return [cls(row) for row in resultados]

    @classmethod
    def usuarios_unidos(cls, viaje_id):
        query = """
            SELECT usuarios.nombre, usuarios.apellido
            FROM viajes_usuarios
            JOIN usuarios ON viajes_usuarios.usuario_id = usuarios.id
            WHERE viajes_usuarios.viaje_id = %(viaje_id)s;
        """
        data = {'viaje_id': viaje_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validar(data):
        is_valid = True
        if not data.get('destino'):
            flash("El destino es obligatorio.", "viaje")
            is_valid = False
        if not data.get('descripcion'):
            flash("La descripción es obligatoria.", "viaje")
            is_valid = False
        if not data.get('fecha_inicio'):
            flash("La fecha de inicio es obligatoria.", "viaje")
            is_valid = False
        if not data.get('fecha_fin'):
            flash("La fecha de fin es obligatoria.", "viaje")
            is_valid = False
        # Validaciones de fechas
        from datetime import datetime
        try:
            fecha_inicio = datetime.strptime(data['fecha_inicio'], "%Y-%m-%d")
            fecha_fin = datetime.strptime(data['fecha_fin'], "%Y-%m-%d")
            if fecha_inicio > datetime.now():
                flash("La fecha de inicio no puede ser futura.", "viaje")
                is_valid = False
            if fecha_fin < fecha_inicio:
                flash("La fecha de fin no puede ser anterior a la fecha de inicio.", "viaje")
                is_valid = False
        except Exception:
            flash("Formato de fecha inválido.", "viaje")
            is_valid = False
        return is_valid