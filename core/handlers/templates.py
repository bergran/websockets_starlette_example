# -*- coding: utf-8 -*-
import jinja2


def setup_jinja2(template_dir):
    @jinja2.contextfunction
    def url_for(context, name, **path_params):
        request = context['request']
        return request.url_for(name, **path_params)

    loader = jinja2.FileSystemLoader(template_dir)
    env = jinja2.Environment(loader=loader, autoescape=True)
    env.globals['url_for'] = url_for
    return env


env = setup_jinja2('templates')
