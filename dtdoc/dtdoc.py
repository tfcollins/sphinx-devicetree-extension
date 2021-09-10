from docutils import nodes
from docutils.parsers.rst import Directive

import os
import yaml

class DeviceTreeParser(Directive):

    required_arguments = 1

    def get_yaml(self, fn):
        d = os.path.dirname(__file__)
        s = os.path.split(d)
        s = os.path.join(s[0],'tests','Documentation/devicetree/bindings',fn)
        with open(s) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        #import pprint
        #pprint.pprint(data)
        #pprint.pprint(data['patternProperties']['^channel@[0-9]$']['properties'])

        props = data['patternProperties']['^channel@[0-9]$']['properties']

        section = nodes.section()
        sn = fn.split('/')[-1].split('.')[0]
        section += nodes.title('adi,ltc6952.yaml', sn)
        fields = nodes.field_list()
        for prop in props:
            name = nodes.field_name(text=prop)
            body = nodes.field_body()
            params = nodes.paragraph(text='')
            for p in props[prop]:
                params += nodes.Text(props[prop][p])
            body += params
            field = nodes.field('', name, body)
            fields += field

        section += fields

        sections = []
        sections += section


        return sections

    def run(self):
        return self.get_yaml(self.arguments[0])


def setup(app):
    app.add_directive("devicetree", DeviceTreeParser)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
