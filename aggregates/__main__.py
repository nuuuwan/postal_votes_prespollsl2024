import os

from gig import Ent, EntType, GIGTable
from utils import Log, TSVFile

log = Log('aggregates')

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
d_list = []
for year in years:
    gig_table = GIGTable(
        f'government-elections-{category}', 'regions-ec', year
    )
    ents = Ent.list_from_type(EntType.PD)
    total_valid_postal = 0
    total_valid = 0
    n = 0
    n_postal = 0
    for id, data in gig_table.remote_data_idx.items():
        if not (id.startswith('EC-') and len(id) == 6):
            continue

        pd_id = id
        is_postal = pd_id.endswith('P')

        row = gig_table.get(pd_id)
        valid = int(round(float(data['valid'])))

        n += 1
        total_valid += valid
        if is_postal:
            n_postal += 1
            total_valid_postal += valid
    p_postal = total_valid_postal / total_valid
    d = dict(
        year=year,
        n=n,
        n_postal=n_postal,
        total_valid=total_valid,
        total_valid_postal=total_valid_postal,
        p_postal=p_postal,
    )
    d_list.append(d)

data_path = os.path.join('aggregates', 'data.tsv')
TSVFile(data_path).write(d_list)
log.info(f'Wrote  {data_path}')
