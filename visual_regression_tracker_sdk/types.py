import collections
import enum

Config = collections.namedtuple('Config', [
    'apiUrl',
    'branchName',
    'project',
    'apiKey',
])

Build = collections.namedtuple('Build', [
    'id',
    'projectId',
])

TestRun = collections.namedtuple('TestRun', [
    'name',
    'imageBase64',
    'os',
    'browser',
    'viewport',
    'device',
    'diffTollerancePercent',
])

TestRunResult = collections.namedtuple('TestRunResult', [
    'url',
    'status',
    'pixelMisMatchCount',
    'diffPercent',
    'diffTollerancePercent',
])


class TestRunStatus(enum.Enum):
    NEW = 'new'
    OK = 'ok'
    UNRESOLVED = 'unresolved'
