from marshmallow import Schema, fields


class ReviewSchemaRequest(Schema):
    review = fields.Str(required=True)
    
class ReviewSchema(Schema):
    review = fields.Str(required=True)
    sentiment = fields.Str(required=True)