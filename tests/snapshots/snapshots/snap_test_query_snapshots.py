# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['APITestCase::test_equipment_against_snapshot equipment_snapshot_resp'] = {
    'data': {
        'levels': [
            {
                'difficulty': 'beginner'
            },
            {
                'difficulty': 'intermediate'
            },
            {
                'difficulty': 'advanced'
            }
        ]
    }
}

snapshots['APITestCase::test_levels_response_against_snapshot levels_snapshot_resp'] = {
    'data': {
        'levels': [
            {
                'difficulty': 'beginner'
            },
            {
                'difficulty': 'intermediate'
            },
            {
                'difficulty': 'advanced'
            }
        ]
    }
}
