import os
import time
import json

from ImaerPlugin.tasks import ImportImaerCalculatorResultTask

'''plugin_dir = imaer_plugin.plugin_dir
sys.path.append(plugin_dir)
from ImaerPlugin.tasks import ImportImaerCalculatorResultTask
'''

class CalculationJob():

    def __init__(self, gml_files, user_options, name=None):
        self.gml_files = gml_files
        self.user_options = user_options
        self.name = name
        self.status = 'new'
        self.job_key = None

    def __str__(self):
        return f'CalculationJob[status: {self.status}, key: {self.job_key}, {self.name}]'


class AeriusConnectManager():

    def __init__(self, imaer_plugin):
        self.imaer_plugin = imaer_plugin
        self.jobs = []
        self.interval = 10  # seconds interval
        self.timeout = 180  # seconds
        self.connection = imaer_plugin.aerius_connection

    def __str__(self):
        return 'AeriusConnectManager[jobs: {0}]'.format(len(self.jobs))

    def print_jobs(self):
        for job in self.jobs:
            print(f'* {job}')

    def add_job(self, gml_files, user_options, name=None):
        calc = CalculationJob(gml_files, user_options, name)
        self.jobs.append(calc)

    def delete_server_jobs(self):
        server_jobs = self.__get_server_jobs()
        #print(server_jobs)
        print(f'Deleting all {len(server_jobs)} existing server jobs')
        for job in server_jobs:
            self.connection.delete_job(job['jobKey'])

    def run(self):
        self.running = True
        self.last_start_time = time.time()
        while self.running:
            print('--- Next iteration ---')
            print(self)
            self.print_jobs()

            server_jobs = self.__get_server_jobs()
            stats = self.__get_server_stats(server_jobs)
            print(stats)

            # Todo check
            if self.__is_finished():
                self.running = False
                continue

            # Timeout check
            print(time.time() - self.last_start_time)
            if time.time() - self.last_start_time > self.timeout:
                self.running = False
                continue

            # Start job
            if stats.get('RUNNING', 0) < 6:
                self.__start_job()

            # Start download
            self.__download_job()

            self.__update_job_statuses()

            time.sleep(self.interval)

    def __get_job_by_status(self, status):
        for job in self.jobs:
            if job.status == status:
                return job

    def __get_job_by_key(self, job_key):
        for job in self.jobs:
            if job.job_key == job_key:
                return job

    def __is_finished(self):
        for job in self.jobs:
            if job.status not in ['finished', 'failed']:
                return False
        return True

    def __start_job(self, job=None):
        if job is None:
            job = self.__get_job_by_status('new')
        if job is not None:
            response = self.connection.post_calculate(job.gml_files, job.user_options)
            bstr = response.readAll()
            result_dict = json.loads(bytes(bstr))
            print('# job check:')
            print(result_dict)
            if 'jobKey' in result_dict:
                print('# job started')
                job.job_key = result_dict['jobKey']
                job.status = 'running'
                self.last_start_time = time.time()
            elif 'error' in result_dict and result_dict['error'] == 'Bad Request':
                print('# job error')
                job.status = 'failed'
                # TODO: write to log file?
            elif 'successful' in result_dict and result_dict['successful'] == False:
                print('# job not successful')
                print('not successful')
                job.status = 'failed'
                # TODO: write to log file
            else:
                print('# job else ???')

    def __update_job_statuses(self, server_jobs=None):
        if server_jobs is None:
            server_jobs = self.__get_server_jobs()
        for server_job in server_jobs:
            print(server_job)
            if server_job['status'] == 'COMPLETED':
                print(server_job['jobKey'])
                job = self.__get_job_by_key(server_job['jobKey'])
                print(job)
                if job is None:
                    continue
                if job.status == 'running':
                    job.status = 'completed'
                    job.result_url = server_job['resultUrl']


    def __download_job(self, job=None):
        if job is None:
            job = self.__get_job_by_status('completed')
        # download job
        if job is not None:
            print('download job')
            for gml_file in job.gml_files:
                print(gml_file['gml_fn'])
                gml_path = os.path.dirname(gml_file['gml_fn'])
                print(gml_path)
                response = self.connection.download_result_zip(job.result_url, gml_path, job.name)
                job.status = 'downloading'
                print(response)
                for result_gml_fn in response:
                    self.__gml_to_gpkg(result_gml_fn)
                job.status = 'finished' # tmp!

    def __gml_to_gpkg(self, gml_fn):
        gpkg_fn = gml_fn.replace('.gml', '.gpkg')  # TODO
        def dummy_callback(gpkg_fn, feat_cnt, rp_without_geom_cnt=-1):
            pass
        task = ImportImaerCalculatorResultTask(gml_fn, gpkg_fn, dummy_callback)
        task_result = self.imaer_plugin.task_manager.addTask(task)
        print(task_result)

    def __get_server_jobs(self):
        server_jobs = self.connection.get_jobs()
        return server_jobs

    def __get_server_stats(self, jobs):
        result = {}
        for job in jobs:
            if job['status'] in result:
                result[job['status']] += 1
            else:
                result[job['status']] = 1
        result['TOTAL'] = len(jobs)
        return result
