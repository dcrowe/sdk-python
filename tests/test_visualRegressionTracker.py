import pytest
from visual_regression_tracker_sdk import Config, VisualRegressionTracker, \
    TestRun, TestRunResult, TestRunStatus, Build


CONFIG = Config(
    apiUrl='http://localhost:4200',
    branchName='develop',
    project='Default project',
    apiKey='CPKVK4JNK24NVNPNGVFQ853HXXEG',
)


@pytest.fixture
def mock_post(mocker):
    yield mocker.patch('visual_regression_tracker_sdk.visualRegressionTracker._http_post_json')


@pytest.fixture
def vrt():
    yield VisualRegressionTracker(CONFIG)


def test__track__should_track_success(vrt, mocker):
    testRun = TestRun(
        name='name',
        imageBase64='image',
        os='os',
        device='device',
        viewport='viewport',
        browser='browser',
        diffTollerancePercent=None,
    )
    testRunResult = TestRunResult(
        url='url',
        status=TestRunStatus.OK,
        pixelMisMatchCount=12,
        diffPercent=0.12,
        diffTollerancePercent=0,
    )
    vrt._startBuild = mocker.Mock()
    vrt._submitTestResult = mocker.Mock(return_value=testRunResult)
    
    vrt.track(testRun)

    vrt._startBuild.assert_called_once()
    vrt._submitTestResult.assert_called_once_with(testRun)


def test__track__should_track_no_baseline(vrt, mocker):
    testRun = TestRun(
        name='name',
        imageBase64='image',
        os='os',
        device='device',
        viewport='viewport',
        browser='browser',
        diffTollerancePercent=None,
    )
    testRunResult = TestRunResult(
        url='url',
        status=TestRunStatus.NEW,
        pixelMisMatchCount=12,
        diffPercent=0.12,
        diffTollerancePercent=0,
    )
    vrt._startBuild = mocker.Mock()
    vrt._submitTestResult = mocker.Mock(return_value=testRunResult)
    
    with pytest.raises(Exception, match='No baseline: url'):
        vrt.track(testRun)


def test__track__should_track_difference(vrt, mocker):
    testRun = TestRun(
        name='name',
        imageBase64='image',
        os='os',
        device='device',
        viewport='viewport',
        browser='browser',
        diffTollerancePercent=None,
    )
    testRunResult = TestRunResult(
        url='url',
        status=TestRunStatus.UNRESOLVED,
        pixelMisMatchCount=12,
        diffPercent=0.12,
        diffTollerancePercent=0,
    )
    vrt._startBuild = mocker.Mock()
    vrt._submitTestResult = mocker.Mock(return_value=testRunResult)
    
    with pytest.raises(Exception, match='Difference found: url'):
        vrt.track(testRun)


def test__startBuild__should_start_build(vrt, mock_post):
    buildId = '1312'
    projectId = 'asd'

    mock_post.return_value = {'id':buildId, 'projectId':projectId}

    vrt._startBuild()

    mock_post.assert_called_once_with(
        f'{CONFIG.apiUrl}/builds',
        {'branchName':CONFIG.branchName, 'project':CONFIG.project},
        {'apiKey':CONFIG.apiKey},
    )

    assert vrt.buildId == buildId
    assert vrt.projectId == projectId


def test__startBuild__should_throw_if_no_build_id(vrt, mock_post):
    mock_post.return_value = {'id':None, 'projectId':'projectId'}

    with pytest.raises(Exception, match='Build id is not defined'):
        vrt._startBuild()


def test__startBuild__should_throw_if_no_project_id(vrt, mock_post):
    mock_post.return_value = {'id':'asd', 'projectId':None}

    with pytest.raises(Exception, match='Project id is not defined'):
        vrt._startBuild()


def test__submitTestResults__should_submit_test_run(vrt, mock_post):
    testRunResult = TestRunResult(
        url='url',
        status=TestRunStatus.UNRESOLVED,
        pixelMisMatchCount=12,
        diffPercent=0.12,
        diffTollerancePercent=0,
    )
    testRun = TestRun(
        name='name',
        imageBase64='image',
        os='os',
        device='device',
        viewport='viewport',
        browser='browser',
        diffTollerancePercent=None,
    )
    buildId = '1312'
    projectId = 'asd'
    vrt.buildId = buildId
    vrt.projectId = projectId

    mock_post.return_value = testRunResult._asdict()

    result = vrt._submitTestResult(testRun)

    assert result == testRunResult
    mock_post.assert_called_once_with(
        f'{CONFIG.apiUrl}/test-runs',
        {
          'name': testRun.name,
          'imageBase64': testRun.imageBase64,
          'os': testRun.os,
          'browser': testRun.browser,
          'viewport': testRun.viewport,
          'device': testRun.device,
          'diffTollerancePercent': None,
          'buildId': buildId,
          'projectId': projectId,
          'branchName': CONFIG.branchName,
        },
        {'apiKey': CONFIG.apiKey},
    )

