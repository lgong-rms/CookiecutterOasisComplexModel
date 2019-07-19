# -*- coding: utf-8 -*-
import multiprocessing
import os
import shutil
import shutilwhich
import io

import subprocess32 as subprocess

from oasislmf.model_preparation.oed import ALLOCATE_TO_ITEMS_BY_PREVIOUS_LEVEL_ALLOC_ID
from oasislmf.utils.exceptions import OasisException
from oasislmf.utils.log import oasis_log
from oasislmf.model_execution.bash import genbash

RUNTYPE_GROUNDUP_LOSS = 'gul'
RUNTYPE_INSURED_LOSS = 'il'

WAIT_PROCESSING_SWITCHES = {
    'full_uncertainty_aep': '-F',
    'wheatsheaf_aep': '-W',
    'sample_mean_aep': '-S',
    'full_uncertainty_oep': '-f',
    'wheatsheaf_oep': '-w',
    'sample_mean_oep': '-s',
    'wheatsheaf_mean_aep': '-M',
    'wheatsheaf_mean_oep': '-m',
}

def print_command(command_file, cmd):
    """
    Writes the supplied command to the end of the generated script

    :param cmd: The command to append
    """
    with io.open(command_file, "a", encoding='utf-8') as myfile:
        myfile.writelines(cmd + "\n")

def create_workfolders(runtype, analysis_settings, filename):
    summaries = analysis_settings.get('{}_summaries'.format(runtype))
    if not summaries:
        return

    for summary in summaries:
        if 'id' in summary:
            summary_set = summary['id']
            if summary.get('lec_output'):
                print_command(filename, "md work\\{}_S{}_summaryleccalc".format(runtype, summary_set))

            if summary.get('aalcalc'):
                print_command(filename, 'md work\\{}_S{}_summaryaalcalc'.format(runtype, summary_set))


def il(analysis_settings, max_process_id, filename):
    for process_id in range(1, max_process_id + 1):
        do_any(RUNTYPE_INSURED_LOSS, analysis_settings, process_id, filename)

    for process_id in range(1, max_process_id + 1):
        do_summarycalcs(RUNTYPE_INSURED_LOSS, analysis_settings, process_id, filename)

    for process_id in range(1, max_process_id + 1):
        do_tees(RUNTYPE_INSURED_LOSS, analysis_settings, process_id, filename)

    for process_id in range(1, max_process_id + 1):
        do_reps(RUNTYPE_INSURED_LOSS, analysis_settings, process_id, filename)



def do_gul(analysis_settings, max_process_id, filename):
    for process_id in range(1, max_process_id + 1):
        do_any(RUNTYPE_GROUNDUP_LOSS, analysis_settings, process_id, filename)

    for process_id in range(1, max_process_id + 1):
        do_summarycalcs(RUNTYPE_GROUNDUP_LOSS, analysis_settings, process_id, filename)

    for process_id in range(1, max_process_id + 1):
        do_tees(RUNTYPE_GROUNDUP_LOSS, analysis_settings, process_id, filename)

    for process_id in range(1, max_process_id + 1):
        do_reps(RUNTYPE_GROUNDUP_LOSS, analysis_settings, process_id, filename)


def do_any(runtype, analysis_settings, process_id, filename=''):
    summaries = analysis_settings.get('{}_summaries'.format(runtype))
    if not summaries:
        return

    for summary in summaries:
        if 'id' in summary:
            summary_set = summary['id']

            if summary.get("summarycalc"):
                cmd = 'summarycalctocsv -s'
                if process_id == 1:
                    cmd = 'summarycalctocsv'

                print_command(
                    filename,
                    '{3} < fifo\\{0}_S{1}_summarysummarycalc_P{2} > work\\kat\\{0}_S{1}_summarycalc_P{2}'.format(
                        runtype, summary_set, process_id, cmd
                    )
                )

        print_command(filename, '')


def do_reps(runtype, analysis_settings, process_id, filename=''):
    summaries = analysis_settings.get('{}_summaries'.format(runtype))
    if not summaries:
        return

    for summary in summaries:
        if 'id' in summary:
            summary_set = summary['id']
            if summary.get('eltcalc'):
                cmd = 'eltcalc -s'
                if process_id == 1:
                    cmd = 'eltcalc'

                print_command(
                    filename,
                    "{3} < fifo\\{0}_S{1}_summaryeltcalc_P{2} > work\\kat\\{0}_S{1}_eltcalc_P{2}".format(
                        runtype, summary_set, process_id, cmd
                    )
                )

            if summary.get('pltcalc'):
                cmd = 'pltcalc -s'
                if process_id == 1:
                    cmd = 'pltcalc'

                print_command(
                    filename,
                    '{3} < fifo\\{0}_S{1}_summarypltcalc_P{2} > work\\kat\\{0}_S{1}_pltcalc_P{2}'.format(
                        runtype, summary_set, process_id, cmd
                    )
                )

        print_command(filename, '')


def do_summarycalcs(runtype, analysis_settings, process_id, filename):

    summaries = analysis_settings.get('{}_summaries'.format(runtype))
    if not summaries:
        return

    summarycalc_switch = '-f'
    if runtype == RUNTYPE_GROUNDUP_LOSS:
        summarycalc_switch = '-g'

    summarycalc_directory_switch = ""

    cmd = 'summarycalc {} {}'.format(summarycalc_switch, summarycalc_directory_switch)
    for summary in summaries:
        if 'id' in summary:
            summary_set = summary['id']
            cmd = '{0} -{1} fifo\\{2}_S{1}_summary_P{3}'.format(cmd, summary_set, runtype, process_id)

    cmd = '{0} < {1}fifo\\{2}_P{3}'.format(cmd, '', runtype, process_id)
    print_command(filename, cmd)



def do_tees(runtype, analysis_settings, process_id, filename):
    summaries = analysis_settings.get('{}_summaries'.format(runtype))
    if not summaries:
        return

    for summary in summaries:
        if 'id' in summary:
            summary_set = summary['id']
            cmd = 'copy fifo\\{}_S{}_summary_P{}'.format(runtype, summary_set, process_id)

            if summary.get('eltcalc'):
                c = '{} fifo\\{}_S{}_summaryeltcalc_P{}'.format(cmd, runtype, summary_set, process_id)
                print_command(filename, c)

            if summary.get('pltcalc'):
                c = '{} fifo\\{}_S{}_summarypltcalc_P{}'.format(cmd, runtype, summary_set, process_id)
                print_command(filename, c)

            if summary.get('summarycalc'):
                c = '{} fifo\\{}_S{}_summarysummarycalc_P{}'.format(cmd, runtype, summary_set, process_id)
                print_command(filename, c)

            if summary.get('aalcalc'):
                c = '{} work\\{}_S{}_summaryaalcalc\\P{}.bin'.format(cmd, runtype, summary_set, process_id)
                print_command(filename, c)

            if summary.get('lec_output'):
                c = '{} work\\{}_S{}_summaryleccalc\\P{}.bin'.format(cmd, runtype, summary_set, process_id)
                print_command(filename, c)

            print_command(filename, '')


def run_batch(
    max_process_id,
    analysis_settings,
    num_reinsurance_iterations,
    fifo_tmp_dir,
    mem_limit,
    alloc_rule,
    filename,
    _get_getmodel_cmd,
    custom_args={}
):
    # remove the file if it already exists
    if os.path.exists(filename):
        os.remove(filename)

    aux_file, _ = os.path.splitext(filename)
    aux_file += ".txt"
    if os.path.exists(aux_file):
        os.remove(aux_file)

    print_command(filename, 'md work\\kat')
    gul_threshold = analysis_settings.get('gul_threshold', 0)
    number_of_samples = analysis_settings.get('number_of_samples', 0)

    use_random_number_file = ''
    if 'model_settings' in analysis_settings and analysis_settings['model_settings'].get('use_random_number_file'):
        use_random_number_file = '123'

    if 'gul_output' in analysis_settings:
        gul_output = analysis_settings['gul_output']
        create_workfolders(RUNTYPE_GROUNDUP_LOSS, analysis_settings, filename)

    if 'il_output' in analysis_settings:
        il_output = analysis_settings['il_output']
        create_workfolders(RUNTYPE_INSURED_LOSS, analysis_settings, filename)

    for process_id in range(1, max_process_id + 1):
        if gul_output and il_output:
            getmodel_args = {
                'number_of_samples'      : number_of_samples,
                'gul_threshold'          : gul_threshold,
                'use_random_number_file' : use_random_number_file,
                'coverage_output'        : '{}fifo\\gul_P{}'.format("", process_id),
                'item_output'            : '-',
                'process_id'             : process_id,
                'max_process_id'         : max_process_id
            }
            getmodel_cmd = _get_getmodel_cmd(**getmodel_args)
            main_cmd = '{1} | fmcalc -a {2} > {3}fifo\\il_P{0} '.format(
                process_id, getmodel_cmd,
                alloc_rule,
                "")
            print_command(aux_file, main_cmd)
        else:
            if gul_output and 'gul_summaries' in analysis_settings:
                getmodel_args = {
                    'number_of_samples'      : number_of_samples,
                    'gul_threshold'          : gul_threshold,
                    'use_random_number_file' : use_random_number_file,
                    'coverage_output'        : '{}fifo\\gul_P{}'.format("", process_id),
                    'item_output'            : '',
                    'process_id'             : process_id,
                    'max_process_id'         : max_process_id
                }
                main_cmd = _get_getmodel_cmd(**getmodel_args)
                print_command(aux_file, main_cmd)

            if il_output  and 'il_summaries' in analysis_settings:
                getmodel_args = {
                    'number_of_samples'      : number_of_samples,
                    'gul_threshold'          : gul_threshold,
                    'use_random_number_file' : use_random_number_file,
                    'coverage_output'        : '',
                    'item_output'            : '-',
                    'process_id'             : process_id,
                    'max_process_id'         : max_process_id
                }
                getmodel_cmd = _get_getmodel_cmd(**getmodel_args)
                main_cmd = '{1} | fmcalc -a {2} > {3}fifo\\il_P{0} '.format(
                    process_id, getmodel_cmd,
                    alloc_rule,
                    "")
                print_command(aux_file, main_cmd)

    print_command(filename, 'rush {} < ' + aux_file)
    print_command(filename, '')

    if gul_output:
        print_command(filename, '')
        print_command(filename, 'REM --- Do ground up loss computes ---')
        print_command(filename, '')
        do_gul(analysis_settings, max_process_id, filename)

    if il_output:
        print_command(filename, '')
        print_command(filename, 'REM --- Do insured loss computes ---')
        print_command(filename, '')
        il(analysis_settings, max_process_id, filename)

    do_post_wait_processing(RUNTYPE_INSURED_LOSS, analysis_settings, filename)
    do_post_wait_processing(RUNTYPE_GROUNDUP_LOSS, analysis_settings, filename)

    if il_output:
        print_command(filename, '')
        print_command(filename, 'REM --- Do insured loss kats ---')
        print_command(filename, '')
        do_kats(RUNTYPE_INSURED_LOSS, analysis_settings, max_process_id, filename)

    if gul_output:
        print_command(filename, '')
        print_command(filename, 'REM --- Do ground up loss kats ---')
        print_command(filename, '')
        do_kats(RUNTYPE_GROUNDUP_LOSS, analysis_settings, max_process_id, filename)



def do_post_wait_processing(runtype, analysis_settings, filename):
    if '{}_summaries'.format(runtype) not in analysis_settings:
        return

    for summary in analysis_settings['{}_summaries'.format(runtype)]:
        if "id" in summary:
            summary_set = summary['id']
            if summary.get('aalcalc'):
                cmd = 'aalcalc -K{}_S{}_summaryaalcalc'.format(
                    runtype,
                    summary_set
                )

                cmd = '{} > output\\{}_S{}_aalcalc.csv'.format(cmd, runtype, summary_set)
                print_command(filename, cmd)

            if summary.get('lec_output'):
                leccalc = summary.get('leccalc', {})
                cmd = 'leccalc {} -K{}_S{}_summaryleccalc'.format(
                    '-r' if leccalc.get('return_period_file') else '',
                    runtype,
                    summary_set
                )

                for option, active in sorted(leccalc['outputs'].items()):
                    if active:
                        switch = WAIT_PROCESSING_SWITCHES.get(option, '')
                        cmd = '{} {} output/{}_S{}_leccalc_{}.csv'.format(cmd, switch, runtype, summary_set,
                                                                            option)

                print_command(filename, cmd)

def do_kats(runtype, analysis_settings, max_process_id, filename):
    summaries = analysis_settings.get('{}_summaries'.format(runtype))
    if not summaries:
        return False

    anykats = False
    for summary in summaries:
        if 'id' in summary:
            summary_set = summary['id']

            if summary.get('eltcalc'):
                anykats = True

                cmd = 'kat'
                for process_id in range(1, max_process_id + 1):
                    cmd = '{} work/kat/{}_S{}_eltcalc_P{}'.format(cmd, runtype, summary_set, process_id)

                cmd = '{} > output/{}_S{}_eltcalc.csv'.format(cmd, runtype, summary_set)
                print_command(filename, cmd)

            if summary.get('pltcalc'):
                anykats = True

                cmd = 'kat'
                for process_id in range(1, max_process_id + 1):
                    cmd = '{} work/kat/{}_S{}_pltcalc_P{}'.format(cmd, runtype, summary_set, process_id)

                cmd = '{} > output/{}_S{}_pltcalc.csv'.format(cmd, runtype, summary_set)
                print_command(filename, cmd)

            if summary.get("summarycalc"):
                anykats = True

                cmd = 'kat'
                for process_id in range(1, max_process_id + 1):
                    cmd = '{} work/kat/{}_S{}_summarycalc_P{}'.format(cmd, runtype, summary_set, process_id)

                cmd = '{} > output/{}_S{}_summarycalc.csv'.format(cmd, runtype, summary_set)
                print_command(filename, cmd)

    return anykats


@oasis_log()
def run(
    analysis_settings,
    number_of_processes=-1,
    num_reinsurance_iterations=0,
    ktools_mem_limit=False,
    set_alloc_rule=ALLOCATE_TO_ITEMS_BY_PREVIOUS_LEVEL_ALLOC_ID,
    fifo_tmp_dir=True,
    run_debug=None,
    filename='run_ktools.sh'
):
    if os.name == 'nt':
        filename = 'run_ktools.bat'

    if number_of_processes == -1:
        number_of_processes = multiprocessing.cpu_count()

    custom_gulcalc_cmd = "EarthquakeDamage"

    # Check for custom gulcalc
    if shutil.which(custom_gulcalc_cmd):

        def custom_get_getmodel_cmd(
            number_of_samples,
            gul_threshold,
            use_random_number_file,
            coverage_output,
            item_output,
            process_id,
            max_process_id,
            **kwargs):

            cmd = "{} -m {} -n {} -a {} -p {} -S{}".format(
                custom_gulcalc_cmd,
                process_id,
                max_process_id,
                os.path.abspath("analysis_settings.json"),
                ".",
                number_of_samples)
            if coverage_output != '':
                cmd = '{} -c {}'.format(cmd, coverage_output)
            if item_output != '':
                cmd = '{} -i {}'.format(cmd, item_output)

            return cmd


        if os.name == 'nt':
            run_batch(
                number_of_processes,
                analysis_settings,
                num_reinsurance_iterations=num_reinsurance_iterations,
                fifo_tmp_dir=fifo_tmp_dir,
                mem_limit=ktools_mem_limit,
                alloc_rule=set_alloc_rule,
                filename=filename,
                _get_getmodel_cmd=custom_get_getmodel_cmd,
            )
        else:
            genbash(
                number_of_processes,
                analysis_settings,
                num_reinsurance_iterations=num_reinsurance_iterations,
                fifo_tmp_dir=fifo_tmp_dir,
                mem_limit=ktools_mem_limit,
                alloc_rule=set_alloc_rule,
                filename=filename,
                _get_getmodel_cmd=custom_get_getmodel_cmd,
            )
    else:
        genbash(
            number_of_processes,
            analysis_settings,
            num_reinsurance_iterations=num_reinsurance_iterations,
            fifo_tmp_dir=fifo_tmp_dir,
            mem_limit=ktools_mem_limit,
            alloc_rule=set_alloc_rule,
            filename=filename
        )

    try:

        if os.name != 'nt':
            subprocess.check_call(['bash', filename])
        else:
            subprocess.check_call([filename])
    except subprocess.CalledProcessError as e:
        raise OasisException('Error running ktools: {}'.format(str(e)))
