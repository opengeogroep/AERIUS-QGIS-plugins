from qgis.core import (
    Qgis,
    QgsTask,
    QgsMessageLog
    )

tab = 'Imaer'




class ExtractGmlFromPdfTask(QgsTask):

    def __init__(self, pdf_fn, gml_fn, callback):
        super().__init__('Extract GML from IMAER PDF', QgsTask.CanCancel)
        self.pdf_fn = pdf_fn
        self.gml_fn = gml_fn
        self.callback = callback
        self.exception = None
        self.do_log = True
        #self.log(self.pdf_fn)
        #self.log(self.gml_fn)


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def run(self):
        self.log('Started task "{}"'.format(self.description()))

        self.setProgress(0)

        gml_str = None
        with open(self.pdf_fn, 'r', errors='ignore') as pdf_file:
            for pdf_line in pdf_file:
                if '<imaer:FeatureCollectionCalculator' in pdf_line:
                    self.setProgress(10)
                    gml_str = self.get_gml_string(pdf_line)
                    if gml_str is not None:
                        break
            self.setProgress(20)

        if gml_str is None:
            self.setProgress(100)
            #self.exception = Exception('NoGml')
            return False

        gml_lines = gml_str.split('\\n')
        self.setProgress(60)
        with open(self.gml_fn, 'w') as gml_file:
            for gml_line in gml_lines:
                gml_file.write(gml_line + '\n')
                if self.isCanceled():
                    return False

        self.setProgress(100)
        return True


    def finished(self, result):
        self.log('finished task')
        if result:
            self.callback(self.gml_fn)
        else:
            self.callback(None)


    def cancel(self):
        self.log(
            'Task "{name}" was canceled'.format(
                name=self.description()))
                # TODO delete gml file if exists
        super().cancel()


    def get_gml_string(self, pdf_line):
        '''Finds the gml part in the pdf line'''
        first_char = pdf_line.find('/calculation(')
        if first_char < 0:
            return
        last_char = pdf_line.find(')>>', first_char)
        if last_char < 0:
            return
        first_char += 13 # add the length of the search string to jump to the end
        gml_str = pdf_line[first_char:last_char]
        return gml_str
