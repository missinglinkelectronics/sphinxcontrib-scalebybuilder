# -*- coding: utf-8 -*-
"""
    sphinxcontrib.condimgscale
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Scale images and figures differently depending on the builder.

    :copyright: Copyright 2018 by Stefan Wiehler
                <stefan.wiehler@missinglinkelectronics.com>.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import images

from sphinx.transforms import SphinxTransform
from sphinx.util import logging

if False:
    # For type annotation
    from typing import Any, Dict  # NOQA
    from sphinx.application import Sphinx  # NOQA

logger = logging.getLogger(__name__)

builders = {}


class ConditionallyScaledImage(images.Image):
    option_spec = images.Image.option_spec.copy()


class ConditionallyScaledFigure(images.Figure):
    option_spec = images.Figure.option_spec.copy()


class ConditionalImageScaler(SphinxTransform):
    default_priority = 410

    def apply(self):
        # type: () -> None
        for node in self.document.traverse(nodes.image):
            builder_name = self.app.builder.name
            if 'scale-' + builder_name in node:
                node['scale'] = node['scale-' + builder_name]


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    for builder_name in app.registry.builders.keys():
        ConditionallyScaledImage.option_spec['scale-' + builder_name] = directives.percentage
        ConditionallyScaledFigure.option_spec['scale-' + builder_name] = directives.percentage
    directives.register_directive('image', ConditionallyScaledImage)
    directives.register_directive('figure', ConditionallyScaledFigure)
    app.add_post_transform(ConditionalImageScaler)
    return {'version': '0.9.0', 'parallel_read_safe': True}
