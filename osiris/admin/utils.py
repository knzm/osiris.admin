# -*- coding: utf-8 -*-

__all__ = [
    "get_model_config",
    "guess_dbsession",
    "get_current_dbsession",
    ]


def get_model_config(request, name):
    from osiris.admin.interface import IModelConfig
    return request.registry.getUtility(IModelConfig, name=name)


def guess_dbsession(config):
    try:
        models = config.maybe_dotted('%s.models' % config.package_name)
    except ValueError:
        return None
    else:
        # alchemy
        session = getattr(models, "DBSession", None)
        if not session:
            # Akhet
            session = getattr(models, "Session", None)
        return session


def get_current_dbsession():
    import pyramid.threadlocal
    request = pyramid.threadlocal.get_current_request()
    return getattr(request, 'session_factory')
