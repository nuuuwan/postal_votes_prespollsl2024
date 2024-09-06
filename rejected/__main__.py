import os

from gig import Ent, EntType, GIGTable
from utils import Log, TSVFile

log = Log('aggregates')


def parse_int(x):
    return int(round(float(x)))


def get_p_rejected(d):
    return parse_int(d['rejected']) / parse_int(d['polled'])


def get_d_postal(gig_table):
    d = {}
    for ed in ed_list:
        postal_pd_id = ed.id + "P"

        try:
            data_postal = gig_table.get(postal_pd_id).d
        except KeyError:
            continue

        for k, v in data_postal.items():
            if k in ['entity_id']:
                continue
            if k not in d:
                d[k] = 0
            d[k] += parse_int(v)
    return d


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

ed_list = Ent.list_from_type(EntType.ED)
d_list = []

for year in years:
    gig_table = GIGTable(
        f'government-elections-{category}', 'regions-ec', year
    )

    data_lk = gig_table.get('LK').d
    p_rejected_lk = get_p_rejected(data_lk)

    data_postal = get_d_postal(gig_table)
    p_rejected_postal = get_p_rejected(data_postal)

    d = {
        'year': year,
        '% Rejected (All)': p_rejected_lk,
        '% Rejected (Postal)': p_rejected_postal,
    }
    d_list.append(d)


data_path = os.path.join('rejected', 'data.tsv')
TSVFile(data_path).write(d_list)
log.info(f'Wrote  {data_path}')
os.startfile(data_path)
