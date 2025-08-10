"""
Global configuration to suppress unnecessary warnings and errors
Import this at the beginning of any script to clean up output
"""
import warnings
import os

# Suppress urllib3 OpenSSL warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')
warnings.filterwarnings('ignore', message='NotOpenSSLWarning')

# Disable LangSmith tracing to avoid authentication errors
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ['LANGSMITH_API_KEY'] = 'dummy'  # Prevents missing key warning

# Additional common warnings to suppress
warnings.filterwarnings('ignore', message='LangSmithMissingAPIKeyWarning')
warnings.filterwarnings('ignore', message='Failed to multipart ingest runs')
warnings.filterwarnings('ignore', message='Failed to send compressed multipart ingest')