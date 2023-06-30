from marshmallow import Schema, fields, validate, post_load

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    store_id = fields.Str(required=True)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)

class ItemUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    price = fields.Float(validate=validate.Range(min=0))
    store_id = fields.Str()

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))

    @post_load
    def make_store(self, data, **kwargs):
        return Store(**data)