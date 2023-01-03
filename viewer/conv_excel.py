"""convert xfstest results to excel format

This modules define the method for excel format.
"""

import pandas as pd
from conv_generic import ConvClass

class ConvExcelClass(ConvClass):

    def convert_results(self, l, key):
        """This method convert the list to Dataframe for excel

        Args:
            l (list): The class instance list 
            k (str): key name for excel sheet name

        Examples:
            >>> convert_results({"passed": [testcase.SkippepClass("foo")]}, 'passed')
                   name sec path remarks
            0       foo
        """
        return pd.DataFrame(l[key])

    def dump_results(self, l, output):
        """This method dump the results to excel format

        Args:
            l (list): The class instance list 
            output (str): Output pathname

        Examples:
            >>> dump_results({"passed": [testcase.SkippepClass("foo")]}]}, None)
        """
        if output is None:
            output = 'out.xlsx'

        pd.DataFrame([]).to_excel(output, sheet_name="Title")

        for k in l:
            with pd.ExcelWriter(output, mode='a') as writer:
                df = self.convert_results(l, k)
                df.to_excel(writer, sheet_name=k, index=False)
