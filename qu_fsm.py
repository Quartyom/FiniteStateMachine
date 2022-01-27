# how to use
#
# set_attrs(attr1 = "value", attr2 = "value", ...)
# more important -> less important attributes
#
# @command(attrn = "value", ...)
# def foo(*args):
#   pass
#
# change_attrs(**attrs)
#
# handle_command(*args)
# call the function by _current_attrs

from qu_json import*

class Qu_fsm:
    _all_funcs = dict()
    _all_attrs = dict()
    _current_attrs = dict()

    def __init__(self, file_path):
        self.json_file = Qu_json(file_path)

    def set_default_attrs(self, **attrs):
        if self._all_funcs:
            raise Exception("You can set attrs only before functions definition")
        for key in attrs:
            self._all_attrs[key] = attrs[key]

        if self.json_file.data:    # if data exists
            self._current_attrs = self.json_file.data
        else:
            self._current_attrs = dict(self._all_attrs)
            self.json_file.data = self._current_attrs
            self.json_file.save()

    def get_attr(self, attr_name):
        return self._current_attrs[attr_name]

    def change_attrs(self, **attrs):
        for key in attrs:
            if key not in self._current_attrs:
                raise NameError
            else:
                self._current_attrs[key] = attrs[key]
                
        self.json_file.save()
                
    def method(self, **attrs):  
        def wrap(func):
            out_attrs = dict(self._all_attrs)
            
            for key in attrs:
                out_attrs[key] = attrs[key]
                
            self._all_funcs[str(out_attrs)] = func
            return func
        return wrap

    def handle_method(self, *args):   
        out_attrs = dict(self._current_attrs)
        keys = list(self._current_attrs)[::-1]

        if str(out_attrs) in self._all_funcs:
            self._all_funcs[str(out_attrs)](*args)
            return True
        
        for key in keys:
            out_attrs[key] = self._all_attrs[key]
            if str(out_attrs) in self._all_funcs:
                self._all_funcs[str(out_attrs)](*args)
                return True

        print(self._current_attrs, out_attrs, self._all_attrs)
        print(self._all_funcs)
        return False
