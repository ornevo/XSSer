"""
Author: Or Nevo Michrowski
Date: 11/4/2017
Description: This class handles single page XSS scan.
"""
from Tkinter import END
from HTMLTokenizer import HTMLTokenizer
import requests


# Constants
FAST_SCAN = ["text"]


class XSSer(object):

    def __init__(self, link, list_of_inps, fast, status_box):
        """
        This constructor initializes the XSSer, to scan the passed link.
        :param link: The page to scan, with protocol prefix.
        :param list_of_inps: A reference to the list of all malicious input
            to be tested.
        :param fast: A boolean indicating whether to make a quick scan or not.
            A fast scan will only scan text fields, lower amount of inputs
            and will stop scanning after the first successful try.
        :param status_string: Listbox that contains the current status
        :return: None
        """
        self._link = link  # The page to scan
        self._inps = list_of_inps  # A reference to the list of test inputs
        self._fast = fast
        # A list of the successful inputs, in the form: INPUTNAME:SUCCESS_INPUT
        self.success = []

        page = requests.get(self._link).text
        self._tokenized_page = HTMLTokenizer(page, self._link)

        self.status_var = status_box
        self.status_var.insert(END, "Initialized")
        self.log_hidden = True

    def scan(self):
        """
        This method stars executing the scan of the page for XSSs.
        :return: None
        """
        # For each form
        for form in self._tokenized_page:
            self.scan_form(form)

        self.status_var.insert(END, "{*====== Done! ======*}")
        self.status_var.insert(END, "Success:")
        for success in self.success:
            self.status_var.insert(END, "    " + success)

    def scan_form(self, form):
        """
        This method receives a form object and scans it
        :param form: The form object to scan
        :return: None
        """
        # This method fills the form with random ACCEPTABLE values
        form.auto_fill()

        # And for each field within it
        for field_to_check in form.get_input_names():

            # Skip if its a fast scan and it's not a text field
            field_type = form.get_input_type(field_to_check)
            if self._fast and field_type not in FAST_SCAN:
                continue

            # Try all known crafted inputs, and check if they pass the WAF
            for crafted_inp in self._inps:
                if crafted_inp.startswith("#"):  # If quick scan stop flag
                    # Stop scan if quick scan, skip otherwise
                    if self._fast:
                        return
                    else:
                        continue

                self.status_var.insert(END, "Trying %s -> %s" %
                                       (crafted_inp, field_to_check))

                # Try it
                form.set_input_value(field_to_check, crafted_inp)
                print "Trying " + crafted_inp
                response = form.submit()

                # If found, if its a quick scan stop scanning
                if self.is_success(crafted_inp, field_to_check, response) \
                        and self._fast:
                    return

    def is_success(self, crafted_inp, input_name, response):
        """
        This method checks whether a response for a submission means
            we found a vulnerability.
        If it is successful, the method adds it to the "successful" list and
            return True.
        :param crafted_inp: The input that was submitted
        :param input_name: The name of the input that was attacked
        :param response: The response for the submission
        :return: True/False, whether it was successful
        """
        if hasattr(response, "text") and crafted_inp in response.text:
            self.success.append(crafted_inp + " -> " + input_name)
            return True
        return False

    def toggle_log(self):
        if self.log_hidden:
            self.status_var.grid_remove()
        else:
            self.status_var.grid()
        self.log_hidden = not self.log_hidden
