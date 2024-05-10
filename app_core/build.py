from fastapi import FastAPI, responses
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError, IntegrityError

from api.v1.router import user
from config.setting import AuthSettings
 
from app_core  import setup as db_setup 
from errors.exceptions import AuthException
from handler import exceptions as exec

settings = AuthSettings()


class AppBuilder:
    def __init__(self):
        self._app = FastAPI(
            title=settings.API_TITLE, description=settings.APP_DESCRIPTION
        )

    def register_routes(self):
        self._app.include_router(
            user.user_router,
            prefix=settings.API_PREFIX,
            tags=["User"],
        )
        
        @self._app.get("/", include_in_schema=False)
        def _index():
            return responses.RedirectResponse("/docs")

    def register_exceptions(self):
        self._app.add_exception_handler(
            RequestValidationError, exec.validation_error_handler
        )
        self._app.add_exception_handler(ValidationError, exec.validation_error_handler)
        self._app.add_exception_handler(ValueError, exec.validation_for_all_exceptions)
        self._app.add_exception_handler(
            HTTPException, exec.validation_http_exceptions  # type: ignore
        )
        self._app.add_exception_handler(
            AuthException, exec.validation_exception_handler  # type: ignore
        )
        self._app.add_exception_handler(DBAPIError, exec.db_error_handler)
        self._app.add_exception_handler(IntegrityError, exec.db_error_handler)

    def register_middlewares(self):
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # def register_database(self) -> None:
    #     """Register all databases"""
    #     db_setup.Base.metadata.create_all(
    #         bind=db_setup.database.get_engine  # type : ignore
    #     )

    def register_database(self):
        """Register the database"""

        db_setup.Base.metadata.create_all(bind=db_setup.database.get_engine())


    def get_app(self):
        self.register_routes()
        self.register_middlewares()
        self.register_exceptions()
        self.register_database()
        return self._app
