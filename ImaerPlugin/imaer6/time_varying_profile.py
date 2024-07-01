from PyQt5.QtXml import QDomDocument


class TimeVaryingProfile(object):

    def __init__(self):
        pass


class StandardTimeVaryingProfile(TimeVaryingProfile):

    def __init__(self, *, standard_type, **kwargs):
        super().__init__(**kwargs)
        self.standard_type = standard_type

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:StandardTimeVaryingProfile')

        st = doc.createElement('imaer:standardType')
        st.appendChild(doc.createTextNode(str(self.standard_type)))
        result.appendChild(st)

        return result


class ReferenceTimeVaryingProfile(TimeVaryingProfile):
    def __init__(self, *, local_id, **kwargs):
        super().__init__(**kwargs)
        self.local_id = local_id

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:ReferenceTimeVaryingProfile')

        dv = doc.createElement('imaer:customTimeVaryingProfile')
        dv.setAttribute('xlink:href', f'#TimeVaryingProfile.{self.local_id}')
        result.appendChild(dv)

        return result


class CustomTimeVaryingProfile(TimeVaryingProfile):

    def __init__(self, *, local_id, custom_type, label=None, values=None, **kwargs):
        super().__init__(**kwargs)
        self.local_id = local_id
        self.custom_type = custom_type
        self.label = label
        self.values = values or []
        self.__custom_types = {
            'DAY': {'cols': 1, 'rows': 24},
            'THREE_DAY': {'cols': 3, 'rows': 24},
            'MONTHLY': {'cols': 1, 'rows': 12},
        }

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:customTimeVaryingProfile')
        dv = doc.createElement('imaer:CustomTimeVaryingProfile')
        dv.setAttribute('gml:id', f'TimeVaryingProfile.{self.local_id}')

        if self.label is not None:
            elem = doc.createElement('imaer:label')
            elem.appendChild(doc.createTextNode(str(self.label)))
            dv.appendChild(elem)

        elem = doc.createElement('imaer:customType')
        elem.appendChild(doc.createTextNode(str(self.custom_type)))
        dv.appendChild(elem)

        for value in self.values:
            elem = doc.createElement('imaer:value')
            elem.appendChild(doc.createTextNode(str(value)))
            dv.appendChild(elem)

        result.appendChild(dv)

        return result

    def values_to_csv(self):
        # print('values_to_csv')
        
        # Return empty string for new objects
        if len(self.values) == 0:
            return ''

        num_cols = self.__custom_types[self.custom_type]['cols']
        num_rows = self.__custom_types[self.custom_type]['rows']

        result = ''
        i = 0
        for row_nr in range(num_rows):
            for col_nr in range(num_cols):
                result += str(self.values[i])
                if col_nr < num_cols - 1:
                    result += ';'
                else:
                    result += '\n'
                i += 1
        return result

    def values_from_csv(self, csv_text):
        # print('values_from_csv')
        num_cols = self.__custom_types[self.custom_type]['cols']
        num_rows = self.__custom_types[self.custom_type]['rows']

        # csv to recs and values
        recs = []
        for line in csv_text.split('\n'):
            values = []
            if not len(line.strip()) > 0:
                continue
            for part in line.split(';'):
                try:
                    values.append(float(part))
                except ValueError:
                    return False
            if len(values) == num_cols:
                recs.append(values)
        
        result = []
        for rec in recs:
            for value in rec:
                result.append(value)
        
        if not (num_rows * num_cols) == len(result):
            return False

        self.values = result
        return True
