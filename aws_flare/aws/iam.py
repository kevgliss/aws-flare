from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from ..core import FlareSchema, DictField, OrField


class IAMInstanceProfileSchema(FlareSchema):
    instance_profile_name = fields.String()

    @validates('instance_profile_name')
    def app_specific(self, data):
        if data in self.context.get('invalid_instance_profiles', []):
            raise ValidationError('You are using an invalid IAM profile, consider moving onto an application specific group.')


class IAMRolePolicyStatementSchema(FlareSchema):
    resource = OrField([
        fields.List(fields.String()),
        fields.String()
    ])

    action = OrField([
        fields.List(fields.String()),
        fields.String()
    ])

    effect = fields.String()

    @validates('action')
    def validate_action(self, data):
        for d in data:
            if'*' in d:
                raise ValidationError('You have a wildcard statement "{0}" in your policy consider making it explict.'.format(
                    d
                ))


class IAMRolePolicySchema(FlareSchema):
    statement = fields.Nested(IAMRolePolicyStatementSchema, many=True)


class IAMSchema(FlareSchema):
    managed_policies = fields.List(fields.Dict())
    assume_role_policy_document = fields.Dict()

    rolepolicies = DictField(
        fields.String(),
        fields.Nested(IAMRolePolicySchema)
    )
    instance_profiles = fields.Nested(IAMInstanceProfileSchema, many=True)
    role = fields.Dict()

