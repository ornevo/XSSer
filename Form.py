"""
Author: Or Nevo Michrowski
Date: 11/4/2017
Description: This file defines the Form class, which represents a web form.
"""
import requests

# Constants
M_GET = "get"

# Input keys
K_NAME = "name"
K_TYPE = "type"
K_VALUE = "value"

# The following dictionary translates input types into their default values
INP_TYPE_TO_VALUE = {
    "text": "Abcdab_23",
    "password": "Fxilwx_99",
    "email": "justatest@mail.com",

}

IGNORE_TYPES = [u"submit", u"reset"]


class Form(object):
    def __init__(self, method, action, full_page_url):
        """
        :param method: The method of the form: get/post
        :param action: The action of the form
        :param full_page_url: The url of the form's page. including the domain
            and the http:// or https:// prefix.
        :return: None
        """
        super(Form, self).__init__()

        self._method = method.lower()
        # Inputs: Each input is a dictionary with the keys
        #   "name", "value" and "type"
        self._inputs = []

        if action.startswith('/'):  # If its an absolute url
            # Assuming that full_page_url starts with http:// to extract the
            #   domain
            splitted_domain = full_page_url.split("/")[:3]
            domain = splitted_domain[0] + "//" + splitted_domain[-1]
            self._action = domain + action
        elif action.startswith('http://') or action.startswith('https://'):
            self._action = action
        else:  # Relative path
            if full_page_url[-1] != '/':
                full_page_url += '/'
            self._action = full_page_url + action

    def add_input(self, name, type_of_inp):
        """
        This method adds an input to the form
        :param name: The name of the input
        :param type_of_inp: Its type
        :return: None
        """
        if type_of_inp not in IGNORE_TYPES:
            to_add = {
                K_NAME: name,
                K_TYPE: type_of_inp,
                K_VALUE: ""
            }
            self._inputs.append(to_add)

    def get_input_names(self):
        """
        This method returns a list of all the names of the inputs in the form.
        :return: A list of all the names of the inputs in the form.
        """
        ret = []
        for inp_dict in self._inputs:
            ret.append(inp_dict[K_NAME])
        return ret

    def get_input_type(self, inp_name):
        """
        Returns the type of the input with the name "inp_name"
        :param inp_name: The name of the input to return it's type
        :return: The input's type
        """
        for curr in self._inputs:
            if curr[K_NAME] == inp_name:
                return curr[K_TYPE]

    def set_input_value(self, input_name, new_value):
        """
        This method receives the a name of an input, and sets its value to a
            new, given one
        :param input_name: The name of the input to set
        :param new_value: The new value to set it to
        :return: None
        """
        to_set = \
            [curr for curr in self._inputs if input_name == curr[K_NAME]][0]
        to_set[K_VALUE] = new_value

    def set_input_to_default(self, input_name):
        """
        This method sets an input's value to it's default, acceptable one
        :param input_name: The name of the input to set
        :return: None
        """
        for curr in self._inputs:
            if curr[K_NAME] == input_name:
                curr[K_VALUE] = INP_TYPE_TO_VALUE[curr[K_TYPE]]
                break

    def auto_fill(self):
        """
        This method sets all the inputs to their default values
        :return: None
        """
        for inp in self._inputs:
            inp[K_VALUE] = INP_TYPE_TO_VALUE[inp[K_TYPE]]

    def submit(self):
        """
        This method sends the form with its input's current values,
            and returns the response.
        :return: The response to the form submission.
        """
        # Gather data to send
        payload = {}
        for inp in self._inputs:
            payload[inp[K_NAME]] = inp[K_VALUE]

        # Send
        if self._method == M_GET:
            return requests.get(self._action, params=payload)
        else:
            return requests.post(self._action, data=payload)

    # === Slots ===

    def __str__(self):
        """
        A toString implementation
        :return: Ya, the toString
        """
        str_rep = "<Form action='%s' method='%s' " % (str(self._action),
                                                      str(self._method))
        str_rep += "inputs=[%s] >" % \
                   ', '.join([str(inp) for inp in self._inputs])
        return str_rep
