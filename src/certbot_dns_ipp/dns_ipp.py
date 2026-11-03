"""
This module defines a certbot plugin to automate the process of completing a
``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and subsequently
removing, TXT records using the IP-Projects API.
"""

import logging

import requests
from certbot import errors
from certbot.plugins.dns_common import DNSAuthenticator

logger = logging.getLogger(__name__)

class Authenticator(DNSAuthenticator):
	description = "IPP DNS authenticator"
	url = "https://api.ip-projects.de/v1/dns/acme/"

	@classmethod
	def add_parser_arguments(cls, add):
		super().add_parser_arguments(add)
		add("credentials", help="the config file, that contains your ACME API key")


	def _setup_credentials(self):
		logger.debug("_setup_credentials")
		self.credentials = self._configure_credentials(
			"credentials",
			"Credentials file, that contains the ACME API key",
			{
				"acme_api_key": "Your ACME API key, as shown in the Customer Portal"
			}
		)
		self.api_key = self.credentials.confobj['dns_ipp_acme_api_key']


	def _perform(self, domain, validation_name, validation):
		logger.debug("_perform")
		payload = {
			"domain":	domain,
			"key":		validation_name,
			"value":	validation
		}
		self._send_request("add", payload)


	def _cleanup(self, domain, validation_name, validation):
		logger.debug("_cleanup")
		payload = {
			"domain":	domain,
			"key":		validation_name,
			"value":	validation
		}
		self._send_request("remove", payload)


	def _send_request(self, action, payload):

		headers = {
			"X-API-Key":		self.api_key,
			"Content-Type":		"application/json"
		}

		url = self.url + action

		try:
			response = requests.post(url, json=payload, headers=headers, timeout=15, verify=True)
			response.raise_for_status()

		except requests.exceptions.Timeout:
			raise errors.PluginError("request timed out")

		except requests.exceptions.ConnectionError:
			raise errors.PluginError("connection error")
		
		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 403:
				raise errors.PluginError("invalid API key, or no access to domain")
			else:
				raise errors.PluginError(f"request error occurred. status: {response.status_code}")
