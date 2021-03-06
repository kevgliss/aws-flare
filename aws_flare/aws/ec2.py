from marshmallow import fields, validates_schema
from marshmallow.exceptions import ValidationError

from ..core import FlareSchema
from ..utils import is_private, in_network
from .iam import IAMSchema


class IPRangeSchema(FlareSchema):
    cidr_ip = fields.String()

    @validates_schema
    def external_ip(self, data):
        if not is_private(data['cidr_ip']):
            for network in self.context.get('network_whitelist', []):
                if in_network(data, network):
                    break
            else:
                raise ValidationError('Security group contains public range: {range}.'.format(
                    range=data['cidr_ip']
                ), ['cidr_ip'])

        if data['cidr_ip'] == '0.0.0.0/0':
            raise ValidationError('Security group allows all ranges via 0.0.0.0/0.', ['cidr_ip'])


class IpPermissionSchema(FlareSchema):
    ip_ranges = fields.Nested(IPRangeSchema, many=True)
    ip_protocol = fields.String()
    to_port = fields.Integer()
    from_port = fields.Integer()

    @validates_schema
    def rules(self, data):
        if (data['to_port'] - data['from_port']) > 1000:
            raise ValidationError('Think about reducing the number of available ports.', ['from_port', 'to_port'])


class SecurityGroupSchema(FlareSchema):
    group_id = fields.String()
    group_name = fields.String()
    ip_permissions = fields.Nested(IpPermissionSchema, many=True, error_messages={'type': 'No security group primitive provided, security group rules will not be validated.'})


class LaunchConfigSchema(FlareSchema):
    security_groups = fields.Nested(SecurityGroupSchema, many=True)
    iam_instance_profile = fields.Nested(IAMSchema)
    image = fields.Dict()

