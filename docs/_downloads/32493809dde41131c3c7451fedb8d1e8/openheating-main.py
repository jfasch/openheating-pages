#!/usr/bin/python3

from openheating.plant import logutil
from openheating.plant import dbusutil
from openheating.plant.config_plant import PlantConfig
from openheating.dbus import names
from openheating.dbus import lifecycle
from openheating.dbus.main import Main_Server

from gi.repository import GLib

import argparse


parser = argparse.ArgumentParser(description='OpenHeating: DBus circuit service')
parser.add_argument('--config', help='Main/plant configuration file')
dbusutil.argparse_add_bus(parser)
logutil.add_log_options(parser)
args = parser.parse_args()

logutil.configure_from_argparse(args, componentname=names.Bus.MAIN)
bus = dbusutil.bus_from_argparse(args)

config = PlantConfig()
config.parse(args.config)

main_object = Main_Server(
    bus=bus,
    servicedefs=config.get_servicedefs(),
    interval=5)

lifecycle.run_server(
    loop=GLib.MainLoop(),
    bus=bus,
    busname=names.Bus.MAIN,
    objects=[('/', main_object)],
)
