from database import db
from models.category import Category
from models.task import Task


class CategoryController:
    @staticmethod
    def list_categories():
        categories = Category.query.all()
        result = []
        for category in categories:
            cat_data = category.to_dict()
            cat_data["task_count"] = Task.query.filter_by(category_id=category.id).count()
            result.append(cat_data)
        return result, 200

    @staticmethod
    def create_category(data):
        if not data:
            return {"error": "Dados inválidos"}, 400

        name = data.get("name")
        if not name:
            return {"error": "Nome é obrigatório"}, 400

        category = Category(
            name=name,
            description=data.get("description", ""),
            color=data.get("color", "#000000"),
        )

        try:
            db.session.add(category)
            db.session.commit()
            return category.to_dict(), 201
        except Exception:
            db.session.rollback()
            return {"error": "Erro ao criar categoria"}, 500

    @staticmethod
    def update_category(cat_id, data):
        category = db.session.get(Category, cat_id)
        if not category:
            return {"error": "Categoria não encontrada"}, 404

        if "name" in data:
            category.name = data["name"]
        if "description" in data:
            category.description = data["description"]
        if "color" in data:
            category.color = data["color"]

        try:
            db.session.commit()
            return category.to_dict(), 200
        except Exception:
            db.session.rollback()
            return {"error": "Erro ao atualizar"}, 500

    @staticmethod
    def delete_category(cat_id):
        category = db.session.get(Category, cat_id)
        if not category:
            return {"error": "Categoria não encontrada"}, 404

        try:
            db.session.delete(category)
            db.session.commit()
            return {"message": "Categoria deletada"}, 200
        except Exception:
            db.session.rollback()
            return {"error": "Erro ao deletar"}, 500
