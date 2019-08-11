import logging
import json

from phones_scraper.config import get_config


class StateManager(object):

    # TODO: Usually im using redis for this ...

    def __init__(self):
        config = get_config()
        self.path_log = getattr(config, 'FILE_DONE', False)
        self.checkpoints = self.__get_states()

    def __get_states(self) -> dict:
        res = {}
        try:
            with open(self.path_log, 'r') as f_log:
                res = json.load(f_log)
        except (FileExistsError, FileNotFoundError, json.decoder.JSONDecodeError):
            return res

        return res

    def save_state(self, point: int, data):
        """
        Save site which was done. And in production environment i using Redis or Celery.

        :param point: id for checkpoint
        :type point: int

        :param data: result
        :type data: any
        """
        if not self.path_log:
            logging.error('Could\'nt save checkpoint, because path for log isn\'t defined')
            return

        self.checkpoints[point] = data
        with open(self.path_log, 'w') as f_log:
            json.dump(self.checkpoints, f_log)

    def check_state(self, point: int) -> bool:
        """
        Check this point is done or not.

        :param point: id for checkpoint
        :type point: int
        :return: Boolean
        """
        return point in self.checkpoints

    def get_state(self, point: int) -> bool:
        """
        Get state for checkpoint.

        :param point: id for checkpoint
        :type point: int
        :return: Boolean
        """
        return self.checkpoints[point] if point in self.checkpoints else None

    def reset_state(self):
        """
        Just clear all saved checkpoints.

        :return:
        """
        try:
            open(self.path_log, 'w').close()
        except (FileNotFoundError, FileExistsError):
            pass
