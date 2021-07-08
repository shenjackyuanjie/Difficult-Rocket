"""
writen by shenjackyuanjie
mail: 3695888@qq.com
github: @shenjackyuanjie
"""
import logging
import logging.config
import configparser

configs = configparser.ConfigParser()
configs.read('logging.config')
# configs['version'] = 1

# logging.config.dictConfig(configs)
logging.config.fileConfig('logging.config')
logger = logging.getLogger('simpleExample')


logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
