from db import db

#this is what is called a "secondary table" in SQLAlchemy, its effectively a mapping

class ItemTags(db.Model):
    __tablename__ = "item_tags"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)