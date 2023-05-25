from flask import render_template, session

sand = {
    'B1': {
        'loam': {
            'min': 0,
            'max': 10,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B2': {
        'loam': {
            'min': 10,
            'max': 18,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B3': {
        'loam': {
            'min': 18,
            'max': 33,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B4': {
        'loam': {
            'min': 33,
            'max': 50,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B5': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B6': {
        'loam': {
            'min': 0,
            'max': 50,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    }
}

zavel = {
    'B7': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 8,
            'max': 12,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B8': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 12,
            'max': 18,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B9': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 18,
            'max': 25,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },

}

clay = {
    'B10': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 25,
            'max': 35,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B11': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 35,
            'max': 50,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B12': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 50,
            'max': 100,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },

}
leem = {
    'B13': {
        'loam': {
            'min': 50,
            'max': 85,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
    'B14': {
        'loam': {
            'min': 85,
            'max': 100,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 0,
            'max': 15,
        }
    },
}

moerig = {
    'B15': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 15,
            'max': 25,
        }
    },
    'B16': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 0,
            'max': 8,
        },
        'om': {
            'min': 25,
            'max': 100,
        }
    },
    'B17': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 8,
            'max': 100,
        },
        'om': {
            'min': 16,
            'max': 35,
        }
    },
    'B18': {
        'loam': {
            'min': 0,
            'max': 0,
        },
        'clay': {
            'min': 8,
            'max': 100,
        },
        'om': {
            'min': 35,
            'max': 70,
        }
    },

}

messages = {
    'B1': 'leemarm, zeer fijn tot matig fijn zand (loamy, very fine to moderately fine sand)',
    'B2': 'zwak lemig, zeer fijn tot matig fijn zand (weak loamy, very fine to moderately fine sand)',
    'B3': 'sterk lemig, zeer fijn tot matig fijn zand (very silty, very fine to moderately fine sand)',
    'B4': 'zeer sterk lemig, zeer fijn tot matig fijn zand (very strong loamy, very fine to moderately fine sand)',
    'B5': 'grof zand (coarse sand)',
    'B6': 'keileem (boulder clay)',
    'B7': 'zeer lichte zavel (very light loam)',
    'B8': 'matig lichte zavel (moderately light loam)',
    'B9': 'zware zavel (heavy loam)',
    'B10': 'lichte klei (light clay)',
    'B11': 'matig zware klei (moderately heavy clay)',
    'B12': 'zeer zware klei (very heavy clay)',
    'B13': 'zandige leem (sandy loam)',
    'B14': 'siltige leem (silty loam)',
    'B15': 'venig zand (peaty sand)',
    'B16': 'zandig veen en veen (sandy peat and peat)',
    'B17': 'venige klei (peaty clay)',
    'B18': 'kleiig veen (clayey peat)'
}

generic_text = {
        'B1': 'Leemarm, zeer fijn tot matig fijn zand',
        'B2': 'Zwak lemig, zeer fijn tot matig fijn zand', 
        'B3': 'Sterk lemig, zeer fijn tot matig fijn zand',                
        'B4': 'Zeer sterk lemig, zeer fijn tot matig fijn zand',                
        'B5': 'Grof zand',                
        'B6': 'Keileem',
        'B7': 'Zeer lichte zave',
        'B8': 'Matig lichte zave',
        'B9': 'Zware zave',
        'B10': 'Lichte klei',
        'B11': 'Matig zware klei',
        'B12': 'Zeer zware klei',
        'B13': 'Zandige leem',
        'B14': 'Siltige leem',
        'B15': 'Venig zand',
        'B16': 'Zandig veen en veen',
        'B17': 'Venige kle',
        'B18': 'Kleiig veen'
    }

groups = {
        1280: ['B1', 'B2', 'B3', 'B4', 'B6'],
        1100: ['B5'],
        1000: ['B6'],
        870: ['B7', 'B8', 'B9'],
        650: ['B10', 'B11', 'B12'],
        450: ['B13', 'B14'],
        220: ['B15', 'B16', 'B17', 'B18']
    }
    
def calculateChart(sandParam, siltParam, clayParam, organicMatter):
    data = dict()
    data.update(sand)
    data.update(zavel)
    data.update(clay)
    data.update(leem)
    data.update(moerig)
    selectKey = ''
    loam = float(siltParam) + float(clayParam)
    clayOrSand = False if float(clayParam) >= 0 and float(clayParam) < 8 else True
    peaty = True if float(organicMatter) >= 15 else False

    for key, item in data.items():
        if (key == 'B5' or key == 'B6'):
            continue

        if (clayOrSand==False and peaty == False  and float(loam) >= item['loam']['min'] and float(loam) < item['loam']['max']):
            selectKey = key
            break

        if (clayOrSand and peaty == False and float(clayParam) >= item['clay']['min'] and float(clayParam) < item['clay']['max']):
            selectKey = key
            break

        if (clayOrSand==False and peaty == False and float(loam) >= item['loam']['min'] and float(loam) < item['loam']['max']):
            selectKey = key
            break

        if (not clayOrSand  and peaty and float(organicMatter) >= item['om']['min'] and float(organicMatter) < item['om']['max']):
            selectKey = key
            break

        if (key == 'B17' or key == 'B18'):
            if (clayOrSand  and peaty and float(organicMatter) >= item['om']['min'] and float(organicMatter) < item['om']['max']):
                selectKey = key
                break


    return selectKey


def get_position(b):
    for key, item in groups.items():
        if b in item:
            return key

    return 0
def sheet2():
    return render_template('sheet2.html',
                           data={"sand": sand, "zavel": zavel, "clay": clay, "leem": leem, "moerig": moerig})
