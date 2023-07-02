from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import ItemSchema, TagAndItemSchema
from Models.tag import TagModel
from Models import TagModel, StoreModel, ItemModel

blp = Blueprint("Tags","tags", __name__, description="Operations on tags.")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError as e:
            abort(409, message="Tag with that name already exists.")
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="Deletes a tag if it is not linked to any items.")
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Tag is linked to items. Not deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(400, message="Tag is linked to items. Not deleted.")

    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema) #order of decorators matters
    def put(self, tag_data, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag:
            tag.name = tag_data["name"]
        else:
            tag = TagModel(id=tag_id, **tag_data)

        db.session.add(tag)
        db.session.commit()
        return tag

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagAndItemSchema)
    def post(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

    def delete(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "Tag removed from item."}