import hashlib

from src.models.database import get_db


def hash_password(plain: str) -> str:
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()


def _row_to_public_dict(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }


def get_todos_usuarios():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    return [_row_to_public_dict(row) for row in cursor.fetchall()]


def get_usuario_por_id(usuario_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    return _row_to_public_dict(row) if row else None


def login_usuario(email, senha):
    db = get_db()
    cursor = db.cursor()
    senha_hash = hash_password(senha)
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha_hash),
    )
    row = cursor.fetchone()
    if row:
        return {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "tipo": row["tipo"],
        }
    return None


def criar_usuario(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, hash_password(senha), tipo),
    )
    db.commit()
    return cursor.lastrowid
