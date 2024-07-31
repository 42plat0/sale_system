import csv, os
from datetime import datetime, timedelta


DB_DIR_NAME = "database"
USERS_FILE = "users.csv"
SALES_FILE = "sales.csv"
EMPLOYEE_REPORT = "employee_report.csv"

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + f"/{DB_DIR_NAME}/"

REPORT_ADMIN = "admin_efficiency_report.csv"
efficiency_report_path = BASE_DIR + REPORT_ADMIN


SALE_REPORT = "admin_sale_report.csv"
sale_report_path = BASE_DIR + SALE_REPORT


users_path_csv = BASE_DIR + USERS_FILE
user_list = [
   {
    "id": ["int", 1234],
    "password":["str", "worker"],
    "name":["str", "John Salad"],
    "is_admin":["bool", False],
   },
   {
    "id":["int", 4321],
    "password":["str","worker"],
    "name":["str", "Brown Lameass"],
    "is_admin":["bool", False],
   },
   {
    "id": ["int", 3333],
    "password":["str", "worker"],
    "name":["str", "Benis Penis"],
    "is_admin":["bool", False],
   },
   {
    "id":["int", 9999],
    "password":["str", "admin"],
    "name":["str", "Donald Peterson"],
    "is_admin":["bool", True],
   },
]


sales_path_csv = BASE_DIR + SALES_FILE
sales_list = [
     {
        "employee_id":["int", 1],
        "product_name":["str", "Jumper"],
        "total_sum":["float", 32.00],
    }
]


employee_report_path_csv = BASE_DIR + EMPLOYEE_REPORT

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
no_time = datetime.strptime(now, "%Y-%m-%d %H:%M:%S") - datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
employee_report_list = [
    {
        "employee_id":["int", 1234],
        "date_logged_in": ["str", now],
        "date_logged_out": ["str", now],
        "session_time": ["str", no_time],
        "sale_total_usd": ["float", 32.00],
    }
]


class App():

    @staticmethod
    def create_database_directory():
        if not os.path.isdir(BASE_DIR):
            os.mkdir(BASE_DIR)

    # @staticmethod
    # def create_database(path, )
    
    @staticmethod
    def login():
        try:
            username_id = input("Prisijungimo id: ")
            password = input("Slaptazodis: ")

            return {"id": ["int", username_id], "password": ["str", password]}
        except Exception as e:
            print(e, "error was found")
    

    @staticmethod
    def menu_prompt(menu_text):
        max_menu_index = len(menu_text)
        for menu_opt in menu_text.values():
            print(menu_opt)
        try:
            choice = int(input("> "))

            if choice > max_menu_index:
                raise ValueError
            
            return choice

        except Exception:
            print("Neteisinga ivestis")
            return App.menu_prompt(menu_text)
    
    @staticmethod
    def reprompt():
        print("Ar norite testi? 1/0")
        try:
            choice = int(input("> "))
            if choice == 1:
                return True
            elif choice == 0:
                return False
            else:
                raise Exception
            
        except Exception:
            print("Neteisinga ivestis")
            return App.reprompt()
    
    @staticmethod
    def dynamic_input_menu(input_fields, dynamic_input=None):
        # generate input menu dynamically
        # keliose vietose naudojam su skirtingais fields adminui ir darbuotojui

        # usage:
        '''
        input_fields = [
            { 
                "input text ": { "key name": "" } # means that type is str or not important
            },
            { 
                "input text ": { "key name": "type" } example : "Pardavimo suma: ":{"sale_sum" : float} #be kabuciu type!
            },
            {
                None: {"employee_id": int} # None reiskia, kad inputo neprasome userio ir jy gauname kitaip (pvz per objekta)
            }
        ]
        '''
        output = {}

        for field in input_fields:
            for input_text, key_and_type in field.items():
                if input_text:
                    print(input_text)
                    for key, input_type in key_and_type.items():
                        if input_type and not input_text == None:
                            try:
                                user_value = input_type(input("> "))
                            except ValueError:
                                print("Neteisinga ivestis!")
                                return App.dynamic_input_menu(input_fields, dynamic_input)
                            except Exception as e:
                                print(e)
                                return App.dynamic_input_menu(input_fields, dynamic_input)
                        else:
                            user_value = input("> ")
                    
                        output[key] = user_value
                else:
                    for key, input_type in key_and_type.items():
                        output[key] = input_type(dynamic_input)

        return output or None


class Database():
    def __init__(self, path, data_list, create_instantly=True):
        self.path = str(path) # todo ar reik?
        self.data_list = data_list
        
                
        if create_instantly and data_list:
            self.__create_db_base__()
            self.__create_database__()
            self.__create_dtypes__()
        else:
            self.__create_db_base__()
            self.__create_dtypes__()
    

    def get_keys(self):
        return
    
    def __create_db_base__(self):
        data_list = []
        data_key_type = {}

        for data in self.data_list:
            data_point = {}
            for key, type_and_value in data.items():
                data_key_type[key] = type_and_value[0]
                data_point[key] = type_and_value[1]
            data_list.append(data_point)
        
        self.keys = data_list[0].keys()
        self.data_list = data_list
        self.data_key_type = data_key_type

    def __create_database__(self):    
        if not os.path.isfile(self.path):
            #make csv file for each db when object is created
            with open(self.path, "w", encoding="utf-8", newline="") as output_file:
                writer = csv.DictWriter(output_file, fieldnames=self.keys)
                writer.writeheader()
                writer.writerows(self.data_list)
    
    def __create_dtypes__(self):
        self.dtypes = {}
        for key, dtype in self.data_key_type.items():
            self.dtypes[key] = dtype

#todo merge with database
class CsvHelper():

    def __init__(self, file_path, dtypes=None, data_class=None ,newline="", encoding="utf-8"):
        self.file_path = file_path
        self.dtypes = dtypes
        self.data_class = data_class
        self.newline = newline
        self.encoding = encoding


    def obj_to_dict(self, obj):
        cls = globals()[self.data_class]
        return cls(**obj)


    def apply_datatype(self, row):
        for col_key, col_type in self.dtypes.items():
            if col_type == "int":
                row[col_key] = int(row[col_key])
            elif col_type == "float":
                row[col_key] = float(row[col_key])
            elif col_type == "bool":
                row[col_key] = row[col_key] in "True"

        return row


    def is_object(self, row):
        if self.data_class is not None:
            return isinstance(row, globals()[self.data_class])


    def read(self):
        with open(self.file_path, "r", encoding=self.encoding, newline=self.newline) as file:
            rows = list(csv.DictReader(file))
            for row in rows:
                if self.dtypes:
                    row = self.apply_datatype(row)
                if self.data_class:
                    row = self.obj_to_dict(row)
            return rows


    def save(self, data, keys):
        with open(self.file_path, "w", encoding=self.encoding, newline=self.newline) as output_file:
            writer = csv.DictWriter(output_file, fieldnames=keys)
            writer.writeheader()

            for row in data:
                if self.is_object(row):
                    row = row.__dict__

                writer.writerow(row)


    def delete(self):
        os.remove(self.file_path)


class Auth():

    @staticmethod
    def log_user_in(users, login_info):
        for user in users:
            if user["id"] == int(login_info["id"][1]) and user["password"] == login_info["password"][1]:
                return user
        
        return None

    @staticmethod
    def get_user_name(users, login_id):
        for user in users:
            if user["id"] == login_id:
                return user["name"]

    @staticmethod
    def check_user_privileges(login_info):
        return login_info["is_admin"]


class Employee():

    def __init__(self, id):
        self.id = id 

        self.date_logged_in = None
        self.date_logged_out = None
        self.session_time = 0
        self.sale_total_usd = 0

        self.menu = {
            "register_sale": "1. Uzregistruoti pardavima",
            "exit_menu": "2. Atsijungti",
        }

        self.sales_made = []

        self.__set_logged_in_date__()


    def __set_logged_in_date__(self):
        self.date_logged_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    def set_logged_out_date(self):
        self.date_logged_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calculate_session_time(self):
        self.session_time = datetime.strptime(self.date_logged_out, "%Y-%m-%d %H:%M:%S") - datetime.strptime(self.date_logged_in, "%Y-%m-%d %H:%M:%S")

    def populate_sales(self, product):
        self.sales_made.append(product)


    def log_sale(self):

        log_sale_fields = [
            {
                None: {"employee_id": int}
            },
            {
                "Prekes pavadinimas: ": {"product_name": ""},
            },
            {
                "Pardavimo suma: ":{ "total_sum" : float}
            }
        ]

        sale = App.dynamic_input_menu(log_sale_fields, self.id)
        self.sales_made.append(sale)

    def update_employee_after_logging_sale(self):
        for sale in self.sales_made:
            self.sale_total_usd += sale["total_sum"] 

        self.set_logged_out_date()
        self.calculate_session_time()

    def return_sale_list(self):
        self.update_employee_after_logging_sale()

        return self.sales_made


class Admin():

    def __init__(self, id):
        self.id = id

        self.menu = {
            "get_employee_efficiency_log": "1. Darbuotojai pagal efektyvuma",
            "get_sold_products_log": "2. Pardavimai",
            "create_user": "3. Uzregistruoti nauja vartotoja",
            "exit_menu": "4. Atsijungti",
        }

        self.efficiency_sort_menu = {
            "session_time": "1. Isrusiuoti pagal darbo laika",
            "usd_per_h": "2. Isrusiuoti pagal pardavimo suma per valanda",
        }

        self.created_user_list = []
        

    def get_each_employee_report(self, employee_report):
        all_employee_ids_in_report = []

        each_employee_report = []

        # get all employees once
        for row in employee_report:
            if row["employee_id"] not in all_employee_ids_in_report:
                all_employee_ids_in_report.append(row["employee_id"])

        # create dict for each employee to modify
        for employee in all_employee_ids_in_report:
            each_employee_report.append({
                "name":["str", ""],
                "id":["int", employee],
                "session_time":["timedelta", timedelta(hours=0, minutes=0, seconds=0)],
                "sale_total_usd":["float",0] 
            })
        
        # add session time and sale total to each employee dict
        for index, employee_id in enumerate(all_employee_ids_in_report):
            for report_row in employee_report:
                if employee_id == report_row["employee_id"]:
                    each_employee_report[index]["sale_total_usd"][1] += report_row["sale_total_usd"]
                    employee_session_time = datetime.strptime(report_row["session_time"], "%H:%M:%S").time()
                    session_time = timedelta(
                        hours=employee_session_time.hour, 
                        minutes=employee_session_time.minute, 
                        seconds=employee_session_time.second
                    )
                    each_employee_report[index]["session_time"][1] += session_time

        return each_employee_report


    def get_employee_efficiency_log(self, employee_report, users, sort_by=1):
        employee_report = self.get_each_employee_report(employee_report)

        # add name to report and delete id 
        for employee in employee_report:
            employee["name"][1] = Auth.get_user_name(users, employee["id"][1])
            employee.pop("id")
            employee["sale_total_usd"] = [employee["sale_total_usd"][0], round(employee["sale_total_usd"][1], 2)]

        # # TODO CHECK IF WORKS WITH MORE USERS
        # # sort by time spent
        if sort_by == 1:
            for index, employee in enumerate(employee_report):
                for i in range(index + 1, len(employee_report)):
                    if employee_report[i]["session_time"][1].seconds > employee_report[index]["session_time"][1].seconds:
                        employee_report[i], employee_report[index] = employee_report[index], employee_report[i]
        
        # sort by usd/hour sold
        elif sort_by == 2:
            for index, employee in enumerate(employee_report):
                for i in range(index + 1, len(employee_report)):
                    if employee_report[i]["sale_total_usd"][1] / (employee_report[i]["session_time"][1].seconds / 3600) > employee_report[index]["sale_total_usd"][1] / (employee_report[index]["session_time"][1].seconds / 3600):
                        employee_report[i], employee_report[index] = employee_report[index], employee_report[i]

        return employee_report
    

    def get_sold_products_log(self, sales_report, users):
        report = []
        for row in sales_report:
            # create proper report with names without id's
            report.append({
                "name":["str", Auth.get_user_name(users, row["employee_id"])],
                "product_name":["str",row["product_name"]],
                "total_sum":["float",row["total_sum"]],
            })
        
        # sort by price high..low
        for index, sale in enumerate(report):
            for i in range(index + 1, len(report)):
                if report[i]["total_sum"][1] > report[index]["total_sum"][1]:
                    report[i], report[index] = report[index], report[i]
                
        return report


    def create_user(self, users):
        get_new_user_fields = [
            {
                "Vartotojo prisijungimo ID: " : {"id": int}
            },
            {
                "Vartotojo slaptazodis: " : {"password": ""}
            },
            {
                "Vartotojo vardas: ": {"name": ""}
            },
            {
                "Ar vartotojas yra administratorius? (Taip = 1, Ne = 0)": {"is_admin": int}
            }
        ]

        new_user = App.dynamic_input_menu(get_new_user_fields, self.id) if not None else None

    
        if new_user["is_admin"] != 1 and new_user["is_admin"] != 0:
            print("Neteisinga ivestis!")
            return self.create_user(users)
        else:
            new_user["is_admin"] = bool(new_user["is_admin"])

        #check if user already exist
        for user in users:
            if user["id"] != new_user["id"]:
                self.created_user_list.append(new_user)
                break
            else:
                print()
                print("Tokiu prisijungimo ID vartotojas jau egzistuoja!")
                for key, value in user.items():
                    if key != "password":
                        print(f"{key.upper()} : {value}")
                print()
                return


    def return_new_user_list(self):
        return self.created_user_list


class Employee_Report():

    @staticmethod
    def print_summary(employee):
        for stat, value in employee.__dict__.items():
            print(stat.upper(), value)


    @staticmethod
    def parse_report(employee, fieldnames):
        #create dict with proper fieldnames
        employee_fieldnames = list(employee.__dict__.values())
           
        for index, key in enumerate(fieldnames):
            fieldnames[key] = employee_fieldnames[index]
        
        return fieldnames


class Report():
    
    def __init__(self, report, database, database_file):
        self.report = report
        self.database = database
        self.database_file = database_file

        self.menu_text = {
            "terminal": "1. Isspausdinti ataskaita terminale",
            "save": "2. Issaugoti csv faila",
            "delete": "3. Istrinti csv faila",
            "exit_menu": "4. Atgal",
        }
    
    def print(self):
        for index, value in enumerate(self.report):
            print(f"\n{index+1}", end=". ")
            for key, value in value.items():
                if key == "name":
                    key = "Darbuotojo vardas:"

                elif key == "product_name":
                    key = "   " + "Produktas:"
                
                elif key == "total_sum":
                    key = "   " + "Suma:"
                    value[1] = str(value[1]) + " $"
                
                elif key == "session_time":
                    key = "   " + "Darbo laikas:"
                
                elif key == "sale_total_usd":
                    key = "   " + "Pardavimų suma:"
                    value[1] = str(value[1]) + " $"
                print(key, value[1])
        print()
    
    def save_to_csv(self):
        try:
            self.database.__create_database__()
        except Exception as e:
            print(e)


    def delete_csv(self):
        try:
            self.database_file.delete()
        except FileNotFoundError:
            print("Csv failo nesukurete")
        except Exception as e:
            print(e)


def main():
    # seed data
    global user_list, sales_list, employee_report_list
    #create starting files
    App().create_database_directory()
    users_db = Database(users_path_csv, user_list)
    sales_db = Database(sales_path_csv, sales_list)
    employee_report_db = Database(employee_report_path_csv, employee_report_list)
    
    users_file = CsvHelper(
        users_db.path,
        users_db.dtypes
    )

    # get employee_report
    employee_report_file = CsvHelper(
        employee_report_db.path,
        employee_report_db.dtypes
        )
    employee_report_list = employee_report_file.read()

    # get sale list
    sales_file = CsvHelper(
        sales_db.path,
        sales_db.dtypes
        )
    sales_list_db = sales_file.read()
    
    # get user list
    user_list_db = users_file.read()

    #user logs in
    user = App.login() 

    # check if user exists
    user = Auth.log_user_in(user_list_db, user) # user list, current user
    
    #todo negrazina menu!
    if user is not None:
        # check user privileges
        if Auth.check_user_privileges(user):
            # if admin give admin menu
            print("Hello, Admin!")
            user = Admin(user["id"])
        else:
            # if employee give its menu
            user = Employee(user["id"])
    else:
        print("Neteisingas prisijungimas")
        return

    #prompt user for choice
    while True:

        menu_choice = App.menu_prompt(user.menu)

        if isinstance(user, globals()["Admin"]): 

            # efficiency report
            if menu_choice == 1:
                efficiency_menu_choice = App.menu_prompt(user.efficiency_sort_menu)

                #list
                report_list = user.get_employee_efficiency_log(employee_report_list, user_list_db, sort_by = efficiency_menu_choice)
                # create db
                efficiency_report_db = Database(efficiency_report_path, report_list, create_instantly=False)
                efficiency_report_file = CsvHelper(
                    efficiency_report_db.path,
                    efficiency_report_db.dtypes
                )
                # create report
                report = Report(report_list, efficiency_report_db, efficiency_report_file)

                # give report menu
                while True:
                    efficiency_menu_choice = App.menu_prompt(report.menu_text)

                    if efficiency_menu_choice == 1:
                        report.print()
                    
                    elif efficiency_menu_choice == 2:
                        report.save_to_csv()
                    
                    elif efficiency_menu_choice == 3:
                        report.delete_csv()
                        
                    elif efficiency_menu_choice == 4:
                        break
            
            # sale report
            elif menu_choice == 2:
                #list 
                report_list = user.get_sold_products_log(sales_list_db, user_list_db)
                # create db
                sale_report_db = Database(sale_report_path, report_list, create_instantly=False)
                sale_report_file = CsvHelper(
                    sale_report_db.path,
                    sale_report_db.dtypes
                )
                # create report
                report = Report(report_list, sale_report_db, sale_report_file)
                
                # give report menu
                while True:
                    sale_menu_choice = App.menu_prompt(report.menu_text)

                    if sale_menu_choice == 1:
                        report.print()
                    
                    elif sale_menu_choice == 2:
                        report.save_to_csv()
                    
                    elif sale_menu_choice == 3:
                        report.delete_csv()
                        
                    elif sale_menu_choice == 4:
                        break

            # create user  
            elif menu_choice == 3:
                while True:
                    # TODO kartoijasi
                    user.create_user(user_list_db)

                    if not App.reprompt():
                        new_users_list = user.return_new_user_list()
                        break

                if new_users_list:
                    for user in new_users_list:
                        user_list_db.append(user)
                
                    users_file.save(user_list_db, users_db.keys)

            else:
                break
        else:
            # log sales 
            if menu_choice == 1:
                while True:
                    user.log_sale()

                    if not App.reprompt():
                        # make product list to save
                        employee_sales = user.return_sale_list()
                        break
                
                if employee_sales:
                    #append sold products to existing csv file data
                    for sale in employee_sales:
                        sales_list_db.append(sale)

                # save updated sold product list to csv file  
                sales_file.save(sales_list_db, sales_db.keys)

                # todo unique!
                report_card = Employee_Report.parse_report(user, employee_report_db.dtypes) #todo nudefinint fieldnames
                employee_report_list.append(report_card)
                employee_report_file.save(employee_report_list, employee_report_db.keys)
            
            else:
                break


if __name__ == "__main__":
    main()



#todo buggs!!
# logina double sale
# negrazina i meniu admin sukurus useri
# 

#paprasyti failo pavadinimo

# klase table'ui seed User)list
# todo logged_out seed data NONE
# todo _create_database_directory 


# menu atskira klse nes universali funkcija!
# todo menu_prompt galetu atskira klase tureti
# todo reprompt 
# todo dynamic_input_menu 
    # validatoriu klasei required: True

# Databse klase
# todo Database name -> FileDatabase
# todo metodu pavadinimai db_base database

# Auth 
#todo loadina savo userius
#todo logged_user local variable kuri mes aglim pasiekt veliua (user NAME)


#employee
#todo su adminu gali dalintis bendra info loggedin/out password ir t.t.
#todo date format i bendra varaible
#todo log sales atskirai i faila o ne kartu


#admin
#todo admin ir adminmenu interface turi buti atskirai
#todo logas yra adminas, menu interface dalis
#atskirti interafce nuo data dalies
#todo konstantos vietoj sort_by=1, sukurti pacioje klaseje
#todo atskiros funkcijos sortinimui
#new_user["is_admin"] not in [0, 1]

#report
#todo patisklinti kokie reportai

#gali nelikti helperio

#todo app.init()
# database > csv.helper

#todo menu atskira useriui ir adminui