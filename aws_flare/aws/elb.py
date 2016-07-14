from marshmallow import fields, validates, validates_schema
from marshmallow.exceptions import ValidationError

from ..core import FlareSchema
from .ec2 import SecurityGroupSchema


class ListenerSchema(FlareSchema):
    instance_port = fields.Int()
    load_balancer_port = fields.Int()
    sslcertificate_id = fields.String()

    @validates_schema
    def validate_schema(self, data):
        if data.get('sslcertificate_id'):
            if data['load_balancer_port'] != 443:
                raise ValidationError('You are using SSL on the non-standard port: {port}'.format(
                    port=data['load_balancer_port']
                ), ['sslcertificate_id'])


class ListenerDescriptionSchema(FlareSchema):
    listener = fields.Nested(ListenerSchema)
    policy_names = fields.List(fields.String)

    @validates_schema
    def validate_policies(self, data):
        for name in data:
            if not name.startswith('ELBSecurityPolicy'):
                raise ValidationError('Custom listener policies are not recommended.', ['policy_names'])
            else:
                if name != self.context.get('standard_cipher_policy'):
                    raise ValidationError('You are using cipher policy {name} instead of the standard {standard}'.format(
                        name=name,
                        standard=self.context.get('standard_cipher_policy')
                    ), ['policy_names'])


class ELBSchema(FlareSchema):
    listener_descriptions = fields.Nested(ListenerDescriptionSchema, many=True)
    security_groups = fields.Nested(SecurityGroupSchema, many=True)
    load_balancer_name = fields.String()
    vpc_id = fields.String()
    scheme = fields.String()
    dnsname = fields.String()
    cname = fields.String()

    @validates('scheme')
    def validates_scheme(self, data):
        if data == 'internet-facing':
            raise ValidationError('ELB is externally facing, consider moving your service internally.')

    @validates('vpc_id')
    def validates_vpc_id(self, data):
        if not data:
            raise ValidationError('Consider moving your service to the VPC.')

    @validates('listener_descriptions')
    def validate_listener_description(self, data):
        for listener in data:
            if listener['listener'].get('sslcertificate_id'):
                break
        else:
            raise ValidationError('You have an ELB but have not configured TLS/SSL. Consider adding TLS.')

