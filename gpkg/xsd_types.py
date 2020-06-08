

namespaces = {'xmlns': 'http://www.w3.org/2001/XMLSchema'}

class XsdElement():

    def __init__(self, elem):
        #print('hiero:', elem)
        self.name = elem.get('name')
        self.type = elem.get('type')
        #self.substitutionGroup = elem.get('substitutionGroup')


    def __str__(self):
        result = 'XsdElement[{} ({}) <{}>]'.format(self.name, self.type, self.isBaseType())
        return result

    def isBaseType(self):
        print(self.type)
        return self.type in ['string', 'double', 'integer']





class XsdSimpleType():

    def __init__(self, elem):
        self.elem = elem
        self.name = elem.get('name')
        self.enumeration = []
        restrictions = elem.findall('xmlns:restriction', namespaces)
        if len(restrictions) == 1:
            restriction = restrictions[0]
            self.data_type = restriction.get('base')
            #print(self.data_type)
            enums = restriction.findall('xmlns:enumeration', namespaces)
            if len(enums) > 0:
                for enum in enums:
                    v = enum.get('value')
                    a = None
                    self.enumeration.append({'value': v, 'annotation': a})
        else:
            print('None or multiple restrictions!')


    def __str__(self):
        result = 'XsdSimpleType[{} ({}), {}]'.format(self.name, self.data_type, self.enumeration)
        return result

    def createTable(self, db):
        q = 'DROP TABLE IF EXISTS {}'.format(self.name)
        db.run_query_text(q)

        q = 'CREATE TABLE {} (value string, annotation string)'.format(self.name)
        db.run_query_text(q)

        for enum in self.enumeration:
            q = 'INSERT INTO {} VALUES (?, NULL)'.format(self.name)
            db.run_query_text(q, (enum['value'],))




class XsdComplexType():

    def __init__(self, elem):
        self.name = elem.get('name')
        print(self.name)
        if elem.get('substitutionGroup') == "gml:AbstractObject":
            print('  abstract!')
        #self.restriction = elem.findall('restriction')
        for child in elem:
            print(' #', child.tag.replace('{http://www.w3.org/2001/XMLSchema}', ''))
            pass


        self.elements = []
        sequences = elem.findall('xmlns:sequence', namespaces)
        if len(sequences) == 1:
            sequence = sequences[0]
            for child in sequence:
                #print(' -', child)
                if child.tag == '{http://www.w3.org/2001/XMLSchema}element':
                    elem = XsdElement(child)
                    print('   -', elem)
                    self.elements.append(elem)

        else:
            print('no sequence in complexType')


    def __str__(self):
        result = 'XsdComplexType[{}]'.format(self.name)
        return result


    def createTable(self, db):


        q = 'DROP TABLE IF EXISTS {}'.format(self.name)
        db.run_query_text(q)

        q = 'CREATE TABLE {} ('.format(self.name)
        field_list = ['id integer']
        for elem in self.elements:
            if elem.isBaseType():
                field_list.append('{} {}'.format(elem.name, elem.type))
        print(field_list)
        q += ', '.join(field_list)
        q += ')'
        print('q:', q)
        if len(field_list) > 0:
            pass
        db.run_query_text(q)
