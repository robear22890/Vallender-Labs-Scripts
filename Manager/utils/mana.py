##############################################################################
# PyCharm Community Edition
# -*- coding: utf-8 -*-
"""
Orthologs-Project
Directory_management updated on 11/15/2016 at 11:30 AM
##############################################################################

    Input:  A string that represents a path for the main file systems

    Output:  Custom class variables for import in the project file template.

    Description:  This file manges the directories for projects created in PyCharm.
    Each new project gets it's own function.

##############################################################################
@author: rgilmore
"""
##############################################################################
# Libraries:


import json
import os
import shutil
import time
from pathlib import Path
from cookiecutter.main import cookiecutter
from Manager.utils import treelib2
from Manager.utils.json_to_newick import _parse_json
# TODO-ROB once this is a pypi package all of these will be unnecessary
import Cookies
import Manager
import Orthologs
import Tools
from Manager.logit.logit import LogIt

#from project_mana import project_mana  # //TODO-ROB: Add a configure function to proj_mana to get the root directory using the project name
##############################################################################
# Directory Initializations:


class Mana(object):
    """
    This is the directory management base class.  It 
    maps the directories in the PyPi package using the pathlib module and 
    turns the names of each important directory into a pathlike object.  The 
    base class gives the option of creating a new repository with cookiecutter.
    
    This is also the home for many of the utility functions for manipulating
    directories or paths.
    """

# //TODO-ROB Add JSON loading of the different directory variables
# //TODO-Rob change project to projects and add another variable called project_type

    def __init__(self, home=os.getcwd(), repo=None, new_repo=False):
        """
        
        :param home(path or path-like): The home of the file calling this name.  When creating a new 
            repository it is best to explicitly name the home path.
        :param repo(string): The name of the new repository to be created.
        :param new_repo(bool): Triggers cookiecutter to create a new repository.
        """
        # config = tablib.Dataset().load(open('config.yaml').read())
        self.file_home = Path(home)  # Home of the file calling this class

        # Below are the PyPi path strings
        #    The first group is to access the cookiecutter templates
        self.Cookies = Path(Cookies.__path__.path[0])
        self.repo_cookie = self.Cookies / Path('new_repository')
        self.user_cookie = self.Cookies / Path('new_user')
        self.project_cookie = self.Cookies / Path('new_project')
        self.research_cookie = self.Cookies / Path('new_research')
        self.app_cookie = self.Cookies / Path('new_app')
        #    The second group is for the Manager module
        self.Manager = Path(Manager.__path__.path[0])
        self.index = self.Manager / Path('index')
        self.logit = self.Manager / Path('logit')
        self.utils = self.Manager / Path('utils')
        self.shiny = self.Manager / Path('shiny')
        #    The third group is for the Orthologs module
        self.Orthologs = Path(Orthologs.__path__.path[0])
        self.biosql = Path(self.Orthologs) / Path('biosql')
        self.blast = Path(self.Orthologs) / Path('blast')
        self.comp_gen = Path(self.Orthologs) / Path('comparative_genetics')
        self.genbank = Path(self.Orthologs) / Path('genbank')
        self.manager = Path(self.Orthologs) / Path('manager')
        self.phylogenetics = Path(self.Orthologs) / Path('phylogenetics')
        #    The fourth group is for the Tools module
        self.Tools = Path(Tools.__path__.path[0])
        self.ftp = Path(self.Tools) / Path('ftp')
        self.multiprocessing = Path(self.Tools) / Path('multiprocessing')
        self.pandoc = Path(self.Tools) / Path('pandoc')
        self.pybasher = Path(self.Tools) / Path('pybasher')
        self.qsub = Path(self.Tools) / Path('qsub')

        if repo:
            self.repo = repo
            self.repo_path = self.file_home / Path(self.repo)
        if new_repo is True:
            self.create_repo()

        # Create a directory management logger
        # TODO-ROB figure out where to put this based on user stuff
        log = LogIt('user/path/userfile.log', 'Directory Management')
        self.dm_log = log.basic

    def create_repo(self):
        """This function creates a new repository.  If a repository name 
        is given to the class then it is given a name.  If not, cookiecutters
        takes input from the user.
        
        The base class will be the only class that allows cookiecutters parameter
        no_input to be False.
        """
        if self.repo:
            no_input = True
            e_c = {
                "project_slug": self.repo
            }
        else:
            e_c = None
            no_input = False
        cookiecutter(self.repo_cookie, no_input=no_input, extra_context=e_c, output_dir=self.file_home)

    # Map the main project directory.
    def get_dir_map(self, top, gitignore=None):
        # TODO-ROB:  Change ignore to a .gitignore filename
        default_ignore = ['.git', '.idea']
        if gitignore is not None:
            gitignore += default_ignore
        else:
            gitignore = default_ignore
        # Treelib will help to map everything and create a json at the same time
        tree = treelib2.Tree()
        tree.create_node('.', top)
        # Walk through the directory of choice (top)
        # Topdown is true so that directories can be modified in place
        for root, dirs, files in os.walk(top, topdown=True):
            # Only remove directories from the top
            if root == top:
                print(root)
                try:
                    dirs[:] = set(dirs) - set(gitignore)  # Remove directories from os.walk()
                    print(dirs)
                except ValueError:
                    pass
            for d in dirs:
                rd = str(Path(root) / Path(d))
                tree.create_node(d, identifier=rd, parent=root)
            for f in files:
                tree.create_node(f, parent=root)
        return tree

    # def user_dir_config(self, username):
    #     # TODO-ROB USE SQL here to see if the user db contains the username
    #     if username in os.listdir(self.users):
    #         return UserWarning('This user already exists')
    #     else:
    #         # TODO-ROB CREATE THESE IN A VIRTUAL ENVIRONMENT FOR EACH USER
    #         # TODO-ROB The virtual environment can be the name of the user
    #         # TODO-ROB When the user logs in, they will activate the virtual environment
    #         for path in self.user_dict.values():
    #             Path.mkdir(path, parents=True, exist_ok=True)
    #         for path in self.user_project_dict.values():
    #             Path.mkdir(path, parents=True, exist_ok=True)
    #
    # def user_project_config(self, project_name, private=False):
    #     if private is False:
    #         path = self.user_project_dict['public']
    #     else:
    #         path = self.user_project_dict['private']
    #     Path.mkdir(path / Path(project_name))

    def get_newick_dir_map(self, top, ignore=None):
        """Takes a treelib tree created by get_dir_map and returns
        a tree a dir_map in newick format.  This will be useful for Bio.Phylo
        applications."""

        tree = self.get_dir_map(top, ignore)
        Ntree = _parse_json(tree.to_jsonnewick())
        return Ntree

    def proj_mana(self, js_file):
        with open(js_file, 'r') as file:
            pdr = json.load(file)
        return pdr

    # # //TODO-ROB Find a different way to return a
    # def path_list_make(self, path, o_path=None):
    #     # Takes a path and reduces it to a list of directories within the project
    #     # An optional attribute (o_path) is give so that a deeper path within the project can be used
    #     home = str(self.__project_home).split('/')
    #     path_list = str(path).split('/')
    #     for item in home:
    #         if item in path_list:
    #             path_list.remove(item)
    #     # path_list = set(p) - set(home)
    #     if o_path is not None:
    #         o_path = str(o_path).split('/')
    #         for item in o_path:
    #             if item in path_list:
    #                 path_list.remove(item)
    #         # path_list = set(path_list) - set(o_path)
    #     return path_list

    # //TODO-ROB utilize Path.mkdir(parents=TRUE) instead
    # def dir_make(self, path, path_list):
    #     # Takes a path list which is a list of folder names
    #     # path_list created by str(path).split('/')
    #     # The path_list appends to path, which is already an established directory inside the project
    #     t = None
    #     for item in path_list:
    #
    #         if os.path.isdir(path + '/' + item): # If for some reason the directory already exists...
    #             path += '/' + item  # Append a directory
    #             continue
    #         path += '/' + item  # Append a directory
    #         os.mkdir(path)
    #     if len(os.listdir(path)) > 0:
    #         path, t = self.dir_archive(path, path_list='')
    #     return path, t
    #
    # # //TODO-ROB Change to using a compression module https://pymotw.com/2/compression.html
    # def dir_archive(self, path, path_list):
    #     # Use the path that you want to update/add to
    #     # Returns path and the time stamp (could be None)
    #     unique_dir = False
    #     archive_path = path
    #     for item in path_list:
    #
    #         path += '/' + item  # Append a directory
    #         if os.path.isdir(path):  # If the child directory exists
    #             archive_path = path  # Then update the dir_archive path and continue
    #             continue
    #         else:                     # If the child directory doesnt exist
    #             unique_dir = True     # Then raise the flag
    #             os.mkdir(path)        # And make a directory
    #
    #     if unique_dir is False:  # Only dir_archive if the final child directory is not unique (via unique_dir = False)
    #         t = time.strftime("%m%d%Y-%I%M%S")
    #         new_archive = self.Archive + '/' + t  # Creates a time stamped directory
    #
    #         os.mkdir(new_archive)
    #         for item in os.listdir(archive_path):
    #             if os.path.isfile(archive_path + '/' + item):  # Only dir_archive the FILES
    #                 shutil.move(archive_path + '/' + item, new_archive)
    #         return path, t
    #     else:
    #         return path, None





# TODO-ROB Add a instance that stores new paths inside of a text file and has an updating/overwriting ability

# TODO-ROB CALL ON THIS INSTNACE IN __INIT__ SO THAT VARIABLES CAN BE CREATED BASED ON THE PATHS








