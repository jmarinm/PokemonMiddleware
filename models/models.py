from marshmallow import Schema, fields


class PokemonListed (Schema):
    id = fields.Integer()
    name = fields.String()
    image = fields.String()