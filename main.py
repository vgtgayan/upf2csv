from upf2csv_lib import *

debug = True
if debug:
    print("Debug Mode on...\n")



if __name__ == '__main__':

    #test_csv_syntax_class()
    #test_power_domain_data()
    #test_upf_reader()
    #test_power_domain_upf()
    upf2csv("top.upf", "out.csv")
