import os

JAZZMIN_SETTINGS = {
    #"site_logo": "images/logo.png",   Caminho para a logo
    "site_brand": "Admin Civilizar",  # Nome que aparece no painel
    "custom_css": "/static/custom.css",

    "icons": {
        # auth
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        # permissions
        "permissions.Module": "fas fa-cubes",  # Ícone para Módulos
        "permissions.Policy": "fas fa-shield-alt",  # Ícone para Policies
        "permissions.Access": "fas fa-user-lock",  # Ícone para Acesso
        "permissions.UserModuleAccess": "fas fa-user-cog",  # Ícone para relacionamento usuário/módulo
        
        # tests
        "tests.Test": "fas fa-vial",  # Ícone para Test
        "tests.Category": "fas fa-list-alt",  # Ícone para Category
        "tests.Question": "fas fa-question-circle",  # Ícone para Question
        "tests.Keyword": "fas fa-key",  # Ícone para Keyword

        # secretariats
        "secretariats.Secretariat": "fas fa-building",  # Ícone para Secretariat

        # schools
        "schools.School": "fas fa-school",  # Ícone para School
        "schools.SchoolTest": "fas fa-flask",  # Ícone para SchoolTest
        "schools.Class": "fas fa-chalkboard-teacher",  # Ícone para Class
        "schools.Student": "fas fa-user-graduate",  # Ícone para Student
        "schools.TestExecuted": "fas fa-clipboard-check",  # Ícone para TestExecuted
    },
}