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

    postal_rows = []
    all_rows = []
    for id, data in gig_table.remote_data_idx.items():
        if not (id.startswith('EC-') and len(id) == 6):
            continue

        pd_id = id
        is_postal = pd_id.endswith('P')

        row = gig_table.get(pd_id)
        all_rows.append(row)
        if is_postal:
            postal_rows.append(row)

    d_all = {}
    for row in all_rows:
        for k, v in row.dict.items():
            if k in ['electors', 'polled', 'rejected', 'valid']:
                continue
            if k not in d_all:
                d_all[k] = 0
            d_all[k] += v

    d_postal = {}
    for row in postal_rows:
        for k, v in row.dict.items():
            if k in ['electors', 'polled', 'rejected', 'valid']:
                continue
            if k not in d_postal:
                d_postal[k] = 0
            d_postal[k] += v

    winner_all = max(d_all, key=d_all.get)
    p_winner_all = d_all[winner_all] / sum(d_all.values())
    p_winner_all_postal = d_postal[winner_all] / sum(d_postal.values())
    winner_postal = max(d_postal, key=d_postal.get)

    d = dict(
        year=year,
        winner_all=winner_all,
        p_winner_all=p_winner_all,
        p_winner_all_postal=p_winner_all_postal,
        winner_postal=winner_postal,
    )
    print(d)

    d_list.append(d)


data_path = os.path.join('candidate', 'data.tsv')
TSVFile(data_path).write(d_list)
log.info(f'Wrote  {data_path}')
