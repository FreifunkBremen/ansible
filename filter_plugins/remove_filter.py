# removes an element from a list
class FilterModule (object):
  def filters(self):
    return {
      "remove": self.remove,
    }

  def remove(self, l, e):
    if e in l:
      l.remove(e)
    return l
