module_mapper = {
    'cargobay':'Cargo Bay Extension',
    'computer':'Shipment Computer',
    'tradeboost':'Trade Boost',
    'rush':'Rush',
    'tradeburst':'Trade Burst',
    'shipdrone':'Shipment Drone',
    'offload':'Offload',
    'beam':'Shipment Beam',
    'entrust':'Entrust',
    'recall':'Recall',
    'dispatch':'Dispatch',
    'miningboost':'Mining Boost',
    'hydrobay':'Hydrogen Bay Expansion',
    'enrich':'Enrich',
    'remote':'Remote Mining',
    'hydroupload':'Hydrogen Upload',
    'miningunity':'Mining Unity',
    'crunch':'Crunch',
    'genesis':'Genesis',
    'minedrone':'Mining Drone',
    'hydrorocket':'Hydrogen Rocket',
    'weak':'Weak Battery',
    'battery':'Battery',
    'laser':'Laser',
    'mass':'Mass Battery',
    'dual':'Dual Laser',
    'barrage':'Barrage',
    'dart':'DART',
    'alpha':'Alpha',
    'delta':'Delta',
    'passive':'Passive',
    'omega':'Omega',
    'mirror':'Mirror',
    'blast':'Blast',
    'area':'Area',
    'emp':'EMP',
    'teleport':'Teleport',
    'rsextender':'RSLE',
    'repair':'Remote Repair',
    'warp':'Time Warp',
    'unity':'Unity',
    'sanctuary':'Sanctuary',
    'stealth':'Stealth',
    'fortify':'Fortify',
    'impulse':'Impulse',
    'rocket':'Alpha Rocket',
    'salvage':'Salvage',
    'suppress':'Suppress',
    'destiny':'Destiny',
    'barrier':'Barrier',
    'vengeance':'Vengeance',
    'deltarocket':'Delta Rocket',
    'leap':'Leap',
    'bond':'Bond',
    'alphadrone':'Alpha Drone',
    'suspend':'Suspend',
    'omegarocket':'Omega Rocket',
    'remotebomb':'Remote Bomb',
}


def set_weapons(compendium, loadout, **kwargs):
    done = []
    for idx, role in compendium['Roles'].items():
        if role == 'zookeeper':
            done.append(idx)
            loadout.at[idx, 'weapon'] = 'DART'
            done.append(idx)

    for idx, row in compendium.iterrows():
        if idx in done:
            continue
        w = row.loc['weak':'dart'].astype(int).idxmax()
        loadout.at[idx, 'weapon'] = module_mapper[w]


def set_shields(compendium, loadout, **kwargs):
    blast_shields_count = kwargs.get('blast', 0)
    area_shields_count = kwargs.get('area', 0)

    done = []

    blast_shields = compendium['blast']
    area_shields = compendium['area']

    for idx, role in compendium['Roles'].items():
        if role == 'raider':
            done.append(idx)
            loadout.at[idx, 'shield'] = 'Delta'

    top_blast_shields = compendium['blast'].sort_values(ascending=False)
    if blast_shields_count:
        for idx, tbs in top_blast_shields.items():
            if idx in done:
                continue
            loadout.at[idx, 'shield'] = 'Blast'
            done.append(idx)
            blast_shields_count -= 1
            if (blast_shields_count == 0): break

    top_area_shields = compendium['area'].sort_values(ascending=False)
    if area_shields_count:
        for idx, tbs in top_area_shields.items():
            if idx in done:
                continue
            loadout.at[idx, 'shield'] = 'Area'
            done.append(idx)
            area_shields_count -= 1
            if (area_shields_count == 0): break

    loadout['shield'].replace('', 'Omega', inplace=True) 


def set_supports(compendium, loadout, **kwargs):
    zookeeper_available = 'zookeeper' in compendium['Roles'].values

    done = []

    for idx, row in compendium.iterrows():
        bsl = row['bs']
        if row['Roles'] == 'raider':
            loadout.at[idx, 'support_1'] = 'Teleport'
            loadout.at[idx, 'support_2'] = 'Time Warp'
            loadout.at[idx, 'support_3'] = 'Destiny'
            loadout.at[idx, 'support_4'] = 'Leap' if zookeeper_available else 'Impulse'
            loadout.at[idx, 'support_5'] = 'Bond' if bsl == 6 else ''
            done.append(idx)

        elif row['Roles'] == 'zookeeper':
            loadout.at[idx, 'support_1'] = 'Teleport'
            loadout.at[idx, 'support_2'] = 'Barrier'
            loadout.at[idx, 'support_3'] = 'Bond'
            loadout.at[idx, 'support_4'] = 'Impulse'
            loadout.at[idx, 'support_5'] = 'Suspend' if bsl == 6 else ''
            done.append(idx)

    support_modules = w = row.loc['emp':'remotebomb']
    for module, count in kwargs.items():
        top = compendium[module].sort_values(ascending=False)
        for idx, t in top.items():
            if idx in done:
                continue

            key = 'support_1'
            while (loadout.at[idx, key] != ''):
                key = f'support_{int(key.split("_")[1]) + 1}'

            loadout.at[idx, key] = module_mapper[module]

            if key == 'support_5' or (key == 'support_4'  and compendium.at[idx, 'bs'] < 6):
                done.append(idx)
            
            count -= 1
            if (count == 0): break


    for idx, player in loadout.iterrows():
        if player['support_1'] == '': print(f'{idx} missing support_1')
        if player['support_2'] == '': print(f'{idx} missing support_2')
        if player['support_3'] == '': print(f'{idx} missing support_3')
        if player['support_4'] == '': print(f'{idx} missing support_4')
        if player['support_5'] == '' and compendium.at[idx, 'bs'] == 6: print(f'{idx} missing support_5')

