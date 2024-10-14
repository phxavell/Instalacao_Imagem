#!/usr/bin/env python3.7

from dialog import Dialog





d = Dialog(dialog="dialog")

notebooks = [
    ("A40A35M",  "Avell A40 LIV", "NVidia MX 250"),
    ("A52D105B", "Avell A52 LIV", "NVidia GTX 1650"),
    ("A52F91A",  "Avell A52 MUV", "NVidia GTX 1050"),
#    ("A60D91C",  "Avell A60 MUV", "NVidia GTX 1660 TI"),
#    ("A62D107B", "Avell A62 LIV", "NVidia GTX 1650"),
#    ("A62D107D", "Avell A62 LIV", "NVidia GTX 1650 TI"),
#    ("A62D107E", "Avell A62 LIV", "NVidia RTX 2060"),
#    ("A62D91B",  "Avell A62 MUV", "NVidia GTX 1650"),
#    ("A62D91C",  "Avell A62 MUV", "NVidia GTX 1660 TI"),
#    ("A62F91B",  "Avell A62 MUV", "NVidia GTX 1650"),
#    ("A65D107E", "Avell A65 LIV", "NVidia RTX 2060"),
#    ("A65D107F", "Avell A65 LIV", "NVidia RTX 2070"),
#    ("C62D105B", "Avell C62 LIV", "NVidia GTX 1650"),
#    ("C62D107B", "Avell C62 LIV", "NVidia GTX 1650"),
#    ("C62D107D", "Avell C62 LIV", "NVidia GTX 1650 TI"),
#    ("C62D107E", "Avell C62 LIV", "NVidia RTX 2060"),
#    ("C65D107F", "Avell C65 LIV", "NVidia RTX 2070"),
#    ("C65D107G", "Avell C65 LIV", "NVidia RTX 2080"),
#    ("C65D109F", "Avell C65 LIV", "NVidia RTX 2070"),
#    ("C65D109G", "Avell C65 LIV", "NVidia RTX 2080"),
#    ("C65D91B",  "Avell C65 MUV", "NVidia GTX 1650"),
#    ("C65D91C",  "Avell C65 MUV", "NVidia GTX 1660 TI"),
]

diag_notebook_code, tag = d.menu(
    'Selecionar Notebook Avell', choices=[
        ("A40A35M",  "Avell A40 LIV NVidia MX 250"),
        ("A52D105B", "Avell A52 LIV NVidia GTX 1650"),
        ("A52F91A",  "Avell A52 MUV NVidia GTX 1050"),
 #       ("A60D91C",  "Avell A60 MUV NVidia GTX 1660 TI"),
 #       ("A62D107B", "Avell A62 LIV NVidia GTX 1650"),
 #       ("A62D107D", "Avell A62 LIV NVidia GTX 1650 TI"),
 #       ("A62D107E", "Avell A62 LIV NVidia RTX 2060"),
 #       ("A62D91B",  "Avell A62 MUV NVidia GTX 1650"),
 #       ("A62D91C",  "Avell A62 MUV NVidia GTX 1660 TI"),
 #       ("A62F91B",  "Avell A62 MUV NVidia GTX 1650"),
 #       ("A65D107E", "Avell A65 LIV NVidia RTX 2060"),
 #       ("A65D107F", "Avell A65 LIV NVidia RTX 2070"),
 #       ("C62D105B", "Avell C62 LIV NVidia GTX 1650"),
 #       ("C62D107B", "Avell C62 LIV NVidia GTX 1650"),
 #       ("C62D107D", "Avell C62 LIV NVidia GTX 1650 TI"),
 #       ("C62D107E", "Avell C62 LIV NVidia RTX 2060"),
 #       ("C65D107F", "Avell C65 LIV NVidia RTX 2070"),
 #       ("C65D107G", "Avell C65 LIV NVidia RTX 2080"),
 #       ("C65D109F", "Avell C65 LIV NVidia RTX 2070"),
 #       ("C65D109G", "Avell C65 LIV NVidia RTX 2080"),
 #       ("C65D91B",  "Avell C65 MUV NVidia GTX 1650"),
 #       ("C65D91C",  "Avell C65 MUV NVidia GTX 1660 TI"),
   ]
)


if diag_notebook_code != 'ok':
    print('Notebook nao selecionado')
    sys.exit(5)


print(diag_notebook_code)

nb_name = ''
nb_gpu = ''
nb_voltage = ''
nb_amp = ''
nb_powersupply = ''

if tag == 'A40A35M':
    nb_name = 'Avell A40 LIV'
    nb_gpu = 'NVidia MX 250'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A52D105B':
    nb_name = 'Avell A52 LIV'
    nb_gpu = ' NVidia GTX 1650'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A52F91A':
    nb_name = 'Avell A52 MUV'
    nb_gpu = 'NVidia GTX 1050'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A60D91C':
    nb_name = 'Avell A60 MUV'
    nb_gpu = 'NVidia GTX 1660 TI'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A62D107B':
    nb_name = 'Avell A62 LIV'
    nb_gpu = 'NVidia GTX 1650'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A62D107D':
    nb_name = 'Avell A62 LIV'
    nb_gpu = 'NVidia GTX 1650 TI'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A62D107E':
    nb_name = 'Avell A62 LIV'
    nb_gpu = 'NVidia RTX 2060'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A62D91B':
    nb_name = 'Avell A62 MUV'
    nb_gpu = 'NVidia GTX 1650'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A62D91C':
    nb_name = 'Avell A62 MUV'
    nb_gpu = 'NVidia GTX 1660 TI'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A62F91B':
    nb_name = 'Avell A62 MUV'
    nb_gpu = 'NVidia GTX 1650'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A65D107E':
    nb_name = 'Avell A65 LIV'
    nb_gpu = 'NVidia RTX 2060'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'A65D107F':
    nb_name = 'Avell A65 LIV'
    nb_gpu = 'NVidia RTX 2070'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C62D105B':
    nb_name = 'Avell C62 LIV'
    nb_gpu = 'NVidia GTX 1650'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C62D107B':
    nb_name = 'Avell C62 LIV'
    nb_gpu = 'NVidia GTX 1650'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C62D107D':
    nb_name = 'Avell C62 LIV'
    nb_gpu = 'NVidia GTX 1650 TI'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C62D107E':
    nb_name = 'Avell C62 LIV'
    nb_gpu = 'NVidia RTX 2060'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'
 
if tag == 'C65D107F':
    nb_name = 'Avell C65 LIV'
    nb_gpu = 'NVidia RTX 2070'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C65D107G':
    nb_name = 'Avell C65 LIV'
    nb_gpu = 'NVidia RTX 2080'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C65D109F':
    nb_name = 'Avell C65 LIV'
    nb_gpu = 'NVidia RTX 2070'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C65D109G':
    nb_name = 'Avell C65 LIV'
    nb_gpu = 'NVidia RTX 2080'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C65D91B':
    nb_name = 'Avell C65 MUV'
    nb_gpu = 'NVidia GTX 1650'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'

if tag == 'C65D91C':
    nb_name = 'Avell C65 MUV'
    nb_gpu = 'NVidia GTX 1660 TI'
    nb_voltage = '19,5'
    nb_amp = '9,13'
    nb_powersupply = '???'
  


print('O codigo selecionado eh %s com a tag %s.' % (diag_notebook_code, tag))
print(
    '%s %s %s %s' % (
        nb_name, nb_gpu, nb_voltage, nb_amp
    )
)

weekcurrent = datetime.date(
    datetime.datetime.now().year,
    datetime.datetime.now().month,
    datetime.datetime.now().day
).isocalendar()[1]

week_code, week_input = d.inputbox(
    'Qual semana?',
    init=str(weekcurrent).zfill(2),
    title='Semana'
)

if week_code != 'ok':
    print('Semana foi cancelada')
    sys.exit(5)

print('A semana sugerida foi %s, mas a escolhida foi %s!' % (week_code, week_input))

initial_code, initial_input = d.inputbox(
    'Qual numero inicial?',
    init='000',
    title='Numero inicial'
)

if initial_code != 'ok':
    print('Numero inicial foi cancelado')
    sys.exit(5)


final_code, final_input = d.inputbox(
    'Qual numero final?',
    init='',
    title='Numero final'
)

if final_code != 'ok':
    print('Numero final foi cancelado')
    sys.exit(5)

if final_input == '':
    print('Numero final estah vazio.')
    sys.exit(5)

for etiqueta in range(int(initial_input), int(final_input) + 1):
    os.system('/usr/sbin/usbconfig ugen0.5 reset')
    os.system('cat label_template.txt | sed "s/ZZZ1/' + nb_name + '/g" | sed "s/ZZZ2/' + nb_gpu + '/g" | sed "s/ZZZ3/' +nb_voltage + '/g"  | sed "s/ZZZ4/' + nb_amp  + '/g"  | sed "s/ZZZ5/AVNB21' +  str(week_input) + str(etiqueta).zfill(3)  + '/g" > /dev/unlpt0')



