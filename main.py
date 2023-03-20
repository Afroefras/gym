from os import getenv

cred = {
    "type": "service_account",
    "project_id": "gymworkout",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    
    "private_key_id": getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": getenv("GOOGLE_CLIENT_ID"),
    "client_x509_cert_url": getenv("GOOGLE_CLIENT_X509_CERT_URL"),
}