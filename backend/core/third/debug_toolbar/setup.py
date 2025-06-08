class DebugToolbarSetup:
    """
    We used a class, just for name-spacing convenience.
    """

    @staticmethod
    def do_settings(INSTALLED_APPS, MIDDLEWARE, middleware_position=None):
        INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar"]

        # In order to deal with that:
        # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-middleware
        # The order of MIDDLEWARE is important.
        # You should include the Debug Toolbar middleware as early as possible in the list.
        # However, it must come after any other middleware that encodes the response’s content, such as GZipMiddleware.
        # We support inserting the middleware at an arbitrary position in the list.
        # If position is not specified, we will just include it at the end of the list.

        debug_toolbar_middleware = "debug_toolbar.middleware.DebugToolbarMiddleware"

        if middleware_position is None:
            MIDDLEWARE = MIDDLEWARE + [debug_toolbar_middleware]
        else:
            MIDDLEWARE.insert(middleware_position, debug_toolbar_middleware)

        return INSTALLED_APPS, MIDDLEWARE
