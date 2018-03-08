from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import traceback
from datetime import datetime

from tqdm import tqdm

from setting_logger import Logger


class Pachong(object):

    tasks_available = []

    def __init__(self, project, input_, output='', fetcher=None, Database=None, batch=100, machine=0):
        self.batch = batch
        self.machine = machine
        self.project = project
        self.Database = Database
        self.input_ = input_
        self.output = output
        self.fetcher = fetcher
        self.logger = Logger(project + '_' + (input_ if self.input_ is self.output else output) + '.log')

    def crawl(self, task, *args, **kwargs):
        self.task = task
        print('Starting task: {}'.format(task))
        while True:
            samples = self.sample_input(self.batch, self.batch * self.machine)
            if not samples:
                break
            with tqdm(samples) as bar:
                for target in bar:
                    target_id = target['_id']
                    self.input_.update(target_id, {'task.{}.status'.format(task): 'running'})
                    self.input_.drop_field(target_id, 'task.{}.traceback'.format(self.task))
                    bar.set_description(target_id)
                    try:
                        if self.input_ is self.output:
                            [self.output.update(target_id, chong)
                             for chong in eval('self.{}(target_id, *args, **kwargs)'.format(self.task))
                             if chong]
                        else:
                            [self.output.insert(chong)
                             for chong in eval('self.{}(target_id, *args, **kwargs)'.format(self.task))
                             if chong]
                        self.logger.push('DATABASE', '{} is done.'.format(target_id))
                        self.input_.update(target_id, {'task.{}.status'.format(self.task): 'done'})
                    except Exception:
                        self.traceback = traceback.format_exc()
                        self.input_.update(target_id, {'task.{}.status'.format(self.task): 'error',
                                                       'task.{}.traceback'.format(self.task): self.traceback})
        return self

    def import_input(self, filepath=None, input_list=None, update=False):
        if not update and self.input_.collection.name in set(self.output.db.collection_names()):
            self.logger.push('DATABASE', 'Input already exists.')
            return self

        if filepath:
            with open(filepath, 'r') as i:
                input_list = {line.strip() for line in i if line.strip()}
        import_count = len([self.input_.insert(target_id) for target_id in input_list])
        self.logger.push('DATABASE', 'Imported {} inputs to crawl.'.format(import_count))
        return self

    def captcha_handler(self):
        raise LookupError

    def sample_input(self, n_sample, skip):
        cursor = self.input_.find_all({'task.{}.status'.format(self.task): {'$nin': ['done', 'progress']}})
        return list(cursor.skip(skip).limit(n_sample))
    # def get_input(self):
    #     return [tar['_id'] for tar in self.input_.find({'done': {'$ne': 1}}, fields=['_id'])]

    @staticmethod
    def utc_now():
        return (datetime.now() - datetime(1970, 1, 1)).total_seconds()

    @property
    def input_(self):
        return self._input_

    @input_.setter
    def input_(self, val):
        if val == '':
            raise AttributeError('Input name is required')
        self._input_ = self.Database(self.project, val)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, val):
        if val == '':
            raise AttributeError('Input name is required')
        self._profile = self.Database(self.project, val)

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, val):
        self._output = self.input_ if not val else self.Database(self.project, val)
        self.logger = Logger(self.project + '_' +
                             (self.input_.collection.name if self.input_ is self.output
                              else self.output.collection.name) + '.log')
    @property
    def fetcher(self):
        return self._fetcher

    @fetcher.setter
    def fetcher(self, val):
        if val is None:
            raise AttributeError('Fetcher is NoneType')
        self._fetcher = val

    @property
    def Database(self):
        return self._Database

    @Database.setter
    def Database(self, val):
        if val is None:
            raise AttributeError('Database is NoneType')
        self._Database = val

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, val):
        if val not in self.tasks_available:
            raise LookupError('Available task options are {}'.format(self.tasks_available))
        if not isinstance(self.fetcher, self.tasks_available[val]):
            raise TypeError('Fetcher type wrong.')
        self._task = val
