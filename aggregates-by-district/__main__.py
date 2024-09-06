import os

from gig import Ent, EntType, GIGTable
from utils import Log, TSVFile

log = Log('aggregates')

ed_idx = Ent.idx_from_type(EntType.ED)

years = [
    '1982',
    '1988',
    '1994',
    '1999',
    '2005',
    '2010',
    '2015',
    '2019',
]
category = 'presidential'
ed_to_year_to_p_postal = {}
for year in years:
    gig_table = GIGTable(
        f'government-elections-{category}', 'regions-ec', year
    )
    ents = Ent.list_from_type(EntType.PD)
    ed_to_valid = {}
    ed_to_postal_valid = {}
    for id, data in gig_table.remote_data_idx.items():
        if not (id.startswith('EC-') and len(id) == 6):
            continue

        ed_id = id[:-1]
        is_postal = id.endswith('P')

        valid = int(round(float(data['valid'])))
        if ed_id not in ed_to_valid:
            ed_to_valid[ed_id] = 0
        ed_to_valid[ed_id] += valid
        if is_postal:
            if ed_id not in ed_to_postal_valid:
                ed_to_postal_valid[ed_id] = 0
            ed_to_postal_valid[ed_id] += valid

    for ed_id in ed_to_valid:
        all_valid = ed_to_valid[ed_id]
        postal_valid = ed_to_postal_valid.get(ed_id, 0)
        ed_name = ed_idx[ed_id].name

        p_postal = postal_valid / all_valid

        if ed_name not in ed_to_year_to_p_postal:
            ed_to_year_to_p_postal[ed_name] = {}
        ed_to_year_to_p_postal[ed_name][year] = p_postal

d_list = []
for ed_name in ed_to_year_to_p_postal:
    d = dict(
        ed_name=ed_name,
    )
    for year in years:
        d[year] = ed_to_year_to_p_postal[ed_name].get(year, '')
    d_list.append(d)

data_path = os.path.join('bellwether', 'data.tsv')
TSVFile(data_path).write(d_list)
log.info(f'Wrote  {data_path}')
os.startfile(data_path)
