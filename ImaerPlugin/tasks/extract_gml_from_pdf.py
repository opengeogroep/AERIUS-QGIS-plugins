from qgis.core import (
    Qgis,
    QgsTask,
    QgsMessageLog
)

tab = 'Imaer'


class ExtractGmlFromPdfTask(QgsTask):

    def __init__(self, pdf_fn, gml_base_fn, callback):
        super().__init__('Extract GML from IMAER PDF', QgsTask.CanCancel)
        self.pdf_fn = pdf_fn
        self.gml_base_fn = gml_base_fn
        self.gml_fns = []
        self.callback = callback
        self.exception = None
        self.do_log = True
        # self.log(self.pdf_fn)

    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)

    def run(self):
        self.log('Started task "{}"'.format(self.description()))

        self.setProgress(0)

        with open(self.pdf_fn, 'r', errors='ignore') as pdf_file:
            for pdf_line in pdf_file:
                if '<imaer:FeatureCollectionCalculator' in pdf_line:
                    self.setProgress(10)
                    gml_strings = self.get_gml_strings(pdf_line)
                    if len(gml_strings) > 0:
                        break
            self.setProgress(20)

        if len(gml_strings) == 0:
            self.setProgress(100)
            return False

        i = 0
        self.gml_fns = []
        for gml_str in gml_strings:
            gml_fn = self.gml_base_fn.format(i)
            self.gml_fns.append(gml_fn)
            gml_lines = gml_str.split('\\n')
            self.setProgress(60)
            with open(gml_fn, 'w') as gml_file:
                # self.log(f'Writing GML file: {gml_fn}')
                for gml_line in gml_lines:
                    gml_file.write(gml_line + '\n')
                    if self.isCanceled():
                        return False
            i += 1

        self.setProgress(100)
        return True

    def finished(self, result):
        self.log('finished task')
        if result:
            self.callback(self.gml_fns)
        else:
            self.callback([])

    def cancel(self):
        self.log(
            'Task "{name}" was canceled'.format(
                name=self.description()))
        # TODO delete gml file if exists
        super().cancel()

    def get_gml_strings(self, pdf_line):
        result = []
        start_string = '<?xml '
        end_string = '</imaer:FeatureCollectionCalculator>'

        stop = False
        start_char = 0

        while not stop:
            '''Finds the gml part in the pdf line'''
            first_char = pdf_line.find(start_string, start_char)
            if first_char < 0:
                break
            last_char = pdf_line.find(end_string, first_char)
            if last_char < 0:
                break
            last_char += len(end_string)  # add the length of the search string to jump to the end
            result.append(pdf_line[first_char:last_char])
            start_char = last_char

        return result
