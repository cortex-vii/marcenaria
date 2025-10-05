import os

# Configuração do Django Unfold
UNFOLD = {
    "SITE_TITLE": "Teste",
    "SITE_HEADER": "Administrativo",
    "SITE_URL": "/",
    "SITE_ICON": {
        "name": "dashboard",
        "color": "#3B82F6",
    },
    "SITE_SYMBOL": "dashboard",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "development",
    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254", 
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Dashboard",
                "separator": True,
                "items": [
                    {
                        "title": "Home",
                        "icon": "home",
                        "link": "/admin/",
                    },
                ],
            },
            {
                "title": "Orçamentos",
                "separator": True,
                "items": [
                    {
                        "title": "Orçamentos",
                        "icon": "description",
                        "link": "/admin/marcenaria/orcamento/",
                    },
                    {
                        "title": "Ambientes",
                        "icon": "room",
                        "link": "/admin/marcenaria/ambiente/",
                    },

                ],
            },
            {
                "title": "Cadastros",
                "separator": True,
                "items": [
                    {
                        "title": "Componentes",
                        "icon": "widgets",
                        "link": "/admin/marcenaria/componente/",
                    },
                    {
                        "title": "Tipos de Componentes",
                        "icon": "construction",
                        "link": "/admin/marcenaria/tipocomponente/",
                    },
                    {
                        "title": "Tipos de Peças",
                        "icon": "category",
                        "link": "/admin/marcenaria/tipopeca/",
                    },
                    {
                        "title": "Fornecedores",
                        "icon": "business",
                        "link": "/admin/marcenaria/fornecedor/",
                    },
                ],
            },
            {
                "title": "User Management",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": "/admin/auth/user/",
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": "/admin/auth/group/",
                    },
                ],
            },
        ],
    },
}