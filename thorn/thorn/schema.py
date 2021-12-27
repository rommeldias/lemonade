# -*- coding: utf-8 -*-
import datetime
import json
from copy import deepcopy
from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE, INCLUDE
from marshmallow.validate import OneOf
from flask_babel import gettext
from thorn.models import *


def partial_schema_factory(schema_cls):
    schema = schema_cls(partial=True)
    for field_name, field in list(schema.fields.items()):
        if isinstance(field, fields.Nested):
            new_field = deepcopy(field)
            new_field.schema.partial = True
            schema.fields[field_name] = new_field
    return schema


def translate_validation(validation_errors):
    for field, errors in list(validation_errors.items()):
        if isinstance(errors, dict):
            validation_errors[field] = translate_validation(errors)
        else:
            validation_errors[field] = [gettext(error) for error in errors]
        return validation_errors


def load_json(str_value):
    try:
        return json.loads(str_value)
    except BaseException:
        return None


# region Protected\s*
# endregion

class BaseSchema(Schema):
    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value is not None  # Empty lists must be kept!
        }


class ConfigurationListResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    category = fields.String(required=False, allow_none=True)
    value = fields.String(required=True)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    internal = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    editor = fields.String(required=False, allow_none=True, missing='TEXT', default='TEXT',
                           validate=[OneOf(list(EditorType.__dict__.keys()))])

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Configuration"""
        return Configuration(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class ConfigurationItemResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    category = fields.String(required=False, allow_none=True)
    value = fields.String(required=True)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    internal = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    editor = fields.String(required=False, allow_none=True, missing='TEXT', default='TEXT',
                           validate=[OneOf(list(EditorType.__dict__.keys()))])

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Configuration"""
        return Configuration(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class ConfigurationCreateRequestSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    category = fields.String(required=False, allow_none=True)
    value = fields.String(required=True)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    internal = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    editor = fields.String(required=False, allow_none=True, missing='TEXT', default='TEXT',
                           validate=[OneOf(list(EditorType.__dict__.keys()))])

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Configuration"""
        return Configuration(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class NotificationListResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    created = fields.DateTime(
        required=False,
        allow_none=True,
        missing=datetime.datetime.utcnow,
        default=datetime.datetime.utcnow)
    text = fields.String(required=True)
    link = fields.String(required=False, allow_none=True)
    status = fields.String(required=False, allow_none=True, missing="UNREAD", default="UNREAD",
                           validate=[OneOf(list(NotificationStatus.__dict__.keys()))])
    from_system = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    type = fields.String(required=False, allow_none=True, missing="INFO", default="INFO",
                         validate=[OneOf(list(NotificationType.__dict__.keys()))])

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Notification"""
        return Notification(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class NotificationItemResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    created = fields.DateTime(
        required=False,
        allow_none=True,
        missing=datetime.datetime.utcnow,
        default=datetime.datetime.utcnow)
    text = fields.String(required=True)
    link = fields.String(required=False, allow_none=True)
    status = fields.String(required=False, allow_none=True, missing="UNREAD", default="UNREAD",
                           validate=[OneOf(list(NotificationStatus.__dict__.keys()))])
    from_system = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    type = fields.String(required=False, allow_none=True, missing="INFO", default="INFO",
                         validate=[OneOf(list(NotificationType.__dict__.keys()))])

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Notification"""
        return Notification(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class NotificationCreateRequestSchema(BaseSchema):
    """ JSON serialization schema """
    text = fields.String(required=True)
    link = fields.String(required=False, allow_none=True)
    status = fields.String(required=False, allow_none=True, missing="UNREAD", default="UNREAD",
                           validate=[OneOf(list(NotificationStatus.__dict__.keys()))])
    from_system = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    type = fields.String(required=False, allow_none=True, missing="INFO", default="INFO",
                         validate=[OneOf(list(NotificationType.__dict__.keys()))])
    user_id = fields.Integer(allow_none=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Notification"""
        return Notification(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class PermissionListResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    applicable_to = fields.String(required=False, allow_none=True,
                                  validate=[OneOf(list(AssetType.__dict__.keys()))])

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Permission"""
        return Permission(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class PermissionItemResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    applicable_to = fields.String(required=False, allow_none=True,
                                  validate=[OneOf(list(AssetType.__dict__.keys()))])
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Permission"""
        return Permission(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class RoleListResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    label = fields.String(required=True)
    description = fields.String(required=True)
    all_user = fields.Boolean(
        required=False,
        allow_none=True,
        missing=False,
        default=False)
    system = fields.Boolean(
        required=False,
        allow_none=True,
        missing=False,
        default=False)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    users = fields.Nested(
        'thorn.schema.UserListResponseSchema',
        allow_none=True,
        many=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Role"""
        return Role(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class RoleItemResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    label = fields.String(required=True)
    description = fields.String(required=True)
    all_user = fields.Boolean(
        required=False,
        allow_none=True,
        missing=False,
        default=False)
    system = fields.Boolean(
        required=False,
        allow_none=True,
        missing=False,
        default=False)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    permissions = fields.Nested(
        'thorn.schema.PermissionItemResponseSchema',
        required=True,
        many=True)
    users = fields.Nested(
        'thorn.schema.UserItemResponseSchema',
        allow_none=True,
        many=True,
        only=['id', 'first_name', 'last_name', 'email', 'login'])

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Role"""
        return Role(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class RoleCreateRequestSchema(BaseSchema):
    """ JSON serialization schema """
    name = fields.String(required=True)
    label = fields.String(required=True)
    description = fields.String(required=True)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    users = fields.Nested(
        'thorn.schema.UserCreateRequestSchema',
        allow_none=True,
        many=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Role"""
        return Role(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserListResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    login = fields.String(required=True)
    email = fields.String(required=True)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    status = fields.String(required=False, allow_none=True, missing='ENABLED', default='ENABLED',
                           validate=[OneOf(list(UserStatus.__dict__.keys()))])
    authentication_type = fields.String(required=False, allow_none=True, missing='INTERNAL', default='INTERNAL',
                                        validate=[OneOf(list(AuthenticationType.__dict__.keys()))])
    created_at = fields.DateTime(
        required=False,
        allow_none=True,
        missing=datetime.datetime.utcnow,
        default=datetime.datetime.utcnow)
    updated_at = fields.DateTime(
        required=False,
        allow_none=True,
        missing=datetime.datetime.utcnow,
        default=datetime.datetime.utcnow)
    first_name = fields.String(required=False, allow_none=True)
    last_name = fields.String(required=False, allow_none=True)
    locale = fields.String(
        required=False,
        allow_none=True,
        missing='pt',
        default='pt')
    confirmed_at = fields.DateTime(required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True)
    roles = fields.Nested(
        'thorn.schema.RoleListResponseSchema',
        allow_none=True,
        many=True)
    workspace = fields.Nested(
        'thorn.schema.WorkspaceListResponseSchema',
        allow_none=True)
    full_name = fields.Function(
        lambda x: "{} {}".format(
            x.first_name,
            x.last_name).strip())

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of User"""
        return User(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserItemResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    login = fields.String(required=True)
    email = fields.String(required=True)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    status = fields.String(required=False, allow_none=True, missing='ENABLED', default='ENABLED',
                           validate=[OneOf(list(UserStatus.__dict__.keys()))])
    authentication_type = fields.String(required=False, allow_none=True, missing='INTERNAL', default='INTERNAL',
                                        validate=[OneOf(list(AuthenticationType.__dict__.keys()))])
    first_name = fields.String(required=False, allow_none=True)
    last_name = fields.String(required=False, allow_none=True)
    locale = fields.String(
        required=False,
        allow_none=True,
        missing='pt',
        default='pt')
    api_token = fields.String(required=False, allow_none=True)
    roles = fields.Nested(
        'thorn.schema.RoleItemResponseSchema',
        allow_none=True,
        many=True)
    workspace = fields.Nested(
        'thorn.schema.WorkspaceItemResponseSchema',
        allow_none=True)
    name = fields.Function(lambda x: "{} {}".format(x.first_name, x.last_name))

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of User"""
        return User(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserCreateRequestSchema(BaseSchema):
    """ JSON serialization schema """
    login = fields.String(required=True)
    email = fields.String(required=True)
    enabled = fields.Boolean(
        required=False,
        allow_none=True,
        missing=True,
        default=True)
    status = fields.String(required=False, allow_none=True, missing='ENABLED', default='ENABLED',
                           validate=[OneOf(list(UserStatus.__dict__.keys()))])
    authentication_type = fields.String(required=False, allow_none=True, missing='INTERNAL', default='INTERNAL',
                                        validate=[OneOf(list(AuthenticationType.__dict__.keys()))])
    encrypted_password = fields.String(required=True)
    remember_created_at = fields.DateTime(required=False, allow_none=True)
    first_name = fields.String(required=False, allow_none=True)
    last_name = fields.String(required=False, allow_none=True)
    locale = fields.String(
        required=False,
        allow_none=True,
        missing='pt',
        default='pt')
    confirmed_at = fields.DateTime(required=False, allow_none=True)
    confirmation_sent_at = fields.DateTime(required=False, allow_none=True)
    unconfirmed_email = fields.String(required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True)
    roles = fields.Nested(
        'thorn.schema.RoleCreateRequestSchema',
        allow_none=True,
        many=True,
        only=['name'])
    workspace = fields.Nested(
        'thorn.schema.WorkspaceCreateRequestSchema',
        allow_none=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of User"""
        return User(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class WorkspaceListResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    owner = fields.Nested(
        'thorn.schema.UserListResponseSchema',
        required=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Workspace"""
        return Workspace(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class WorkspaceItemResponseSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    owner = fields.Nested(
        'thorn.schema.UserItemResponseSchema',
        required=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Workspace"""
        return Workspace(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class WorkspaceCreateRequestSchema(BaseSchema):
    """ JSON serialization schema """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    owner = fields.Nested(
        'thorn.schema.UserCreateRequestSchema',
        required=True)

    # noinspection PyUnresolvedReferences
    @post_load
    def make_object(self, data, **kwargs):
        """ Deserialize data into an instance of Workspace"""
        return Workspace(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE

