#-------------------------------- Project Details ---------------------------------------
    #   Title       : upf2csv converter
    #   Description : Convert upf code into UGO csv format
    #   Author      : Gayan VGT (gayan@synopsys.com)
    #   Started     : 9/01/2020
    #   Modified    : 9/25/2020
    # 
    # 
#------------------------------------ To Do ---------------------------------------------
    #   1. Convert class names to UpperCaseCamelCase convention - Done(9/24)
    #   2. [Bug-fix] outOfIndex error when all fields for a particular section is empty - Done(9/24)
    #   3. Add support for Supply section - Done(9/27)
    #   4. Check the possibility of simplifying the wrapper function - Done (9/25)
    #   5. Refer line 356
    # 
#------------------------------------ Work Log ------------------------------------------
    #   1. Power Domain section - Done
    #   2. User-Variable section - Done
    #   3. Backup v3: C:\Users\gayan\PycharmProjects\ugo_oop\upf2csv_lib_v3.py
    #                 Working code for power domain and user variable sections.
    #   4. [9/25/2020]
    #      Implemented wrapper classes
    #      Backup v4: C:\Users\gayan\PycharmProjects\ugo_oop\upf2csv_lib_v4.py
    #                 Working code for power domain and user variable sections with new 
    #                 wrapper class implementation
    #   5. [9/26/2020]
    #      Removed unnecessary functions for testing classes
    #      Added regex support in "command_filter", "switch_filter" and "has_switch" methods
    #       in UpfReader base class.
    #      [Bug-fixed] Bug in command_filter method. when "set " command is filtered,
    #       "create_supply_set" also filtered. Fixed using regex.
    #   6. [9/27/2020]
    #       Added suport for "Supply" section
    #       Enhanced, UpfReader -> get_name()
    #       Added bitcoin upf as testcase
    #       [Variable], [Power Domain] and [Supply] passed bicoin upf testcase
    #       [Backup - v5] : C:\Users\gayan\PycharmProjects\ugo_oop\upf2csv_lib_v4.py
    #           Code which, [Variable], [Power Domain] and [Supply] passed bicoin upf testcase.
    # 
    # 
    # 
    # 
#------------------------------- Import Libraries ---------------------------------------
import re
#
#
#
#=============================== Class Definitions  =====================================
#---------------------- Power Intent Data Structure classes -----------------------------
# Base class for the power intent data structure ----------
# Use dictionary to store field-value pairs
# Easy to write csv using dicionary methods
class PowerIntentData:
    # Define constructor
    def __init__(self, SECTION_NAME):
        self.SECTION_NAME = SECTION_NAME
        self.NAME = []
        self.ELEMENTS = []

    def set_section_name(self, SECTION_NAME):
        self.SECTION_NAME = SECTION_NAME

    def get_section_name(self):
        return self.SECTION_NAME

    def set_name(self, NAME):
        self.NAME.append(NAME)

    def get_name(self):
        return str(self.NAME.pop(0))

    def set_elements(self, ELEMENTS):
        self.ELEMENTS.append(ELEMENTS)

    def get_elements(self):
        return str(self.ELEMENTS.pop(0))


# Power domain data section ----------
class PowerDomainData(PowerIntentData):
    # Define constructor
    def __init__(self):
        PowerIntentData.__init__(self, "[Power Domain]")
        self.AVAILABLE_SUPPLIES = []
        self.primary = []

    def set_available_supplies(self, AVAILABLE_SUPPLIES):
        self.AVAILABLE_SUPPLIES.append(AVAILABLE_SUPPLIES)

    def get_available_supplies(self):
        return str(self.AVAILABLE_SUPPLIES.pop(0))

    def set_primary_supply(self, primary):
        self.primary.append(primary)

    def get_primary_supply(self):
        return str(self.primary.pop(0))


# User-variable data class for NAME,VALUE syntax type
class UserVariableNameValueData(PowerIntentData):
    # Define constructor
    def __init__(self):
        PowerIntentData.__init__(self, "[Variable]")
        self.VALUE = []    

    def set_value(self, VALUE):
        self.VALUE.append(VALUE)

    def get_value(self):
        return str(self.VALUE.pop(0))


# User-variable data class for NAME,PATTERN syntax type
class UserVariableNamePatternData(PowerIntentData):
    # Define constructor
    def __init__(self):
        PowerIntentData.__init__(self, "[Variable]")
        self.PATTERN = []   
        self.METHOD = []   
        self.OBJECT_TYPE = []   
        self.OTHER = []   


    def set_pattern(self, PATTERN):
        self.PATTERN.append(PATTERN)

    def get_pattern(self):
        return str(self.PATTERN.pop(0))


    def set_method(self, METHOD):
        self.METHOD.append(METHOD)

    def get_method(self):
        return str(self.METHOD.pop(0))


    def set_object_type(self, OBJECT_TYPE):
        self.OBJECT_TYPE.append(OBJECT_TYPE)

    def get_object_type(self):
        return str(self.OBJECT_TYPE.pop(0))


    def set_other(self, OTHER):
        self.OTHER.append(OTHER)

    def get_other(self):
        return str(self.OTHER.pop(0))


# Supply section data class 
class SupplyData(PowerIntentData):
    # Define constructor
    def __init__(self):
        PowerIntentData.__init__(self, "[Supply]")
        self.DIRECTION = []   
        self.RESOLVE = []   
        self.power = []   
        self.ground = []   
        self.nwell = []   
        self.pwell = []   


    def set_direction(self, DIRECTION):
        self.DIRECTION.append(DIRECTION)

    def get_direction(self):
        return str(self.DIRECTION.pop(0))


    def set_resolve(self, RESOLVE):
        self.RESOLVE.append(RESOLVE)

    def get_resolve(self):
        return str(self.RESOLVE.pop(0))


    def set_power(self, power):
        self.power.append(power)

    def get_power(self):
        return str(self.power.pop(0))


    def set_ground(self, ground):
        self.ground.append(ground)

    def get_ground(self):
        return str(self.ground.pop(0))


    def set_nwell(self, nwell):
        self.nwell.append(nwell)

    def get_nwell(self):
        return str(self.nwell.pop(0))


    def set_pwell(self, pwell):
        self.pwell.append(pwell)

    def get_pwell(self):
        return str(self.pwell.pop(0))


# Supply section data class 
class SwitchableSupplyData(PowerIntentData):
    # Define constructor
    def __init__(self):
        PowerIntentData.__init__(self, "[Switchable Supply]")
        self.OUT = []   
        self.STATE = []   
        self.IN = []   
        self.ACK = []   
        self.ACK_CONTROL = []   
        self.ACK_DELAY = []   
        self.CELL = []   


    def set_out(self, OUT):
        self.OUT.append(OUT)

    def get_out(self):
        return str(self.OUT.pop(0))

    def set_state(self, STATE):
        self.STATE.append(STATE)

    def get_state(self):
        return str(self.STATE.pop(0))

    def set_in(self, IN):
        self.IN.append(IN)

    def get_in(self):
        return str(self.IN.pop(0))       

    def set_ack(self, ACK):
        self.ACK.append(ACK)

    def get_ack(self):
        return str(self.ACK.pop(0))

    def set_ack_control(self, ACK_CONTROL):
        self.ACK_CONTROL.append(ACK_CONTROL)

    def get_ack_control(self):
        return str(self.ACK_CONTROL.pop(0))

    def set_ack_delay(self, ACK_DELAY):
        self.ACK_DELAY.append(ACK_DELAY)

    def get_ack_delay(self):
        return str(self.ACK_DELAY.pop(0)) 

    def set_cell(self, CELL):
        self.CELL.append(CELL)

    def get_cell(self):
        return str(self.CELL.pop(0)) 


#------------------ End of Power Intent Data Structure classes --------------------------
#
#
#
#
#
#
#
#------------------------------ UPF Reader classes --------------------------------------
# Base class for the UPF Reader ----------
class UpfReader():
    def __init__(self, upf_file_name):
        self.upf_file_name = upf_file_name

    # Function to filter a given command from a file
    # Return: Filtered command list
    # Limitations:
    # To Do:
    # Arguments: command_name - The name of the command to filter
    def command_filter(self,command_name , debug = False):
        output = []
        temp_cmd = ""
        multi_line_cmd = 0
        # Support spaces before the command name
        command_pattern = "^[ \t]*" + command_name
        with open(self.upf_file_name, "r") as fp:
            for line in fp:
                if (re.search(command_pattern, line)) or multi_line_cmd:
                    line = line.strip()
                    # Check line is not commented
                    if line[0] == "#":
                        continue
                    # Check for multi line commands
                    elif line[-1] == "\\":
                        temp_cmd = temp_cmd + line[:-1] + " "
                        multi_line_cmd = 1
                    # Last line of multi line commands
                    elif multi_line_cmd:
                        temp_cmd = temp_cmd + line
                        output.append(temp_cmd)
                        multi_line_cmd = 0
                        temp_cmd = ""
                    # Single line commands
                    else:
                        output.append(line)
                    # Debug message
                    if debug:
                        print(line)
        
        return output

    # Function to obtain the value(s) of a given switch in a given command. 
    # Return: The value(s) of the switch (comma separated for multiple values)
    # Supports: single value, multiple values within {}, single value within {}, 
    #           recurring switch:
    #           When same switch occurs more than once in a command 
    #           (Example: -funtion occurs more than once: create_supply_set SS2 -function {power VDD} -function {ground VSS} -update)
    # Limitations:
    # To Do: 
    def switch_filter(self, command, switch, debug = False):
        output = ""
        word_flag = 0
        multiple_flag = 0
        switch_count = 0
        # Split the command into words
        cmd_lst = command.split(" ")
        if debug:
            print(cmd_lst)
    
        for word in cmd_lst:
            if word_flag == 1:
                if debug:
                    print(word)
                # Case: User defined variable Ex: ${cpu_list}
                if word[0] == '$':
                    output += word
                # Check if the word starts with "{"
                elif word[0] == '{':
                    # Case: Single value within {}
                    if word[-1] == '}':
                        multiple_flag = 0
                        output += word[1:-1]
                    # Case: Multiple values within {}
                    else:
                        multiple_flag = 1
                        output += word[1:]
                # Case: Last value of multiple values within {}
                # Check if the word ends with '}'
                elif word[-1] == '}':
                    multiple_flag = 0
                    output += ',' + word[:-1]
                else:
                    # Case: Middle values of multiple values within {}
                    # Append next word to output until '}' is found
                    if multiple_flag == 1:
                        output += ',' + word
                    # Case: Single value without {}
                    else:
                        output += word
    
                if multiple_flag == 0:
                    word_flag = 0
    
            # Search for the given switch
            # Switch can be given with/without "-"
            key = "[-]?" + switch
            # if word == "-" + switch:
            if re.search(key, word):
                if debug:
                    print(word)
                # Case: Same switch occurs multiple times. Adding comma to separate values between switches
                if switch_count > 0:
                    output += ","
                # Set flag to obtain the values after the switch
                word_flag = 1
                # Count switch occurences
                switch_count += 1
    
        if debug:
            print(output)
    
        return output


    # Function to check if a switch exists or not. Return no:of occurences if exists else 0.
    # Supports: 
    # Limitations:
    # To Do:
    def has_switch(self, command, switch, debug = False):
        switch_count = 0
        cmd_lst = command.split(" ")
        if debug:
            print(cmd_lst)
        for word in cmd_lst:
            # Check if word starts with '['
            # print(len(word))
            if len(word) == 0:
                continue
            if word[0]=='[':
                # Remove '['
                word = word[1:]
            # Check if word ends with ']'
            if word[-1]==']':
                # Remove ']'
                word = word[:-1]

            # Search for the given switch
            # Switch can be given with/without "-"
            key = "^[-]?" + switch
            # if word == "-" + switch:
            if re.search(key, word):
                if debug:
                    print(word)
                switch_count += 1
        return switch_count

    # Return the second argument of the upf command.
    # In most of the time this is the name of the particular power object
    # This would be overridden in child classes
    # To Do: Support switch values within {}
    #        Ex: create_supply_set   -function {power VDDM} SS_MEM_SW -update
    def get_name(self, command, debug=False):
        # return command.split(" ")[1]
        command = command.split(" ")
        # Remove first word(command_name)
        command.pop(0)
        # Flag to check switches
        skip_flag = 0
        for word in command:    
            # Handle empty words       
            if len(word) == 0:
                continue
            # Identify switches (-switch) and skip
            elif word[0] == "-":
                skip_flag = 1
            # Skip switch value (value following the switch)
            elif skip_flag:
                skip_flag = 0
            # Return the NAME value
            else:
                return word


    
    # Function to get elements list
    # Supports: return #DEFAULT# for {.} or -include_scope switch. Else return elements.
    # Limitations:
    # To Do: Check the usage in various commands and override if needed
    def get_elements(self, command):
        elements = self.switch_filter(command, "elements")
        if elements == '.':
            return "#DEFAULT#"
        elif elements == "":
            if self.has_switch(command, "include_scope"):
                return "#DEFAULT#"
            else:
                return elements
        else:
            return elements

    # Function to read single upf command and store extracted data in power intent data object
    # Supports: Read single command
    # Limitations: Cannot process multiple commands
    # To Do:
    def read_upf(self, command, power_intent_object):
        power_intent_object.set_name(self.get_name(command))
        power_intent_object.set_elements(self.get_elements(command))


# Power domain upf reader class ----------
class PowerDomainUpfReader(UpfReader):
    def __init__(self,upf_file_name):
        UpfReader.__init__(self, upf_file_name)
        # Filter string for power domain related upf commands
        self.command_name = "create_power_domain"

    # Function to filter power domain related upf commands
    # Supports:
    # Limitations:
    # To Do: 
    def command_filter(self):
        return UpfReader.command_filter(self,self.command_name)

    # Function to get available supply list
    # Supports: -available_supplies {SS1 SS2}
    # Limitations:
    # To Do: 
    def get_available_supplies(self, command):
        avail_sup = self.switch_filter(command, "available_supplies")
        return avail_sup
        # return self.switch_filter(command, "available_supplies")

    # Function to get primary supply of power domain
    # Supports: -supply {primary SS1}
    # Limitations: Below style is not supported yet
    #               "create_power_domain PD1 -elements {.} -supply {ssh1} -supply {ssh2}"
    # To Do: Check the usage of -supply in create_power_domain
    def get_primary_supply(self, command):
        primary = self.switch_filter(command, "supply")
        primary = primary.split(",")
        if primary[0] == "primary":
            return primary[1]
        else:
            return None

    # Overrides Function to read upf file and store extracted data
    # Supports: 
    # Limitations:
    # To Do:
    def read_upf(self, command, power_intent_object):
        #Call super class method
        UpfReader.read_upf(self, command, power_intent_object)
        power_intent_object.set_available_supplies(self.get_available_supplies(command))
        power_intent_object.set_primary_supply(self.get_primary_supply(command))

             
# User-define Variable - Name Value type upf reader class ----------
class UserVariableNameValueUpfReader(UpfReader):
    def __init__(self,upf_file_name):
        UpfReader.__init__(self, upf_file_name)
        # Filter string for User-define Variable related upf commands
        self.command_name = "set "

    # Function to filter user variable Name Value type related upf commands
    # Supports:
    # Limitations:
    # To Do: 
    def command_filter(self, debug=False):
        output = []
        cmd_lst = UpfReader.command_filter(self, self.command_name)
        for cmd in cmd_lst:
            # Check if command contains pattern matching
            has_pattern = self.has_switch(cmd, "pattern")
            if has_pattern:
                if debug:
                    print("Command: {} is not supported by this method.".format(cmd))
            else:
                output.append(cmd)
        return output     

    # Function to 
    # Supports: NAME,VALUE CSV syntax 
    # Limitations:
    # To Do:     
    # UPF patterns:
    #   set mem_pd_name “PD_SRAM”
    #   set test_elem “test1”
    #   set temp_elem “test2 test3”
    #   set t_all “${test_elem} ${temp_elem}”
    #   set mem_pd_name_extend “PD_SRAM_${test_elem}”
    def get_value(self, command, debug=False):
        cmd_lst = command.split(" ")
        val_lst = cmd_lst[2:]
        val_str = ",".join(val_lst)
        if val_str[0] == '"':
            val_str = val_str[1:-1]
        if debug:
            print(cmd_lst)
            print(val_str)
        return val_str

    # Overrides Function to read upf file and store extracted data
    # Supports: 
    # Limitations:
    # To Do:
    def read_upf(self, command, power_intent_object):
        #Call super class method
        UpfReader.read_upf(self, command, power_intent_object)
        power_intent_object.set_value(self.get_value(command))


# User-define Variable - Name Pattern type upf reader class ----------
class UserVariableNamePatternUpfReader(UpfReader):
    def __init__(self,upf_file_name):
        UpfReader.__init__(self, upf_file_name)
        # Filter string for User-define Variable related upf commands
        self.command_name = "set "

    # Function to filter user variable Name Pattern type related upf commands
    # Supports:
    # Limitations:
    # To Do: 
    def command_filter(self, debug=False):
        output = []
        cmd_lst = UpfReader.command_filter(self, self.command_name)
        for cmd in cmd_lst:
            # Check if command contains pattern matching and append to output
            has_pattern = self.has_switch(cmd, "pattern")
            if has_pattern:
                output.append(cmd)
        return output 

    # Function to obtain pattern used for user variable
    # Supports:
    # Limitations:
    # To Do: 
    def get_pattern(self, command):
        return self.switch_filter(command, "pattern")

    # Function to obtain pattern method used for user variable
    # Supports:
    # Limitations:
    # To Do: 
    def get_method(self, command):
        if self.has_switch(command, "regexp"):
            return "#REGEX#"
        elif self.has_switch(command, "exact"):
            return "#EXACT#"
        else:
            return "#GLOB#"


    # Function to obtain object type used for user variable
    # Supports:
    # Limitations:
    # To Do: 
    def get_object_type(self, command):
        object_type = self.switch_filter(command, "object_type")
        # Return corresponding keyword for object type
        if object_type=="model":
            return "#MODEL#"
        elif object_type=="inst":
            return "#INST#"
        elif object_type=="port":
            return "#PORT#"
        elif object_type=="net":
            return "#NET#"
        else:
            return ''

    # Function to obtain other keywords used for user variable
    # Supports: -case_insensitive -ignore_case -transitive -non_leaf -leaf_only 
    # Limitations:
    # To Do: 
    def get_other(self, command):
        output = []
        case_insensitive = self.has_switch(command, "case_insensitive")
        ignore_case = self.has_switch(command, "ignore_case")
        transitive = self.has_switch(command, "transitive")
        non_leaf = self.has_switch(command, "non_leaf")
        leaf_only = self.has_switch(command, "leaf_only")
        # Return corresponding keyword for other type
        if case_insensitive or ignore_case:
            output.append("#CASE_INSENSITIVE#")
        if transitive:
            output.append("#TRANSITIVE#")
        if non_leaf:
            output.append("#NON_LEAF#")
        if leaf_only:
            output.append("#LEAF#")

        # Convert to string and return
        return ",".join(output)


    # Overrides Function to read upf file and store extracted data
    # Supports: 
    # Limitations:
    # To Do:
    def read_upf(self, command, power_intent_object):
        #Call super class method
        UpfReader.read_upf(self, command, power_intent_object)
        power_intent_object.set_pattern(self.get_pattern(command))
        power_intent_object.set_method(self.get_method(command))
        power_intent_object.set_object_type(self.get_object_type(command))
        power_intent_object.set_other(self.get_other(command))


# Supply - upf reader class ----------
class SupplyUpfReader(UpfReader):
    def __init__(self,upf_file_name):
        UpfReader.__init__(self, upf_file_name)
        # Filter string for User-define Variable related upf commands
        # self.command_name = "create_supply_set "
        self.NAME = []
        self.DIRECTION = []   
        self.RESOLVE = []   
        self.power = []   
        self.ground = []   
        self.nwell = []   
        self.pwell = []

    # Function to get power net
    # Supports:
    # Limitations:
    # To Do: 
    def get_power(self, command, debug=False):
        function = self.switch_filter(command, "function")
        function = function.split(",")
        index = 0
        for word in function:
            index +=1
            if word == "power":
                return function[index]
        return ''

    # Function to get ground net
    # Supports:
    # Limitations:
    # To Do: 
    def get_ground(self, command, debug=False):
        function = self.switch_filter(command, "function")
        function = function.split(",")
        index = 0
        for word in function:
            index +=1
            if word == "ground":
                return function[index]
        return ''

    # Function to get nwell net
    # Supports:
    # Limitations:
    # To Do: 
    def get_nwell(self, command, debug=False):
        function = self.switch_filter(command, "function")
        function = function.split(",")
        index = 0
        for word in function:
            index +=1
            if word == "nwell":
                return function[index]
        return ''

    # Function to get pwell net
    # Supports:
    # Limitations:
    # To Do: 
    def get_pwell(self, command, debug=False):
        function = self.switch_filter(command, "function")
        function = function.split(",")
        index = 0
        for word in function:
            index +=1
            if word == "pwell":
                return function[index]
        return ''

    # Function to get RESOLVE value of net
    # Supports:
    # Limitations:
    # To Do: 
    def get_resolve(self, command, debug=False):
        resolve_value = self.switch_filter(command, "resolve")
        if resolve_value == "unresolved":
            return "#UNRESOLVED#"
        elif resolve_value == "one_hot":
            return "#ONE_HOT#"
        elif resolve_value == "parallel":
            return "#PARALLEL#"
        elif resolve_value == "parallel_one_hot":
            return "#PARALLEL_ONE_HOT#"
        else:
            return resolve_value

    # Function to get DIRECTION value of net
    # Supports:
    # Limitations:
    # To Do: 
    def get_direction(self, command, debug=False):
        direction_value = self.switch_filter(command, "direction")
        if direction_value == "in":
            return "#IN#"
        elif direction_value == "out":
            return "#OUT#"
        elif direction_value == "internal":
            return "#INTERNAL#"
        else:
            return direction_value


    # Function to get port name of connect_supply_net 
    def get_ports(self, command, debug=False):
        return self.switch_filter(command, "ports")


    # Function to read create_supply_set command list and extract
    # NAME, power, ground, nwell, pwell values and store in self object
    # Supports: command list
    # Limitations: Only take data from commands which has power function
    # To Do:
    def read_create_supply_set(self, command_list, debug=False):
        # Read NAME and power
        for command in command_list:
            # Check if command contains power function
            if debug:
                print(command)
            has_power = self.has_switch(command, "[{]?power$")
            if has_power:
                ss_name = self.get_name(command)
                self.NAME.append(ss_name)
                # self.NAME.append(self.get_name(command))
                self.power.append(self.get_power(command))
                # self.ground.append(self.get_ground(command))
                # self.nwell.append(self.get_nwell(command))
                # self.pwell.append(self.get_pwell(command))
        # Read ground, nwell, pwell
        for ss_name in self.NAME:
            ground_net = ''
            nwell_net = ''
            pwell_net = ''            
            for command in command_list:
                ground_net_tmp = ''
                nwell_net_tmp = ''
                pwell_net_tmp = ''
                # Check if command contains supply set name
                has_NAME = self.has_switch(command, ss_name + "$")
                if has_NAME:
                    ground_net_tmp = self.get_ground(command)
                    nwell_net_tmp = self.get_nwell(command)
                    pwell_net_tmp = self.get_pwell(command)
                    # Keep non-empty values of ground, nwell, pwell
                    if len(ground_net_tmp) != 0:
                        ground_net = ground_net_tmp
                    if len(nwell_net_tmp) != 0:
                        nwell_net = nwell_net_tmp
                    if len(pwell_net_tmp) != 0:
                        pwell_net = pwell_net_tmp                                        
            self.ground.append(ground_net)
            self.nwell.append(nwell_net)
            self.pwell.append(pwell_net)

        if debug:
            print(self.NAME)
            print(self.power)
            print(self.ground)
            print(self.nwell)
            print(self.pwell)


    # Function to read create_supply_net command list and extract
    # RESOLVE values and store in self object
    # Supports: command list
    # Limitations: Only take data from commands which has matching power net
    # To Do:
    def read_create_supply_net(self, command_list, debug=False):
        for net in self.power:
            resolve_value = ''
            for command in command_list:
                # Check if command contains same power net name
                if net == self.get_name(command):
                   resolve_value = self.get_resolve(command)
            self.RESOLVE.append(resolve_value)
        if debug:
            print(self.RESOLVE)

    # Function to read create_supply_port connect_supply_port command list and extract
    # RESOLVE values and store in self object
    # Supports: command list
    # Limitations: Only take data from commands which has matching power net
    # To Do:
    def read_create_port_n_connect_net(self, create_port_command_list, connect_net_command_list, debug=False):
        for net in self.power:
            direction_value = ''
            port_name = ''
            for connect_net_command in connect_net_command_list:
                # Check if command contains same power net name
                if net == self.get_name(connect_net_command):
                    port_name = self.get_ports(connect_net_command)
                    if debug:
                        print("Port matched : " + port_name )

            for create_port_command in create_port_command_list:
                # Check if command contains same port name obtained above
                if port_name == self.get_name(create_port_command):                
                    direction_value = self.get_direction(create_port_command)
            self.DIRECTION.append(direction_value)
        if debug:
            print(self.DIRECTION)


    # Overrides Function to read upf file and store extracted data
    # Supports: 
    # Limitations:
    # To Do:
    def read_upf(self, supply_set_list, supply_net_list, create_port_command_list, connect_net_command_list, power_intent_object):
        self.read_create_supply_set(supply_set_list)
        power_intent_object.NAME.extend(self.NAME)
        power_intent_object.power.extend(self.power)
        power_intent_object.ground.extend(self.ground)
        power_intent_object.nwell.extend(self.nwell)
        power_intent_object.pwell.extend(self.pwell)

        self.read_create_supply_net(supply_net_list)
        power_intent_object.RESOLVE.extend(self.RESOLVE)

        self.read_create_port_n_connect_net( create_port_command_list, connect_net_command_list)
        power_intent_object.DIRECTION.extend(self.DIRECTION)

# Switchable supply section data class 
#[Switchable Supply]
#OUT,STATE[,IN,ACK,ACK_DELAY,ACK_CONTROL,CELL]
class SwitchableSupplyUpfReader(UpfReader):
    # Define constructor
    def __init__(self,upf_file_name):
        UpfReader.__init__(self, upf_file_name)
        # Filter string for power domain related upf commands
        self.command_name = "create_power_switch"

    # Function to filter power domain related upf commands
    # Supports:
    # Limitations:
    # To Do: 
    def command_filter(self):
        return UpfReader.command_filter(self,self.command_name) 

    def get_out(self, command, debug=True):
        out_str = self.switch_filter(command, "output_supply_port")
        if debug:
            print("[command]: ", command)
            # print("[Filtered switch]: ", out_lst)
        out_lst = out_str.split(',')
        out = out_lst[1]
        # Check if net is specified as the power function of the SS (Ex: SSL_SIPO_SLICE_SW.power)
        power_pattern = ".*[.]power$"
        if re.search(power_pattern, out):
            # print("[power switch]: ", out)
            # Crop the ".power" at the end and return SS name
            return out[:-6]
        # Else the SS where this net is the power net, should be obtained
        else:
            print("[Net switch]: ", out)
            return out

    # Overrides Function to read upf file and store extracted data
    # Supports: 
    # Limitations:
    # To Do:
    def read_upf(self, command, power_intent_object):
        #Call super class method
        power_intent_object.set_out(self.get_out(command))

#---------------------------- End of UPF Reader classes --------------------------------
#
#
#
#
#
#
#
#------------------------------ CSV Writer classes --------------------------------------
# Base class for the CSV Writer ----------
class CsvWriter():
    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name

    # Convert header list to string in UGO power intent CSV format
    # Limitations:
    # To Do: 
    def get_header_line(self, header_lst):
        # Convert header list to string in UGO power intent CSV format
        header_str = ",".join([str(val) for val in header_lst[1:]]) + "\n"
        # Obtain the number of fields (-1 is because first values is "SECTION_NAME")
        field_num = len(header_lst) -1
        return header_str, field_num

    # Obtain value list and header list from the data object and removes empty fields
    # Obtain the header_line and value lines intellegently w/o hardcoding
    # This is achieved by using dictionary data structure in PowerIntentData classes
    # Supports: Returns filtered header list n value list
    # Limitations:
    # To Do:
    def get_value_list(self, power_intent_object, debug = False):
        header_lst = list(power_intent_object.__dict__.keys())
        value_lst = list(power_intent_object.__dict__.values())
        if debug:
            print(value_lst)
            print(header_lst)

        # List to keep the index of empty fields
        empty_fields = []
        # List index
        index = 0
        # Identify empty fields
        for values in value_lst:
            # Flag to check if empty
            empty_flag = 1
            for val in values:
                # Breaks @ 1st non-empty field and set flag to 0
                if val != '' and val != None:
                    empty_flag = 0
                    break
            # Check all the values are empty
            if empty_flag:
                empty_fields.append(index)
            # Increment the index
            index += 1

        if debug:
            print(empty_fields)
        # Remove empty fields
        # Correction variable is to tackle with the change in index after pop()
        correction = 0
        for i in empty_fields:
            value_lst.pop(i-correction)
            header_lst.pop(i-correction)
            correction += 1

        return header_lst,value_lst


    # Writes extracted data in UGO power intent CSV format
    # Supports: 
    # Limitations:
    # To Do: 
    def write_csv(self, power_intent_object, debug = False):
        with open(self.csv_file_name, "a") as csv_fp:
            # Get header list n value list
            header_lst, value_lst = self.get_value_list(power_intent_object)
            if debug:
                print(value_lst)
                print(header_lst)
            if len(value_lst) > 1:
                #Write Section name
                csv_fp.write(str(value_lst[0]) + "\n")
                # Get header line (string) and number of fields
                header_line,field_num = self.get_header_line(header_lst)
                # Write header line
                csv_fp.write(header_line)
                # Get number of data lines
                # The length of first field is used here
                line_num = len(value_lst[1])
                # For each data line
                for line in range(line_num):
                    value_line = ""
                    # For each field except the first(section name)
                    for field in range(1, field_num+1):
                        # Concat values for one line
                        value_line += "\"" + str(value_lst[field][line]) +  "\","
                    # Remove redundant "," and add new line at the EoL
                    value_line = value_line[:-1] + "\n"
                    # Write value/data line
                    csv_fp.write(value_line)
                # Add new line to separate sections
                csv_fp.write("\n")



#---------------------------- End of CSV Writer classes --------------------------------
#
#
#
#
#
#
#
#------------------------------ Wrapper classes ----------------------------------------
# Base wrapper class ---
class Upf2Csv():
    def __init__(self, upf_file_name, csv_file_name):
        self.upf_file_name = upf_file_name
        self.csv_file_name = csv_file_name
        # Create csv writer object
        self.csv_wr = CsvWriter(self.csv_file_name)

    # Read UPF file n filter relevant commands
    # Supports: 
    # Limitations:
    # To Do:
    def read_n_filter_upf(self, upf_reader_object):
        self.cmd_lst = upf_reader_object.command_filter()
        # return cmd_lst

    # Extract data from upf commands and store 
    # Supports: 
    # Limitations:
    # To Do:
    def extract_n_store(self, upf_reader_object, power_intent_object):
        for cmd in self.cmd_lst:
            upf_reader_object.read_upf(cmd, power_intent_object)

    # Read from power intent data object and write in csv format 
    # Supports: 
    # Limitations:
    # To Do:
    def write_to_csv(self, power_intent_object):
        self.csv_wr.write_csv(power_intent_object)

    # Read UPF -> Store Power Intent -> Write CSV
    # Supports: 
    # Limitations: Objects passed (self.upf_rd_obj and self.data_obj) to the methods 
    #              inside this method should be defined in child class
    # To Do:
    def read_store_write(self):
        self.read_n_filter_upf(self.upf_rd_obj)
        self.extract_n_store(self.upf_rd_obj, self.data_obj)
        self.write_to_csv(self.data_obj)

# [Variable] - Name Value type - wrapper class
class UserVariableNameValueUpf2Csv(Upf2Csv):
    def __init__(self, upf_file_name, csv_file_name):
        Upf2Csv.__init__(self, upf_file_name, csv_file_name)
        # Create power intent data object
        self.data_obj = UserVariableNameValueData()
        # Create upf reader object
        self.upf_rd_obj = UserVariableNameValueUpfReader(self.upf_file_name)

# [Variable] - Name Pattern type - wrapper class
class UserVariableNamePatternUpf2Csv(Upf2Csv):
    def __init__(self, upf_file_name, csv_file_name):
        Upf2Csv.__init__(self, upf_file_name, csv_file_name)
        # Create power intent data object
        self.data_obj = UserVariableNamePatternData()
        # Create upf reader object
        self.upf_rd_obj = UserVariableNamePatternUpfReader(self.upf_file_name)

# [Power Domain] - wrapper class
class PowerDomainUpf2Csv(Upf2Csv):
    def __init__(self, upf_file_name, csv_file_name):
        Upf2Csv.__init__(self, upf_file_name, csv_file_name)
        # Create power intent data object
        self.data_obj = PowerDomainData()
        # Create upf reader object
        self.upf_rd_obj = PowerDomainUpfReader(self.upf_file_name)

# [Supply] - wrapper class
class SupplyUpf2Csv(Upf2Csv):
    def __init__(self, upf_file_name, csv_file_name):
        Upf2Csv.__init__(self, upf_file_name, csv_file_name)
        # Create power intent data object
        self.data_obj = SupplyData()
        # Create upf reader object
        self.upf_rd_obj = SupplyUpfReader(self.upf_file_name)

    # Read UPF file n filter relevant commands
    # Supports: 
    # Limitations:
    # To Do:
    def read_n_filter_upf(self, upf_reader_object):
        self.create_supply_set_cmd_lst = upf_reader_object.command_filter("create_supply_set ")
        self.create_supply_net_cmd_lst = upf_reader_object.command_filter("create_supply_net ")
        self.create_supply_port_cmd_lst = upf_reader_object.command_filter("create_supply_port ")
        self.connect_supply_net_cmd_lst = upf_reader_object.command_filter("connect_supply_net ")

    # Extract data from upf commands and store 
    # Supports: 
    # Limitations:
    # To Do:
    def extract_n_store(self, upf_reader_object, power_intent_object):
        # for cmd in self.cmd_lst:
        upf_reader_object.read_upf(self.create_supply_set_cmd_lst, self.create_supply_net_cmd_lst, self.create_supply_port_cmd_lst, self.connect_supply_net_cmd_lst, power_intent_object)

# [Switchable Supply] - wrapper class
class SwitchableSupplyUpf2Csv(Upf2Csv):
    def __init__(self, upf_file_name, csv_file_name):
        Upf2Csv.__init__(self, upf_file_name, csv_file_name)
        # Create power intent data object
        self.data_obj = SwitchableSupplyData()
        # Create upf reader object
        self.upf_rd_obj = SwitchableSupplyUpfReader(self.upf_file_name)

#============================ End of Class Definitions  ================================
#
#
#
#
#
#
#
#------------------------------ Wrapper functions ---------------------------------------

# Section level wrapper-------------------

# Top level wrapper ----------------------
def upf2csv(upf_file_name, csv_file_name):
    # [Variable] - Name Value type 
    upf2csv_obj = UserVariableNameValueUpf2Csv(upf_file_name, csv_file_name)  
    upf2csv_obj.read_store_write()
    del upf2csv_obj
    # [Variable] - Name Pattern type
    upf2csv_obj = UserVariableNamePatternUpf2Csv(upf_file_name, csv_file_name)  
    upf2csv_obj.read_store_write()
    del upf2csv_obj
    # [Power Domain] section
    upf2csv_obj = PowerDomainUpf2Csv(upf_file_name, csv_file_name)  
    upf2csv_obj.read_store_write()
    del upf2csv_obj
    # [Supply] section
    upf2csv_obj = SupplyUpf2Csv(upf_file_name, csv_file_name)  
    upf2csv_obj.read_store_write()
    del upf2csv_obj
    # [Switchable Supply] section
    upf2csv_obj = SwitchableSupplyUpf2Csv(upf_file_name, csv_file_name)  
    upf2csv_obj.read_store_write()
    del upf2csv_obj
#------------------------------ End of Wrapper function --------------------------------
#
#
#
#
#
#
#-------------------------------------- Main  ------------------------------------------
if __name__ == '__main__':
    upf2csv("top.upf", "out.csv")
    upf2csv("bitcoin.upf", "out.csv")


#------------------------------------- The End  ----------------------------------------