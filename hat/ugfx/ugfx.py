# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_ugfx')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_ugfx')
    _ugfx = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_ugfx', [dirname(__file__)])
        except ImportError:
            import _ugfx
            return _ugfx
        try:
            _mod = imp.load_module('_ugfx', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _ugfx = swig_import_helper()
    del swig_import_helper
else:
    import _ugfx
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0


def color(r, g, b):
    return _ugfx.color(r, g, b)
color = _ugfx.color
class surface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, surface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, surface, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _ugfx.new_surface(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _ugfx.delete_surface
    __del__ = lambda self: None

    def store_grey(self, filename):
        return _ugfx.surface_store_grey(self, filename)

    def blit(self, src, xoff, yoff, flip=False):
        return _ugfx.surface_blit(self, src, xoff, yoff, flip)

    def magnify(self, src, factor):
        return _ugfx.surface_magnify(self, src, factor)

    def putpixel(self, x, y, c):
        return _ugfx.surface_putpixel(self, x, y, c)

    def line(self, x1, y1, x2, y2, c):
        return _ugfx.surface_line(self, x1, y1, x2, y2, c)

    def hline(self, x1, x2, y, c):
        return _ugfx.surface_hline(self, x1, x2, y, c)

    def vline(self, x, y1, y2, c):
        return _ugfx.surface_vline(self, x, y1, y2, c)

    def box(self, x1, y1, x2, y2, c):
        return _ugfx.surface_box(self, x1, y1, x2, y2, c)

    def invert(self, x1, y1, x2, y2):
        return _ugfx.surface_invert(self, x1, y1, x2, y2)

    def fill(self, c):
        return _ugfx.surface_fill(self, c)

    def refresh(self):
        return _ugfx.surface_refresh(self)

    def binary_write_sw(self, sclk, mosi):
        return _ugfx.surface_binary_write_sw(self, sclk, mosi)
    __swig_setmethods__["width"] = _ugfx.surface_width_set
    __swig_getmethods__["width"] = _ugfx.surface_width_get
    if _newclass:
        width = _swig_property(_ugfx.surface_width_get, _ugfx.surface_width_set)
    __swig_setmethods__["height"] = _ugfx.surface_height_set
    __swig_getmethods__["height"] = _ugfx.surface_height_get
    if _newclass:
        height = _swig_property(_ugfx.surface_height_get, _ugfx.surface_height_set)
    __swig_setmethods__["bypp"] = _ugfx.surface_bypp_set
    __swig_getmethods__["bypp"] = _ugfx.surface_bypp_get
    if _newclass:
        bypp = _swig_property(_ugfx.surface_bypp_get, _ugfx.surface_bypp_set)
    __swig_setmethods__["p"] = _ugfx.surface_p_set
    __swig_getmethods__["p"] = _ugfx.surface_p_get
    if _newclass:
        p = _swig_property(_ugfx.surface_p_get, _ugfx.surface_p_set)

    def getpixel(self, x, y):
        return _ugfx.surface_getpixel(self, x, y)

    def ptr(self):
        return _ugfx.surface_ptr(self)
    __swig_setmethods__["xoffset"] = _ugfx.surface_xoffset_set
    __swig_getmethods__["xoffset"] = _ugfx.surface_xoffset_get
    if _newclass:
        xoffset = _swig_property(_ugfx.surface_xoffset_get, _ugfx.surface_xoffset_set)
    __swig_setmethods__["yoffset"] = _ugfx.surface_yoffset_set
    __swig_getmethods__["yoffset"] = _ugfx.surface_yoffset_get
    if _newclass:
        yoffset = _swig_property(_ugfx.surface_yoffset_get, _ugfx.surface_yoffset_set)
    __swig_setmethods__["line_length"] = _ugfx.surface_line_length_set
    __swig_getmethods__["line_length"] = _ugfx.surface_line_length_get
    if _newclass:
        line_length = _swig_property(_ugfx.surface_line_length_get, _ugfx.surface_line_length_set)
surface_swigregister = _ugfx.surface_swigregister
surface_swigregister(surface)

class screen(surface):
    __swig_setmethods__ = {}
    for _s in [surface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, screen, name, value)
    __swig_getmethods__ = {}
    for _s in [surface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, screen, name)
    __repr__ = _swig_repr

    def __init__(self, device):
        this = _ugfx.new_screen(device)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _ugfx.delete_screen
    __del__ = lambda self: None
    __swig_setmethods__["finfo"] = _ugfx.screen_finfo_set
    __swig_getmethods__["finfo"] = _ugfx.screen_finfo_get
    if _newclass:
        finfo = _swig_property(_ugfx.screen_finfo_get, _ugfx.screen_finfo_set)
    __swig_setmethods__["vinfo"] = _ugfx.screen_vinfo_set
    __swig_getmethods__["vinfo"] = _ugfx.screen_vinfo_get
    if _newclass:
        vinfo = _swig_property(_ugfx.screen_vinfo_get, _ugfx.screen_vinfo_set)
    __swig_setmethods__["fbp"] = _ugfx.screen_fbp_set
    __swig_getmethods__["fbp"] = _ugfx.screen_fbp_get
    if _newclass:
        fbp = _swig_property(_ugfx.screen_fbp_get, _ugfx.screen_fbp_set)
    __swig_setmethods__["fbfd"] = _ugfx.screen_fbfd_set
    __swig_getmethods__["fbfd"] = _ugfx.screen_fbfd_get
    if _newclass:
        fbfd = _swig_property(_ugfx.screen_fbfd_get, _ugfx.screen_fbfd_set)
    __swig_setmethods__["screensize"] = _ugfx.screen_screensize_set
    __swig_getmethods__["screensize"] = _ugfx.screen_screensize_get
    if _newclass:
        screensize = _swig_property(_ugfx.screen_screensize_get, _ugfx.screen_screensize_set)
screen_swigregister = _ugfx.screen_swigregister
screen_swigregister(screen)

# This file is compatible with both classic and new-style classes.

