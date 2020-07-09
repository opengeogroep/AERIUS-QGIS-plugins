


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


    def add_widgets(self, name, widgets=[]):
        if not name in self:
            self[name] = []
        for widget in widgets:
            if widget in self[name]:
                print('widget already registered (error)')
            else:
                self[name].append(widget)


    def remove_group(self, name):
        if not name in self:
            print('name not in widget_registry')
            return
        for widget in self[name]:
            self[name].remove(widget)
        self.pop(name)


    def remove_all_groups(self):
        names = list(self.keys())
        for name in names:
            self.remove_group(name)


    def show(self):
        print(self)
        for name in self:
            print('  {}'.format(name))
            for widget in self[name]:
                print('    {}'.format(widget))
