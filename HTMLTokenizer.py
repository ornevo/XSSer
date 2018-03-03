"""
Author: Or Nevo Michrowski
Date: 11/4/2017
Description: This file defines the HTMLTokenizer class, which
    receive an html document and extracts it's forms out of it.
The class eventually stores a few form objects,
    each representing a form on the page.
"""
from HTMLParser import HTMLParser
from Form import Form


# Constants
# Tags
T_FORM = "form"
T_INPUT = "input"

# Attributes
A_METHOD = "method"
A_ACTION = "action"
A_NAME = "name"
A_TYPE = "type"

DEFAULT_INP_TYPE = "text"


class HTMLTokenizer(HTMLParser):
    def __init__(self, html, page_url):
        """
        The constructor
        :param html: The html page as a string
        :param page_url: The full url (including protocol prefix, e.g. http://)
            of the page.
        """
        HTMLParser.__init__(self)
        self._url = page_url
        self._forms = []
        self._forms_i = 0
        self._iter_i = 0

        self.feed(html)

    # === Starting tags handling === #

    def handle_starttag(self, tag, attrs):
        """
        This method is called by the super class HTMLParser
            while parsing the page.
        It's called whenever the parser meets an opening tag.
        :param tag: The opening tag it met
        :param attrs: The attributes of the tag
        :return: None
        """
        # If an opening form
        if tag == T_FORM:
            self.handle_starting_form(attrs)
        elif tag == T_INPUT:
            self.handle_input_tag(attrs)

    def handle_starting_form(self, attrs):
        """
        This method handles a new form opening event.
        Called from handle_starttag
        :param attrs: The attributes of the form
        :return: None
        """
        # First, get the relevant attributes
        form_method = ""
        form_action = ""
        for attr in attrs:
            if attr[0] == A_ACTION:
                form_action = attr[1]
            elif attr[0] == A_METHOD:
                form_method = attr[1]

        self._forms.append(Form(form_method, form_action, self._url))

    def handle_input_tag(self, attrs):
        """
        This method handles a new input field tag,
            and adds it to the current form.
        :param attrs: The attributes of the input
        :return: None
        """
        # First, get the relevant attributes
        inp_name = ""
        inp_type = ""
        for attr in attrs:
            if attr[0] == A_NAME:
                inp_name = attr[1]
            elif attr[0] == A_TYPE:
                inp_type = attr[1]

        if inp_type == "":
            inp_type = DEFAULT_INP_TYPE
        self._forms[self._forms_i].add_input(inp_name, inp_type)

    # === Closing tags handling === #

    def handle_endtag(self, tag):
        """
        This method handles closing tags, and is called from parent
            HTMLParser class.
        :param tag: The closed tag name
        :return: None
        """
        if tag == T_FORM:
            self._forms_i += 1  # Progress to the next form index

    # === Iterable slots === #

    def __iter__(self):
        self._iter_i = 0
        return self

    def next(self):
        if self._iter_i == self._forms_i:
            raise StopIteration
        self._iter_i += 1
        return self._forms[self._iter_i - 1]
