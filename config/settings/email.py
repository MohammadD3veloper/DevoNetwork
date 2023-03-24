from config.env import env

# Email configurations
FROM_EMAIL_ADDRESS = env('FROM_EMAIL_ADDRESS')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = env("EMAIL_HOST")

EMAIL_PORT = env("EMAIL_PORT")

EMAIL_HOST_USER = env("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = env("EMAIL_USE_TLS")
