import json
import time


database = '''
{
  "av_system": "Avell Checker - BIOS and EC",
  "av_version": 1,
  "av_lastchange": "2021-08-17T00:00:00.000Z",
  "notebooks": [
    {
      "hw_proc": "AMD Ryzen 3500U",
      "hw_code": "A40A35M",
      "hw_ec": "1.03.10",
      "hw_bios": "N.1.00"
    },
    {
      "hw_code": "A52D105B",
      "hw_ec": "1.17.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "A52D105D",
      "hw_ec": "1.17.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "A52F91A",
      "hw_ec": "1.10.00",
      "hw_bios": "N.1.03"
    },
    {
      "hw_code": "A60D91C",
      "hw_ec": "1.25.00",
      "hw_bios": "QCCFL357.0122.2020.0911.1520"
    },
    {
      "hw_code": "A62D91B",
      "hw_ec": "1.10.00",
      "hw_bios": "N.1.03"
    },
    {
      "hw_code": "A62D107B",
      "hw_ec": "1.17.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "A62D107D",
      "hw_ec": "1.17.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "A62D107E",
      "hw_ec": "1.16.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "A62F91B",
      "hw_ec": "1.10.00",
      "hw_bios": "N.1.03"
    },
    {
      "hw_code": "A65D107E",
      "hw_ec": "1.9.00",
      "hw_bios": "N.1.01"
    },
    {
      "hw_code": "A65D107F",
      "hw_ec": "1.9.00",
      "hw_bios": "N.1.01"
    },
    {
      "hw_code": "C62D105B",
      "hw_ec": "1.17.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "C62D107B",
      "hw_ec": "1.17.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "C62D107D",
      "hw_ec": "1.16.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "C62D107E",
      "hw_ec": "1.16.00",
      "hw_bios": "N.1.02"
    },
    {
      "hw_code": "C65D107F",
      "hw_ec": "1.9.00",
      "hw_bios": "N.1.03"
    },
    {
      "hw_code": "C65D107G",
      "hw_ec": "1.9.00",
      "hw_bios": "N.1.01"
    },
    {
      "hw_code": "C65D109F",
      "hw_ec": "1.9.00",
      "hw_bios": "N.1.01"
    },
    {
      "hw_code": "C65D109G",
      "hw_ec": "1.9.00",
      "hw_bios": "N.1.01"
    },
    {
      "hw_code": "ST1A4",
      "hw_ec": "1.27.00",
      "hw_bios": "N.1.05AVE01"
    },
    {
      "hw_code": "A70D107H",
      "hw_ec": "1.14.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "A70D107I",
      "hw_ec": "1.14.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "A72D107H",
      "hw_ec": "1.14.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "A72D107I",
      "hw_ec": "1.14.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "C62D107H",
      "hw_ec": "1.14.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "C65D107H",
      "hw_ec": "1.14.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "C65D107I",
      "hw_ec": "1.14.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "A52D115K",
      "hw_ec": "1.2.00",
      "hw_bios": "N.1.04AVE00"
    },
    {
      "hw_code": "A65D117H",
      "hw_ec": "1.4.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "A65D117I",
      "hw_ec": "1.4.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "A70D117K",
      "hw_ec": "1.2.00",
      "hw_bios": "N.1.04AVE00"
    },
    {
      "hw_code": "A70D117H",
      "hw_ec": "1.4.00",
      "hw_bios": "N.1.07AVE00"
    },
    
    {
      "hw_code": "C62D117K",
      "hw_ec": "1.2.00",
      "hw_bios": "N.1.04AVE00"
    },
    {
      "hw_code": "C62D115K",
      "hw_ec": "1.2.00",
      "hw_bios": "N.1.04AVE00"
    },
    {
      "hw_code": "C62D117H",
      "hw_ec": "1.4.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "C65D117I",
      "hw_ec": "1.4.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "C65D119J",
      "hw_ec": "1.4.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "C65D117J",
      "hw_ec": "1.4.00",
      "hw_bios": "N.1.07AVE00"
    },
    {
      "hw_code": "BOND115X",
      "hw_ec": "0.33.00",
      "hw_bios": "BCTGL357.0067.2021.0810.1743"
    },
    {
      "hw_code": "BOND117X",
      "hw_ec": "0.33.00",
      "hw_bios": "BCTGL357.0067.2021.0810.1743"
    },
    {
      "hw_code": "B11D117K",
      "hw_ec": "1.8.00",
      "hw_bios": "N.1.01AVE00"
    }
    
  ]
}


'''

db = json.loads(database)



def nb_compare(varCode, varEC, varBIOS):
    isOK = False
    
    for nb in db['notebooks']:
        if nb.get('hw_code') == varCode[:8]:
            if nb.get('hw_ec') == varEC:
                if nb.get('hw_bios') == varBIOS:
                    isOK = True

    # print('%s - %s - %s - %s\n' % (nb.get('hw_proc'), nb.get('hw_code'), nb.get('hw_ec'), nb.get('hw_bios')))

    return isOK


