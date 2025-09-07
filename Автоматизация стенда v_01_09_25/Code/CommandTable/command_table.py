import configparser
import pandas as pd
import time
import threading

class ABSTRACT_DEFAULT_COMMAND_TO_FUNCTOR:
    def __getitem__(self, key):
        return self.pass_function

    def pass_function(self, *args, **kwargs):
        return

DEFAULT_COMMAND_TO_FUNCTOR = ABSTRACT_DEFAULT_COMMAND_TO_FUNCTOR()



class CommandTable(object):
    def __init__(self, on_finish = (lambda: print("Table Execution finished")),
                 command_to_functor: {} = DEFAULT_COMMAND_TO_FUNCTOR):
        self.command_to_functor = command_to_functor
        self.commands = None
        self.my_thread = None
        self.is_active_execution = False
        self.on_finish = on_finish

    def exec_time_sleep(self, time_amount):
        flag = True
        try:
            k = float(time_amount.split(";")[0])
        except Exception as e:
            print(e)
            flag = False
        if flag:
            time.sleep(k)

    def start_table_execution(self):
        self.my_thread = threading.Thread(target = self.execute_table)
        self.is_active_execution = True
        self.my_thread.start()
            
    def execute_table(self):
        if self.commands is None:
            print("ABORT CommandTable.execute_table: CommandTable.commands is None.")
            return
        for index, row in self.commands.iterrows():
            key = self.commands["Command_Name"][index]
            if key == "TimeSleep":
                self.exec_time_sleep(row["Command_Args"])
            else:
                try:
                    self.command_to_functor[key](row["Command_Args"])
                except Exception as e:
                    print(">>",e)
            if not(self.is_active_execution):
                break
        self.is_active_execution = False
        self.on_finish()
        return

    def interrupt_table_execution(self):
        if not(self.is_active_execution):
            return
        self.is_active_execution = False
        self.my_thread.join()
        self.my_thread = None
        print("CommandTable interrupted")

    def wait_execution_finish(self):
        if not(self.is_active_execution):
            return
        self.my_thread.join()
        self.my_thread = None

    def add_commands_from_csv(self, filename):
        self.commands = pd.DataFrame(columns = ["Command_Name", "Command_Args"])

        file = open(filename)
        strings = file.readlines()
        for s in strings[1:]:
            tmp = s.split(";", maxsplit = 2)
            index = int(tmp[0])
            func_name = tmp[1]
            func_args_str = tmp[2][:-1]
            self.commands.loc[index] = [func_name,func_args_str]

    def clear_commands(self):
        self.commands = None


def read_ini(config_file, on_finish = (lambda: print("Table Execution finished")),
                 command_to_functor: {} = DEFAULT_COMMAND_TO_FUNCTOR):
    config = configparser.ConfigParser()
    config.read(config_file)
    if config["Validation"]["Type"] != "CommandTable":
        print("invalid config validation for CommandTable")
        return None
    command_table = CommandTable(on_finish = on_finish,
                                 command_to_functor = command_to_functor)
    command_table.commands = pd.DataFrame(columns = ["Command_Name", "Command_Args"])
    for item in config.items("Commands"):
        tmp = item[1].split(" ", maxsplit = 1)
        index = int(item[0])
        func_name = tmp[0]
        func_args_str = tmp[1]
        command_table.commands.loc[index] = [func_name, func_args_str]
    return command_table



def read_csv(filename, on_finish = (lambda: print("Table Execution finished")),
                 command_to_functor: {} = DEFAULT_COMMAND_TO_FUNCTOR):
    command_table = CommandTable(on_finish = on_finish,
                                 command_to_functor = command_to_functor)
    command_table.add_commands_from_csv(filename)
    return command_table

if __name__ == "__main__":

    def call_function(x):
        print("CallFunction called")

    def set_korad_UIT(s):
        print("*"+s+"*")

    d = {"CallFunction" : call_function, "Korad set U I T" : set_korad_UIT}

    c = read_csv("CommandTable_example2.csv", command_to_functor = d)
    print(c.commands)
    c.start_table_execution()
    c.wait_execution_finish()

