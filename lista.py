import os
l = os.listdir('scripts/pt-br')

for x in l:
  print(''' "aleatorio":{''')
  print('''   "pt-br":"pt-br/{}",'''.format(x))
  print('''   "en-us":"",''')
  print('''   "es":""''')
  print('''},''')
  
