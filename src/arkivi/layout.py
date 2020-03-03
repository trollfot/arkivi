import wrapt
from pathlib import Path
from chameleon import PageTemplateLoader
from horseman.response import reply


TEMPLATES = PageTemplateLoader(
    str((Path(__file__).parent / 'templates').resolve()), ".pt")


class Layout:

    def __init__(self, name, **namespace):
        self._template = TEMPLATES[name]
        self._namespace = namespace

    def render(self, content, **extra):
        ns = {**self._namespace, **extra}
        return self._template.render(content=content, **ns)


menu = (
    ("Spectacles", "/spectacles"),
    ("Tournée", "/tour"),
    ("L'équipe", "/equipe"),
    ("Contact", "/contact")
)


layout = Layout('layout.pt', menu=menu)


def template_endpoint(template_name: str, layout=layout):
    template = TEMPLATES[template_name]

    @wrapt.decorator
    def render(endpoint, instance, args, kwargs):
        try:
            local_namespace = endpoint(*args, **kwargs)
        except KeyError:
            return reply(404)

        request = args[0]
        content = template.render(**local_namespace)
        if layout is not None:
            body = layout.render(
                content, path=request.environ['PATH_INFO'])
            return reply(
                body=body,
                headers={'Content-Type': 'text/html; charset=utf-8'})
        return reply(
            body=content,
            headers={'Content-Type': 'text/html; charset=utf-8'})

    return render
