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
            'DAY': {'cols': 1, 'hours': 24},
            'THREE_DAY': {'cols': 3, 'hours': 24},
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
        # Return empty string for new objects
        if len(self.values) == 0:
            return ''

        cols = self.__custom_types[self.custom_type]['cols']
        hours = self.__custom_types[self.custom_type]['hours']

        result = ''
        for row_nr in range(hours):
            for col_nr in range(cols):
                i = (hours * col_nr) + row_nr
                result += str(self.values[i])
                if col_nr < cols - 1:
                    result += ';'
                else:
                    result += '\n'
        return result

    def values_from_csv(self, csv_text):
        cols = self.__custom_types[self.custom_type]['cols']
        hours = self.__custom_types[self.custom_type]['hours']

        rows = []
        for line in csv_text.split('\n'):
            values = []
            if len(line.strip()) > 0:
                for value in line.split(';'):
                    try:
                        values.append(float(value))
                    except ValueError:
                        return False
            if len(values) == cols:
                rows.append(values)

        cnt = 0
        for col in rows:
            cnt += len(col)

        if not (cols * hours) == cnt:
            return False

        result = []
        for col_nr in range(cols):
            for row in rows:
                result.append(row[col_nr])
        self.values = result
        return True
