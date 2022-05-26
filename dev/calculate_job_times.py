"""Module to calculate average job times

Author: Matthias van den Belt
"""
import datetime


def main():

    # if m.Statistic.query.filter_by(name="finished").first() is None:
    #     stats = [m.Statistic(name="finished"),
    #              m.Statistic(name="failed")]
    # iterate over entries
    total_skipped = 0
    all_deltas = {}

    for entry in everything.split('\n'):
        splitted = entry.split('\t')
        # for i, val in enumerate(splitted):

        job_type = splitted[job_type_index]
        job_status = splitted[job_status_index]
        start_time = splitted[start_index]
        stop_time = splitted[stop_index]

        # skip failed jobs / jobs without finished time
        if job_status != 'finished' or stop_time == 'null' or stop_time == '':

            datetime.datetime.now()
            total_skipped += 1
            continue

        # print(entry)
        # print(start_time)
        # print(stop_time)
        # exit()

        # calculate timedelta between start and finish time
        start_time = datetime.datetime.strptime(start_time, pattern)
        stop_time = datetime.datetime.strptime(stop_time, pattern)
        delta = stop_time - start_time

        if job_type == 'search' and delta < datetime.timedelta(minutes=1):
            job_type = 'recompute'

        if job_type not in all_deltas:
            all_deltas[job_type] = [delta]
        else:
            all_deltas[job_type].append(delta)
        # all_deltas.append(delta)  # TODO
    print(all_deltas)
    # calculate average over all jobs

    for job_type, deltas in all_deltas.items():

        average_timedelta = sum(deltas, datetime.timedelta(0)) / len(deltas)

    # average_timedelta = 2
        print(job_type, 'average time:', average_timedelta, f'({len(deltas)} entries)')
        # print('With', len(deltas), 'entries')

    # print('We skipped', total_skipped, 'entries')

            # print(i, val)

        # exit()
        # print(entry)

    # TODO: calculate average time per job type

if __name__ == '__main__':
    # 0 Z245X621C756D63
    # 1 search
    # 2 7be275a7-c1e5-4dc7-8c49-c51f33f84d54
    # 3 failed
    # 4 hirsutella
    # 5 cameron.gilchrist@research.uwa.edu.au
    # 6 null
    # 7
    # 8 null
    # 9 2021-06-24 09:02:46.122746
    # 10 2021-06-24 09:02:46.486771
    # 11 2021-06-24 09:04:21.334904

    # 2021-07-14 06:33:27.843877
    pattern = '%Y-%m-%d %H:%M:%S.%f'

    job_type_index = 1
    job_status_index = 3
    start_index = 10
    stop_index = 11

    everything = """Q379W565R078L81	search	0775a073-7c18-46a2-874f-890581e9d9de	finished		removed_mailadress	null		null	2021-08-06 05:11:01.578397	2021-08-06 05:11:01.851846	2021-08-06 05:12:50.121125"""

    main()
