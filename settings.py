settings = dict(
    
)

try:
    # pull in settings_local if it exists
    from settings_local import settings as s
    settings.update(s)
except ImportError:
    pass
