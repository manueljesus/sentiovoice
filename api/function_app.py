import azure.functions as func
from src.api import api

app_func = func.AsgiFunctionApp(app=api, http_auth_level=func.AuthLevel.ANONYMOUS)
