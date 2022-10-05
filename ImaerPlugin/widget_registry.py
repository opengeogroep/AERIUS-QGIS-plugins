class WidgetRegistry(dict):

    def __init__(self, parent):
        self.parent = parent

    def __str__(self):
        widget_cnt = 0
        for name in self:
            widget_cnt += len(self[name])
        result = 'WidgetRegistry[names: {}, widgets: {}]'.format(
            len(self),
            widget_cnt
        )
        return result

    def add_widgets(self, name, widgets={}):
        if name not in self:
            self[name] = {}
        for widget_key, widget in widgets.items():
            if widget_key in self[name]:
                print('widget already registered (error)')
            else:
                self[name][widget_key] = widget

    def remove_group(self, name):
        if name not in self:
            print('name not in widget_registry')
            return
        widget_keys = list(self[name].keys())
        for widget_key in widget_keys:
            self[name].pop(widget_key)
        self.pop(name)

    def remove_all_groups(self):
        names = list(self.keys())
        for name in names:
            self.remove_group(name)

    def show(self):
        print(self)
        for name in self:
            print('  {}'.format(name))
            for widget_key, widget in self[name].items():
                print('    {} {}'.format(widget_key, widget))
