from interrogatio.core.exceptions import AlreadyRegisteredError
from interrogatio.handlers.base import QHandler


class QHandlersRegistry(dict):
    def register(self, alias, clazz):
        if alias in self:
            raise AlreadyRegisteredError(f'alias `{alias}` already exists.')
        self[alias] = clazz

    def get_registered(self):
        return list(self.keys())

    def get_instance(self, question):
        qtype = question['type']
        clazz = self[qtype]
        return clazz(question)


_registry = QHandlersRegistry()


def get_registry():
    return _registry


def get_instance(question):
    """
    Returns an instance of a concrete subclass of QHandler initialized with
    a question. The subclass of QHandler is identified by the ``type`` field
    of the question.

    :param question: a question to handle.
    :type question: dict

    :return: an instance of the corresponding QHandler
    :rtype: QHandler subclass
    """
    return get_registry().get_instance(question)


def get_registered():
    """
    Returns a list of registered QHandlers.

    :return: list of aliases of the registered QHandlers.
    :rtype: list
    """
    return get_registry().get_registered()


def register(name):
    if name in get_registry().get_registered():
        raise AlreadyRegisteredError(
            f'The handler `{name}` is already registered.',
        )

    def _wrapper(cls):
        if not issubclass(cls, QHandler):
            raise ValueError(
                'The provided class must be a subclass of QHandler.',
            )

        get_registry().register(name, cls)

        return cls
    return _wrapper
