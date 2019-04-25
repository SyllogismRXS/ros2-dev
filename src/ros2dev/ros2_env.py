#!/usr/bin/env python3

import os
import argparse
import argcomplete
import shutil
from subprocess import check_call

from jinja2 import Environment, FileSystemLoader

def render(name, tmp_dir, replace, env):
    template = env.get_template(name)

    with open(tmp_dir + "/" + name, "w") as f:
        f.write(template.render(data = replace))

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cwd = os.getcwd()

    parser = argparse.ArgumentParser(description='ROS 2 Docker Environment.')
    add = parser.add_argument
    add('positional', choices=['generate', 'build', 'env', 'run'])
    add('-p', '--project_name', default='myproject', help='docker project name')
    add('-d', '--output_dir', default=cwd + "/generated", help='Directory to hold generated files')
    add('-b', '--build_context', default=cwd, help='Docker build context')
    add('-u', '--user_name', default='ros2', help='User to create in Docker')
    add('-w', '--ws_copy_dir', default=None, help='Directory to copy into ROS 2.0 workspace')
    add('-c', '--command', default=None, help='Command to run')
    add('-o', '--dockerfile_override', default=None, help='Dockerfile that overrides base Dockerfile.in')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    replace = {}
    replace['Dockerfile'] = 'Dockerfile'
    template_dirs = [script_dir + '/templates']

    if args.dockerfile_override is not None:
        replace['Dockerfile'] = os.path.basename(args.dockerfile_override)
        template_dirs.append(os.path.dirname(os.path.realpath(args.dockerfile_override)))

    file_loader = FileSystemLoader(template_dirs)
    env = Environment(loader=file_loader)

    tmp_dir = args.output_dir
    if not os.path.exists(tmp_dir):
        try:
            os.mkdir(tmp_dir)
        except OSError:
            print ("Creation of the directory %s failed" % tmp_dir)

    replace['USER_ID'] = os.geteuid()
    replace['tmp_dir'] = tmp_dir
    replace['target'] = 'amd64'
    replace['project_name'] = args.project_name
    replace['build_context'] = args.build_context
    replace['user_name'] = args.user_name
    replace['ws_copy_dir'] = args.ws_copy_dir

    if args.positional == 'generate':
        render(replace['Dockerfile'], tmp_dir, replace, env)
        render('docker-compose.yml', tmp_dir, replace, env)
        return 0
    elif args.positional == 'build':
        cmd = "docker-compose -p " + args.project_name + " build " + replace['target'] + "-" + args.project_name
    elif args.positional == 'env':
        cmd = "docker-compose -p " + args.project_name + " up -d " + replace['target'] + "-" + args.project_name + \
              " && docker attach " + args.project_name + "_" + replace['target'] + "-" + args.project_name + "_1"
    elif args.positional == 'run':
        if args.command is not None:
            cmd = "docker run -it " + replace['target'] + "/" + args.project_name + ":latest " + args.command
        else:
            print("When using the 'run' command, set the --command (-c) flag.")
            return -1

    check_call(cmd, cwd=tmp_dir, shell=True)

    return 0

if __name__ == "__main__":
    sys.exit(main())
