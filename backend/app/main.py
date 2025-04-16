
from app.cli import init_cli
from app.infrastructure.container import Container
from app.presentation.controllers.authentication_controller import auth_blueprint
from app.presentation.controllers.category_association_controller import category_association_blueprint
from app.presentation.controllers.category_controller import category_blueprint
from app.presentation.controllers.product_controller import product_blueprint
from app.presentation.controllers.buildup_controller import buildup_blueprint
from app.presentation.controllers.role_controller import role_blueprint
from app.presentation.controllers.user_controller import user_blueprint
from app.presentation.controllers.user_roles_controller import user_roles_blueprint
from app.presentation.controllers.filter_element_controller import filter_element_blueprint
from app.presentation.controllers.filter_mapping_controller import filter_mapping_blueprint
from flask import Flask, request
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    container = Container()
    app.container = container

    # Swagger UI configuration
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config['SWAGGER_UI_JSONEDITOR'] = True
    app.config['RESTX_VALIDATE'] = True
    app.config['RESTX_SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.config['RESTX_ERROR_404_HELP'] = False
    app.config['SERVER_NAME'] = None  # Add this line

    init_cli(app)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(buildup_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(role_blueprint)
    app.register_blueprint(user_roles_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(category_association_blueprint)
    app.register_blueprint(filter_element_blueprint)
    app.register_blueprint(filter_mapping_blueprint)
    CORS(app) # enable CORS
    # Print all registered routes (fixed format)
    print("\n=== All Flask Routes ===")
    for rule in app.url_map.iter_rules():
        methods = ', '.join(sorted(rule.methods))  # Convert set to string
        print(f"Endpoint: {rule.endpoint:<30} Methods: {methods:<20} URL: {rule.rule}")

    return app


