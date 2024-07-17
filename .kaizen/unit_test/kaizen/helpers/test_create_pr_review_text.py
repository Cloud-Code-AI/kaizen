import pytest
from kaizen.helpers.output import create_pr_review_text

PR_COLLAPSIBLE_TEMPLATE = '''
<details>
<summary>{comment}</summary>

**Reason:** {reason}

**Solution:** {solution}

**Confidence:** {confidence}

**Lines:** {start_line}-{end_line}

**File:** {file_name}

**Severity:** {severity}

</details>
'''


def test_create_pr_review_text_no_reviews():
    topics = {}
    expected_output = '## Code Review\n\n✅ **All Clear:** This PR is ready to merge! 👍\n\n'
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_single_review_no_issues():
    topics = {
        'Topic1': [
            {
                'comment': 'Good code',
                'reason': 'Well written',
                'solution': 'None needed',
                'confidence': 'high',
                'start_line': 1,
                'end_line': 2,
                'file_name': 'file1.py',
                'severity_level': 5
            }
        ]
    }
    expected_output = '## Code Review\n\n✅ **All Clear:** This PR is ready to merge! 👍\n\n### Topic1\n\n' + PR_COLLAPSIBLE_TEMPLATE.format(
        comment='Good code',
        reason='Well written',
        solution='None needed',
        confidence='high',
        start_line=1,
        end_line=2,
        file_name='file1.py',
        severity=5
    ) + '\n'
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_single_review_with_issues():
    topics = {
        'Topic1': [
            {
                'comment': 'Critical issue',
                'reason': 'Security vulnerability',
                'solution': 'Fix it',
                'confidence': 'critical',
                'start_line': 10,
                'end_line': 20,
                'file_name': 'file2.py',
                'severity_level': 9
            }
        ]
    }
    expected_output = '## Code Review\n\n❗ **Attention Required:** This PR has potential issues. 🚨\n\n### Topic1\n\n' + PR_COLLAPSIBLE_TEMPLATE.format(
        comment='Critical issue',
        reason='Security vulnerability',
        solution='Fix it',
        confidence='critical',
        start_line=10,
        end_line=20,
        file_name='file2.py',
        severity=9
    ) + '\n'
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_multiple_reviews_mixed_issues():
    topics = {
        'Topic1': [
            {
                'comment': 'Minor issue',
                'reason': 'Style',
                'solution': 'Reformat code',
                'confidence': 'medium',
                'start_line': 5,
                'end_line': 6,
                'file_name': 'file3.py',
                'severity_level': 3
            },
            {
                'comment': 'Critical issue',
                'reason': 'Security vulnerability',
                'solution': 'Fix it',
                'confidence': 'critical',
                'start_line': 10,
                'end_line': 20,
                'file_name': 'file4.py',
                'severity_level': 9
            }
        ],
        'Topic2': [
            {
                'comment': 'Good code',
                'reason': 'Well written',
                'solution': 'None needed',
                'confidence': 'high',
                'start_line': 1,
                'end_line': 2,
                'file_name': 'file5.py',
                'severity_level': 5
            }
        ]
    }
    expected_output = '## Code Review\n\n❗ **Attention Required:** This PR has potential issues. 🚨\n\n'
    expected_output += '### Topic1\n\n' + PR_COLLAPSIBLE_TEMPLATE.format(
        comment='Minor issue',
        reason='Style',
        solution='Reformat code',
        confidence='medium',
        start_line=5,
        end_line=6,
        file_name='file3.py',
        severity=3
    ) + '\n'
    expected_output += PR_COLLAPSIBLE_TEMPLATE.format(
        comment='Critical issue',
        reason='Security vulnerability',
        solution='Fix it',
        confidence='critical',
        start_line=10,
        end_line=20,
        file_name='file4.py',
        severity=9
    ) + '\n'
    expected_output += '### Topic2\n\n' + PR_COLLAPSIBLE_TEMPLATE.format(
        comment='Good code',
        reason='Well written',
        solution='None needed',
        confidence='high',
        start_line=1,
        end_line=2,
        file_name='file5.py',
        severity=5
    ) + '\n'
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_empty_review_list():
    topics = {
        'Topic1': []
    }
    expected_output = '## Code Review\n\n✅ **All Clear:** This PR is ready to merge! 👍\n\n'
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_no_critical_high_severity():
    topics = {
        'Topic1': [
            {
                'comment': 'Issue',
                'reason': 'Minor bug',
                'solution': 'Fix bug',
                'confidence': 'low',
                'start_line': 3,
                'end_line': 4,
                'file_name': 'file6.py',
                'severity_level': 2
            }
        ]
    }
    expected_output = '## Code Review\n\n✅ **All Clear:** This PR is ready to merge! 👍\n\n### Topic1\n\n' + PR_COLLAPSIBLE_TEMPLATE.format(
        comment='Issue',
        reason='Minor bug',
        solution='Fix bug',
        confidence='low',
        start_line=3,
        end_line=4,
        file_name='file6.py',
        severity=2
    ) + '\n'
    assert create_pr_review_text(topics) == expected_output