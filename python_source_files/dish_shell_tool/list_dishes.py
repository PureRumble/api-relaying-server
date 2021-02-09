#!/usr/bin/python3.9

import requests
import sys
import json
from argparse import ArgumentParser

def receive_server_data():
	url = "http://localhost:8000/restaurant"
	if restaurant is not None:
		url += "/"+restaurant

	received = True
	try:
		response = requests.get(url)
	except:
		received = False
	finally:
		if received != True or response.status_code != 200:
			sys.exit("Connection to restaurant server failed.")

	try:
		r_info = json.loads(response.text)

		if type(r_info) is not dict:
			raise ValueError()
	except:
		sys.exit("Server didn't provde a valid response.")

	return r_info


def list_restaurants(r_info):
	try:
		if "restaurants" not in r_info or type(r_info["restaurants"]) is not list:
			raise ValueError()

		restaurants = r_info["restaurants"]

		r_names = {}
		for r in restaurants:
			if "identifier" not in r or "name" not in r:
				print("here")
				raise ValueError()

			r_names[r["identifier"]] = r["name"]

	except:
		sys.exit("Server didn't provde a valid response.")

	print("These are the restaurants:\n")
	print("Identifier\tName")
	print("------------------------------------------")

	for r in r_names:
		print(f"{r}\t\t{r_names[r]}")


def list_dishes(r_info):
	try:
		if "restaurant" not in r_info or "menu" not in r_info["restaurant"]:
			raise ValueError()

		menu = r_info["restaurant"]["menu"]

		if type(menu) is not list:
			raise ValueError()

		for dish in menu:
			if type(dish) is not dict or "dish" not in dish:
				raise ValueError()

	except:
		sys.exit("Server didn't provde a valid response.")

	print(f"Restaurant {restaurant} offers these dishes:\n")
	for dish in menu:
		print(dish["dish"])



arg_parser = ArgumentParser(
	description="""
		Lists today's dishes for a selected restaurant or all restaurants and their
		identifiers if none is selected.
		"""
)

arg_parser.add_argument(
	"--restaurant",
	action="store",
	type=str,
	help="The identifier of selected restaurant."
)

parsed_args = arg_parser.parse_args()
restaurant = parsed_args.restaurant

r_info = receive_server_data()

if restaurant is None:
	list_restaurants(r_info)
	sys.exit()

list_dishes(r_info)
