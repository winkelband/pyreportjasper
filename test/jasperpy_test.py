# -*- coding: utf-8 -*-
# GNU GENERAL PUBLIC LICENSE
#
# Copyright (c) 2020 Jadson Bonfim Ribeiro <contato@jadsonbr.com.br>
#

import os
from unittest import TestCase
from pyreportjasper import JasperPy


class TestJasperPy(TestCase):
    EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'examples')

    def setUp(self):
        self.input_file = os.path.join(self.EXAMPLES_DIR, 'hello_world.jrxml')
        self.jasper = JasperPy()

    def test_compile(self):
        self.assertRaises(NameError, self.jasper.compile, False)
        self.assertEqual(self.jasper.compile(self.input_file), 0)

    def test_process(self):
        self.assertRaises(NameError, self.jasper.process, False)

        # test invalid format input. Must be list ['pdf']
        kwargs = {
            'input_file': self.input_file,
            'format_list': 'pdf'
        }
        self.assertRaises(NameError, self.jasper.process, **kwargs)

        # test invalid input format
        kwargs = {
            'input_file': self.input_file,
            'format_list': 5
        }
        self.assertRaises(NameError, self.jasper.process, **kwargs)

        # test invalid report format
        kwargs = {
            'input_file': self.input_file,
            'format_list': ['mp3']
        }
        self.assertRaises(NameError, self.jasper.process, **kwargs)

        # test
        kwargs = {
            'input_file': self.input_file,
            'format_list': ['pdf']
        }
        self.assertEqual(self.jasper.process(**kwargs), 0)

    def test_subreports(self):

        input_file_header = os.path.join(self.EXAMPLES_DIR, 'subreports', 'header.jrxml')

        input_file_details = os.path.join(self.EXAMPLES_DIR, 'subreports', 'details.jrxml')

        input_file_main = os.path.join(self.EXAMPLES_DIR, 'subreports', 'main.jrxml')

        self.input_file = os.path.join(self.EXAMPLES_DIR, 'subreports', 'main.jasper')

        data_file = os.path.join(self.EXAMPLES_DIR, 'subreports', 'contacts.xml')

        resources = os.path.join(self.EXAMPLES_DIR, 'subreports') + os.sep

        self.jasper.compile(input_file_header)
        self.jasper.compile(input_file_details)
        self.jasper.compile(input_file_main)

        self.assertEqual(
            self.jasper.process(
                self.input_file,
                format_list=["pdf"],
                parameters={},
                db_connection={
                    'data_file': data_file,
                    'driver': 'xml',
                    'xml_xpath': '/',
                },
                locale='pt_BR',  # LOCALE Ex.:(en_US, de_GE)
                resource=resources
            ), 0)

    def test_jsonql(self):
        self.input_file = os.path.join(self.EXAMPLES_DIR, 'jsonql.jrxml')

        data_file = os.path.join(self.EXAMPLES_DIR, 'contacts.json')

        self.assertEqual(
            self.jasper.process(
                self.input_file,
                format_list=["pdf"],
                parameters={},
                db_connection={
                    'data_file': data_file,
                    'driver': 'jsonql',
                    'jsonql_query': 'contacts.person',
                    'json_locale': 'es_ES'
                },
                locale='pt_BR',  # LOCALE Ex.:(en_US, de_GE)
            ), 0)

    def test_json_process(self):
        self.input_file = os.path.join(self.EXAMPLES_DIR, 'jsonql.jrxml')

        data_file = os.path.join(self.EXAMPLES_DIR, 'contacts.json')

        self.assertEqual(
            self.jasper.process_json(
                self.input_file,
                format_list=["pdf"],
                parameters={},
                db_connection={
                    'data_file': data_file,
                    'driver': 'jsonql',
                    'jsonql_query': 'contacts.person',
                    'json_locale': 'es_ES',
                    'json_date_pattern': 'yyyy-MM-dd',
                    'json_number_pattern': '#,##0.##"'
                },
                locale='pt_BR',  # LOCALE Ex.:(en_US, de_GE)
            ), 0)

    def test_csv(self):
        self.input_file = os.path.join(self.EXAMPLES_DIR, 'csvMeta.jrxml')

        data_file = os.path.join(self.EXAMPLES_DIR, 'csvExampleHeaders.csv')

        self.assertEqual(
            self.jasper.process(
                self.input_file,
                format_list=["pdf"],
                parameters={},
                db_connection={
                    'data_file': data_file,
                    'driver': 'csv',
                    'csv_charset': 'utf8',
                    'csv_field_del': '|',
                    'csv_record_del': '\r\n',
                    'csv_columns': 'Name,Street,City,Phone'
                },
                locale='en_US',  # LOCALE Ex.:(en_US, de_GE)
            ), 0)
