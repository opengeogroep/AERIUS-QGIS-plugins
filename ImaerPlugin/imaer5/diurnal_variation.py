from PyQt5.QtXml import QDomDocument


class DiurnalVariation(object):

    def __init__(self):
        pass

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:diurnalVariation')
        return result


class StandardDiurnalVariation(DiurnalVariation):

    def __init__(self, *, standard_type, **kwargs):
        super().__init__(**kwargs)
        self.standard_type = standard_type

    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)

        dv = doc.createElement('imaer:StandardDiurnalVariation')
        st = doc.createElement('imaer:standardType')
        st.appendChild(doc.createTextNode(str(self.standard_type)))

        dv.appendChild(st)
        result.appendChild(dv)

        return result


class ReferenceDiurnalVariation(DiurnalVariation):
    def __init__(self, *, local_id, **kwargs):
        super().__init__(**kwargs)
        self.local_id = local_id

    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)

        rdv = doc.createElement('imaer:ReferenceDiurnalVariation')

        dv = doc.createElement('imaer:customDiurnalVariation')
        dv.setAttribute('xlink:href', f'#DiurnalProfile.{self.local_id}')

        rdv.appendChild(dv)
        result.appendChild(rdv)

        return result


class CustomDiurnalVariation(DiurnalVariation):

    def __init__(self, *, local_id, custom_type, values=None, **kwargs):
        super().__init__(**kwargs)
        self.local_id = local_id
        self.custom_type = custom_type
        self.values = values or []

    def to_xml_elem(self, doc=QDomDocument()):
        # Does not run super class method because this element will be add_open_data
        # to the document as a "definition".

        result = doc.createElement('imaer:customDiurnalVariation')
        dv = doc.createElement('imaer:CustomDiurnalVariation')
        dv.setAttribute('gml:id', f'DiurnalProfile.{self.local_id}')

        elem = doc.createElement('imaer:customType')
        elem.appendChild(doc.createTextNode(str(self.custom_type)))
        dv.appendChild(elem)

        for value in self.values:
            elem = doc.createElement('imaer:value')
            elem.appendChild(doc.createTextNode(str(value)))
            dv.appendChild(elem)

        result.appendChild(dv)

        return result
