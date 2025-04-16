from datetime import datetime

from app.config import Config
from app.core.application.dtos.product.product_dto import (Product_DTO,
                                                           ProductHeader_DTO)
from app.core.application.services.iepdx_service import IEpdxService
from app.core.application.services.iokobau_service import IOkobauService
from app.core.application.services.iproduct_service import IProductService
from app.core.application.services.iuser_service import IUserService
from app.infrastructure.container import Container
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request
from flask_restx import Api, Namespace, Resource, fields, marshal

from app.core.application.dtos.epdx.epdx_dto import EPD

product_blueprint = Blueprint('product', __name__)
api = Api(
    product_blueprint,
    version='1.0',
    title='Product API',
    description='API for managing EPD products',
    doc='/docs/products',
    default_endpoint=None,
    prefix='/products'
)


product_ns = Namespace('products', description='Product operations', path='/')
api.add_namespace(product_ns)

# Custom DateTime field to handle your format
class CustomDateTime(fields.Raw):
    def format(self, value):
        if value:
            if isinstance(value, str):
                return value
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return None

# API Models
product_input_model = product_ns.model('ProductInput', {
    'status': fields.String(required=True, description='Product status'),
    'user_created': fields.String(description='User who created the product'),
    'user_updated': fields.String(description='User who last updated the product'),
    'epd_name': fields.String(required=True, description='EPD name'),
    'epd_declaredUnit': fields.String(description='EPD declared unit'),
    'epd_version': fields.String(description='EPD version'),
    'epd_publishedDate': fields.String(description='EPD publication date'),
    'epd_validUntil': fields.String(description='EPD validity date'),
    'epd_standard': fields.String(description='EPD standard'),
    'epd_comment': fields.String(description='EPD comment'),
    'epd_location': fields.String(description='EPD location'),
    'epd_formatVersion': fields.String(description='EPD format version'),
    'epd_id': fields.String(description='EPD ID'),
    'epdx': fields.Raw(description='EPD extended data'),
    'epd_sourceName': fields.String(description='EPD source name'),
    'epd_sourceUrl': fields.String(description='EPD source URL'),
    'epd_linear_density': fields.Float(description='EPD linear density'),
    'epd_gross_density': fields.Float(description='EPD gross density'),
    'epd_grammage': fields.Float(description='EPD grammage'),
    'epd_layer_thickness': fields.Float(description='EPD layer thickness'),
    'epd_subtype': fields.String(description='EPD subtype'),
    'epd_bulk_density': fields.Float(description='EPD bulk density')
})

product_output_model = product_ns.inherit('Product', product_input_model, {
    'id': fields.Integer(readonly=True, description='Product identifier'),
    'date_created': CustomDateTime(readonly=True, description='Creation date'),
    'date_updated': CustomDateTime(readonly=True, description='Last update date'),
})


@product_ns.route('/')
class ProductList(Resource):
    @inject
    @product_ns.doc('list_products')
    @product_ns.marshal_list_with(product_output_model)
    def get(self, product_service: IProductService = Provide[Container.product_service]):
        """List all products"""
        products = product_service.get_all_products()
        return [product_dto for product_dto in products]

    @inject
    @product_ns.doc('create_product')
    @product_ns.expect(product_input_model)
    @product_ns.marshal_with(product_output_model, code=201)
    def post(self, product_service: IProductService = Provide[Container.product_service]):
        """Create a new product"""
        data : dict = product_ns.payload
        keys_to_ignore_list = ['date_created', 'date_updated']
        ignored_values_list = [data.pop(key, f"key {key} not present") for key in keys_to_ignore_list ]
        product = ProductHeader_DTO(**(data))
        
        product.date_created = datetime.utcnow()
        product.status = 'active'
        
        created_product : ProductHeader_DTO = product_service.create_product(product)
        return created_product.model_dump(), 201

@product_ns.route('/<int:id>')
@product_ns.param('id', 'The product identifier')
class ProductItem(Resource):
    @inject
    @product_ns.doc('get_product')
    @product_ns.marshal_with(product_output_model)
    def get(self, id: int, product_service: IProductService = Provide[Container.product_service]):
        """Get a product by ID"""
        product : Product_DTO = product_service.get_product_by_id(id)
        if not product:
            product_ns.abort(404, "Product not found")
        return product.model_dump()

    @inject
    @product_ns.doc('update_product')
    @product_ns.expect(product_input_model)
    @product_ns.marshal_with(product_output_model)
    def put(self, id: int, product_service: IProductService = Provide[Container.product_service]):
        """Update a product"""
        data = product_ns.payload
        keys_to_ignore_list = ['date_created', 'date_updated']
        ignored_values_list = [data.pop(key, f"key {key} not present") for key in keys_to_ignore_list ]
        product = ProductHeader_DTO(**(data))
        
        product.date_updated = datetime.utcnow()
        
        updated_product : ProductHeader_DTO = product_service.update_product(id, product)
        if not updated_product:
            product_ns.abort(404, "Product not found")
        return updated_product.model_dump()

    @inject
    @product_ns.doc('delete_product')
    @product_ns.response(204, 'Product deleted')
    def delete(self, id: int, product_service: IProductService = Provide[Container.product_service]):
        """Delete a product"""
        result = product_service.delete_product(id)
        if not result:
            product_ns.abort(404, "Product not found")
        return '', 204


@product_ns.route('/uri/<uri>')
@product_ns.param('uri', 'Unique index, composed as <epd_sourceName>.<epd_id>')
class ProductItem(Resource):
    @inject
    @product_ns.doc('get_product_by_uri')
    @product_ns.marshal_with(product_output_model)
    def get(self, uri: str, product_service: IProductService = Provide[Container.product_service]):
        """Get a product by source and source id"""
        product : Product_DTO = product_service.get_product_by_uri(uri)
        if not product:
            product_ns.abort(404, "Product not found")
        return product.model_dump()


@product_ns.route('/epd/')
class ProductItem(Resource):
    @inject
    @product_ns.doc('product_from_epd')
    @product_ns.expect(product_ns.model('EPD', {
        # EPD model schema here for documentation
        # This is just a placeholder
        'id': fields.String(description='EPD ID'),
        'name': fields.String(description='EPD Name'),
        # Add other fields if needed
    }))
    @product_ns.marshal_with(product_output_model)
    def post(self, epdx_service: IEpdxService = Provide[Container.epdx_service]):
        """Creates a product from the provided epd object"""
        epd_data = request.json
        product : Product_DTO = epdx_service.from_epdx_to_product(EPD(**epd_data))
        if not product:
            product_ns.abort(404, "Could not generate product")
        return product.model_dump()


external_db_ns = Namespace('external-databases', description='External Product Database operations', path='/external')
api.add_namespace(external_db_ns)
# this should have a different route path, not okobau, maybe seed-products and we add different data resources under this function
# to enable a seeding to the admin user of app
# if we put okobau on route, then we should create another controller for okobau
# and we never expose entities in controllers u should use mapper again to map from entity to dto
# we should change response of each controller method here to dtos!
@external_db_ns.route('/okobau/<string:uuid>')
@product_ns.param('uuid', 'The unique product identifier in the external database')
class OkobauProduct(Resource):
    @inject
    @external_db_ns.doc("okobau_product_from_id")
    @external_db_ns.response(201, 'Product created successfully', product_output_model)
    @external_db_ns.response(409, 'Product already exists')
    def post(
        self, uuid : str,     
        okobau_service: IOkobauService = Provide[Container.okobau_service],
        epdx_service: IEpdxService = Provide[Container.epdx_service],
        product_service: IProductService = Provide[Container.product_service],
        user_service: IUserService = Provide[Container.user_service]
    ):
        """creates a product from okobaudat id """
        admin_id = user_service.get_user_by_email(Config.ADMIN_CONFIG.get_admin_user_credentials()[0]).id   # change this when permission logic is added
        product_dto = epdx_service.from_epdx_to_product(okobau_service.get_epdx_from_uuid(uuid))
        result : ProductHeader_DTO = product_service.create_product_from_dto(product_dto, user_id = admin_id)
        if isinstance(result, str):
            return {"message": result}, 409
        return marshal(result.model_dump(), product_output_model), 201

    @inject
    @external_db_ns.doc("get_okobau_data_from_id")
    @external_db_ns.response(404, 'uuid not found')
    def get(
        self, uuid : str,     
        okobau_service: IOkobauService = Provide[Container.okobau_service]
    ):
        """gets a product from okobaudat db using uuid """
        product = okobau_service.get_ilcd_from_uuid(uuid)
        if not product:
            external_db_ns.abort(404, "Product not found")
        return product




