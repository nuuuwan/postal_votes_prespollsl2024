import os

from gig import Ent, EntType, GIGTable
from utils import Log, TSVFile

log = Log('aggregates')


def clean(d):
    return dict(
        sorted(
            [
                (k, float(v))
                for k, v in d.items()
                if k
                not in [
                    'entity_id',
                    'valid',
                    'rejected',
                    'polled',
                    'electors',
                ]
            ],
            key=lambda x: x[1],
            reverse=True,
        )
    )


def get_winner(d):
    d = clean(d)
    return list(d.keys())[0]


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

ed_list = Ent.list_from_type(EntType.ED)
ed_to_n_matches = {}
ed_to_n = {}
for year in years:
    gig_table = GIGTable(
        f'government-elections-{category}', 'regions-ec', year
    )

    data_lk = gig_table.get('LK').d
    winner_lk = get_winner(data_lk)

    ents = Ent.list_from_type(EntType.PD)
    postal_rows = []
    all_rows = []
    for ed in ed_list:
        postal_pd_id = ed.id + "P"
        ed_name = ed.name

        if ed_name not in ed_to_n_matches:
            ed_to_n_matches[ed_name] = 0
            ed_to_n[ed_name] = 0

        try:
            data_postal = gig_table.get(postal_pd_id).d
        except KeyError:
            continue
        ed_to_n[ed_name] += 1
        winner = get_winner(data_postal)

        if winner == winner_lk:
            ed_to_n_matches[ed_name] += 1

d_list = []
for ed_name, n in ed_to_n.items():
    n_matches = ed_to_n_matches[ed_name]
    d_list.append(
        {
            "Electoral District": ed_name,
            'nElections': n,
            'nMatches': n_matches,
            'pMatches': n_matches / n,
        }
    )

d_list.sort(key=lambda x: (x['pMatches'], x['nMatches']), reverse=True)


data_path = os.path.join('bellwether', 'data.tsv')
TSVFile(data_path).write(d_list)
log.info(f'Wrote  {data_path}')
os.startfile(data_path)
