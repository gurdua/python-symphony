#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Purpose:
        Unit Tests for Pod Methods related to Users
            - get_userid_by_email
            - get_user_id_by_user
            - adduser_to_stream
            - user_feature_update
            - search_user
'''

__author__ = 'Matt Joyce'
__email__ = 'matt@joyce.nyc'
__copyright__ = 'Copyright 2017, Symphony Communication Services LLC'

import httpretty
import json
import unittest
import symphony


@httpretty.activate
class Pod_Users_tests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Pod_Users_tests, self).__init__(*args, **kwargs)
        self.__uri__ = "http://fake.pod/"
        self.__session__ = "sessions"
        self.__keymngr__ = "keys"
        self.pod = symphony.Pod(self.__uri__, self.__session__, self.__keymngr__)

    def test_get_userid_by_email(self):
        ''' test get_user_id_by_email '''
        # register response
        httpretty.register_uri(httpretty.GET, self.__uri__ + "pod/v1/user",
                               body='{"id": 123456, "emailAddress": "test@fake.pod" }',
                               status=200,
                               content_type='text/json')
        # run test query
        status_code, response = self.pod.get_userid_by_email('test@fake.pod')
        response = json.loads(response)
        # verify return
        assert status_code == 200
        assert response['id'] == 123456
        assert response['emailAddress'] == "test@fake.pod"

    def test_get_user_id_by_user(self):
        ''' test get_user_id_by_user '''
        # register response
        httpretty.register_uri(httpretty.GET, self.__uri__ + "pod/v1/user/name/testuser/get",
                               body='{"id": 123456, "emailAddress": "test@fake.pod" }',
                               status=200,
                               content_type='text/json')
        # run test query
        status_code, response = self.pod.get_user_id_by_user('testuser')
        response = json.loads(response)
        # verify return
        assert status_code == 200
        assert response['id'] == 123456
        assert response['emailAddress'] == "test@fake.pod"

    def test_user_feature_update(self):
        ''' test user_feature_update '''
        # register response
        httpretty.register_uri(httpretty.POST, self.__uri__ + "pod/v1/admin/user/123456/features/update",
                               body='{ "format": "TEXT", "message": "OK" }',
                               status=200,
                               content_type='text/json')
        # run test query
        test_feature_query = '[{"entitlment": "isExternalRoomEnabled", "enabled": true },'\
                             '{"entitlment": "isExternalIMEnabled", "enabled": true }]'
        status_code, response = self.pod.user_feature_update('123456', test_feature_query)
        # verify return
        assert status_code == 200


if __name__ == '__main__':
    unittest.main()
