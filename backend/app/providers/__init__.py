"""
Provider implementations for threat intelligence APIs
"""
from app.providers.ninja import NinjaProvider
from app.providers.malwarebytes import MalwarebytesProvider
from app.providers.factory import ProviderFactory, ProviderType

# Register providers with the factory
ProviderFactory.register(ProviderType.NINJA.value, NinjaProvider)
ProviderFactory.register(ProviderType.MALWAREBYTES.value, MalwarebytesProvider)
