def gattrs(o):
  return [i for i in dir(o) if not callable(getattr(o,i)) and not i.startswith('__')]