"""
URL configuration for eeet2582_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from eeet2582_backend.api.views.parse_docx import ParseDocxAPIView
from .api.views import google_login, payment, webhook

schema_view = get_schema_view(
   openapi.Info(
      title="Group 1 ReadProof API",
      default_version='v1',
      description="UI",
   ),
   public=True,
   permission_classes=([permissions.AllowAny]),
)

urlpatterns = [

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("login/google", google_login.GoogleSignIn.as_view()),
    path("payment/create-checkout-session",  payment.StripeCheckoutView.as_view()),
    path('payment/webhook', webhook.stripe_webhook, name='stripe_webhook'),
    path('api/parse-docx', ParseDocxAPIView.as_view()),
]
