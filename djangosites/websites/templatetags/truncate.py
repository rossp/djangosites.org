from django import template
 
register = template.Library()
 
def truncate(value, size):
  return value[0:size]
 
def truncate_dot(value, size):
  if len(value) > size and size > 3:
    return value[0:(size-3)] + '...'
  else:
    return value[0:size]

register.filter('truncate', truncate)
register.filter('truncate_dot', truncate_dot)
