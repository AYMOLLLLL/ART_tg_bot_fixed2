from handlers.start import router as start_router
from handlers.application_form import router as application_router
from handlers.admin_handlers import router as admin_router

routers = [start_router, application_router, admin_router]