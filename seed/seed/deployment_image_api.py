# -*- coding: utf-8 -*-}
import math
import logging

from seed.app_auth import requires_auth, requires_permission
from flask import request, current_app, g as flask_globals
from flask_restful import Resource
from sqlalchemy import or_
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from seed.schema import *
from seed.util import translate_validation
from flask_babel import gettext

log = logging.getLogger(__name__)


class DeploymentImageListApi(Resource):
    """ REST API for listing class DeploymentImage """

    def __init__(self):
        self.human_name = gettext('DeploymentImage')

    @requires_auth
    def get(self):
        if request.args.get('fields'):
            only = [f.strip() for f in request.args.get('fields').split(',')]
        else:
            only = ('id', ) if request.args.get(
                'simple', 'false') == 'true' else None
        enabled_filter = request.args.get('enabled')
        if enabled_filter:
            deployment_images = DeploymentImage.query.filter(
                DeploymentImage.enabled == (enabled_filter != 'false'))
        else:
            deployment_images = DeploymentImage.query
        q_filter = request.args.get('q')
        if q_filter:
            find_pattern = '%%{}%%'.format(q_filter.replace(" ", "%"))
            deployment_images = deployment_images.filter(or_(
                    DeploymentImage.name.like(find_pattern),
                    DeploymentImage.user_name.like(find_pattern)))

        page = request.args.get('page') or '1'
        if page is not None and page.isdigit():
            page_size = int(request.args.get('size', 20))
            page = int(page)
            pagination = deployment_images.paginate(page, page_size, True)
            result = {
                'data': DeploymentImageListResponseSchema(
                    many=True, only=only).dump(pagination.items),
                'pagination': {
                    'page': page, 'size': page_size,
                    'total': pagination.total,
                    'pages': int(math.ceil(1.0 * pagination.total / page_size))}
            }
        else:
            result = {
                'data': DeploymentImageListResponseSchema(
                    many=True, only=only).dump(
                    deployment_images)}

        if log.isEnabledFor(logging.DEBUG):
            log.debug(gettext('Listing %(name)s', name=self.human_name))
        return result

    @requires_auth
    def post(self):
        result = {'status': 'ERROR',
                  'message': gettext("Missing json in the request body")}
        return_code = HTTPStatus.BAD_REQUEST
        
        if request.json is not None:
            try:
                request_schema = DeploymentImageCreateRequestSchema()
                response_schema = DeploymentImageItemResponseSchema()
                deployment_image = request_schema.load(request.json)
                if log.isEnabledFor(logging.DEBUG):
                    log.debug(gettext('Adding %s'), self.human_name)
                deployment_image = deployment_image
                db.session.add(deployment_image)
                db.session.commit()
                result = response_schema.dump(deployment_image)
                return_code = HTTPStatus.CREATED
            except ValidationError as e:
                result= {
                   'status': 'ERROR', 
                   'message': gettext('Invalid data for %(name)s.)',
                                      name=self.human_name),
                   'errors': translate_validation(e.messages)
                }
            except Exception as e:
                result = {'status': 'ERROR',
                          'message': gettext("Internal error")}
                return_code = 500
                if current_app.debug:
                    result['debug_detail'] = str(e)

                log.exception(e)
                db.session.rollback()

        return result, return_code


class DeploymentImageDetailApi(Resource):
    """ REST API for a single instance of class DeploymentImage """
    def __init__(self):
        self.human_name = gettext('DeploymentImage')

    @requires_auth
    def get(self, deployment_image_id):

        if log.isEnabledFor(logging.DEBUG):
            log.debug(gettext('Retrieving %s (id=%s)'), self.human_name,
                      deployment_image_id)

        deployment_image = DeploymentImage.query.get(deployment_image_id)
        return_code = HTTPStatus.OK
        if deployment_image is not None:
            result = {
                'status': 'OK',
                'data': [DeploymentImageItemResponseSchema().dump(
                    deployment_image)]
            }
        else:
            return_code = HTTPStatus.NOT_FOUND
            result = {
                'status': 'ERROR',
                'message': gettext(
                    '%(name)s not found (id=%(id)s)',
                    name=self.human_name, id=deployment_image_id)
            }

        return result, return_code

    @requires_auth
    def delete(self, deployment_image_id):
        return_code = HTTPStatus.NO_CONTENT
        if log.isEnabledFor(logging.DEBUG):
            log.debug(gettext('Deleting %s (id=%s)'), self.human_name,
                      deployment_image_id)
        deployment_image = DeploymentImage.query.get(deployment_image_id)
        if deployment_image is not None:
            try:
                db.session.delete(deployment_image)
                db.session.commit()
                result = {
                    'status': 'OK',
                    'message': gettext('%(name)s deleted with success!',
                                       name=self.human_name)
                }
            except Exception as e:
                result = {'status': 'ERROR',
                          'message': gettext("Internal error")}
                return_code = HTTPStatus.INTERNAL_SERVER_ERROR
                if current_app.debug:
                    result['debug_detail'] = str(e)
                db.session.rollback()
        else:
            return_code = HTTPStatus.NOT_FOUND
            result = {
                'status': 'ERROR',
                'message': gettext('%(name)s not found (id=%(id)s).',
                                   name=self.human_name, id=deployment_image_id)
            }
        return result, return_code

    @requires_auth
    def patch(self, deployment_image_id):
        result = {'status': 'ERROR', 'message': gettext('Insufficient data.')}
        return_code = HTTPStatus.NOT_FOUND

        if log.isEnabledFor(logging.DEBUG):
            log.debug(gettext('Updating %s (id=%s)'), self.human_name,
                      deployment_image_id)
        if request.json:
            request_schema = partial_schema_factory(
                DeploymentImageCreateRequestSchema)
            # Ignore missing fields to allow partial updates
            deployment_image = request_schema.load(request.json, partial=True)
            response_schema = DeploymentImageItemResponseSchema()
            try:
                deployment_image.id = deployment_image_id
                deployment_image = db.session.merge(deployment_image)
                db.session.commit()

                if deployment_image is not None:
                    return_code = HTTPStatus.OK
                    result = {
                        'status': 'OK',
                        'message': gettext(
                            '%(n)s (id=%(id)s) was updated with success!',
                            n=self.human_name,
                            id=deployment_image_id),
                        'data': [response_schema.dump(
                            deployment_image)]
                    }
            except ValidationError as e:
                result= {
                   'status': 'ERROR', 
                   'message': gettext('Invalid data for %(name)s (id=%(id)s)',
                                      name=self.human_name,
                                      id=deployment_image_id),
                   'errors': translate_validation(e.messages)
                }
            except Exception as e:
                result = {'status': 'ERROR',
                          'message': gettext("Internal error")}
                return_code = 500
                if current_app.debug:
                    result['debug_detail'] = str(e)
                db.session.rollback()
        return result, return_code
