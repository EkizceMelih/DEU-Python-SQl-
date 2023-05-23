#require libraries
import csv
import re
import json

#MELIH EKIZCE 2020510031 --------- YUSUF SUER 2020510067

class Student:
    def __init__(self, id, name, lastname, email, grade):#Creating Student object
        
        self.id = id
        self.name = name
        self.lastname = lastname
        self.email = email
        self.grade = grade

    def toJSON(self): #require for OBJECT TO json file 
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "grade": self.grade
        }
def extract_logical_operators(text):#extract AND , OR
    operators = ["AND", "OR"]
    extracted_operators = []
    words = text.upper().split()

    for word in words:
        if word in operators:
            extracted_operators.append(word)

    return extracted_operators
def returnColumnOfStudent(columnName,studentIndex):#return column name ID,NAME,LASTNAME,EMAIL,GRADE
    if columnName.casefold()=="id".casefold():#casefold require for noIgnoreCase
        return students[studentIndex].id
    elif columnName.casefold()=="name".casefold():
        return students[studentIndex].name
    elif columnName.casefold()=="lastname".casefold():
        return students[studentIndex].lastname
    elif columnName.casefold()=="email".casefold():
        return students[studentIndex].email
    elif columnName.casefold()=="grade".casefold():
        return students[studentIndex].grade
def applyCoundition(column,operator,value):
    allOperators = ['=', '!=', '<', '>', '<=', '>=', '!<', '!>', 'AND', 'OR'] #all operators
    try:
        value = int(value)
        column = int(column)
    except ValueError:
        pass
   
    if operator in allOperators:
        if operator == '=':#for string operations
            if type(column)==str and type(value)==str:
                column=column.upper()
                value=value.upper()
            return column == value
        elif operator == '!=':#for string operations
            if type(column)==str and type(value)==str:
                column=column.upper()
                value=value.upper()
            return column != value
        elif operator == '<':#for math operations
            return column < value
        elif operator == '>':#for math operations
            return column > value
        elif operator == '<=':#for math operations
            return column <= value
        elif operator == '>=':#for math operations
            return column >= value
        elif operator == '!<':#for math operations
            return column >= value
        elif operator == '!>':#for math operations
            return column <= value
        else:
            return False
    else:
        return False    
no_delete_students=[]      
def evaluate_condition(query,index,mode):
    
    if mode =="SELECT":
        where_index = query.upper().index("WHERE")#finding value of the "WHERE" in the query
        order_index = query.upper().index("ORDER")#finding value of the "ORDER" in the query

    
        where_order_clause = query[where_index + 5:order_index].strip()
        andOr = extract_logical_operators(where_order_clause)
        column_names = []
        operators =  []
        values =  []
        result=False
    
        words = where_order_clause.split()
        i=0
        for word in words: 
            if word.casefold()=="OR".casefold() or word.casefold()=="AND".casefold():
                i=0
                continue
                
            if i==0:
                column_names.append(returnColumnOfStudent(word, index))#Find column names
            elif i==1:
                operators.append(word) #find operators like =,> etc
            elif i==2:
                word = re.sub(r'\W+', '', word) #find value like 'John' or 50(grade)
                values.append(word)     
        
            
            i+=1
        j=0
    
    
        
        if len(andOr)!=0:#if query has AND or OR
            for x in andOr:
                if x == "AND":   # IF HAS AND   
                    result=applyCoundition(column_names[j], operators[j], values[j]) and applyCoundition(column_names[j+1], operators[j+1], values[j+1])
                elif x == "OR": # IF HAS OR   
                    result=applyCoundition(column_names[j], operators[j], values[j]) or applyCoundition(column_names[j+1], operators[j+1], values[j+1])                
                if result ==False:
                     break
                j+=1
        else:
              
               result=applyCoundition(column_names[j], operators[j], values[j])     
 
        
    elif mode =="DELETE": #if mode delete
        
       

        # split query
        query_parts = query.split()
        
        # find index of where word in the query
        where_index = query_parts.index('WHERE')
        
        # take where word's index to query last index
        where_order_clause = ' '.join(query_parts[where_index + 1:])

       

   
        andOr = extract_logical_operators(where_order_clause)
        column_names = []
        operators =  []
        values =  []
        result=False
    
        words = where_order_clause.split()
        i=0
        for word in words:
            if word.casefold()=="OR".casefold() or word.casefold()=="AND".casefold():
                i=0
                continue
                
            if i==0:
                column_names.append(returnColumnOfStudent(word, index))
            elif i==1:
                operators.append(word) 
            elif i==2:
                word = re.sub(r'\W+', '', word)
                values.append(word)     
        
            
            i+=1
        j=0
    
        #DELETE FROM STUDENT WHERE name = ‘John’ and grade <= 20
        
        for x in andOr:
            if x == "AND":       
                result=applyCoundition(column_names[j], operators[j], values[j]) and applyCoundition(column_names[j+1], operators[j+1], values[j+1])
            elif x == "OR":
                result=applyCoundition(column_names[j], operators[j], values[j]) or applyCoundition(column_names[j+1], operators[j+1], values[j+1])                
            if result ==False:
                 break
            
            j+=1
    
    #print(result)
    return result   
#SELECT name FROM STUDENTS WHERE grade > 40 AND name = ‘John’ ORDER BY DSC
students = []
def insert_record(students, values):#
  
    sameIdCheck=0#is like a boolean
    for student in students:
        if int(student.id) == int(values[0]):
            #print("student id:" + student.id +" valude[0]== "+ values[0])
            print("There is another person with the same ID number.")#info message 
            sameIdCheck=1#if found same ID number sameIdCheck=1 like a true
            break  
    if sameIdCheck==0:
        student = Student(values[0], values[1], values[2], values[3],values[4])#fill attributes
        #students.append(student)
        no_delete_students.append(student)
        print("You have added the following person to the system:")#info message 
        print(student.id+" "+student.name+" "+student.lastname+" "+student.email+" "+student.grade)#displaying added person
    sameIdCheck=0


#reading csv file and creating Student Object
with open(r"students.csv", 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # csv to Students object operation
            if row[0]!="id": 
                student = Student(row[0], row[1], row[2], row[3],row[4])#fill attributes
                students.append(student)# adding to Students list
                #no_delete_students.append(student)
            
 
sorted_students_byID=sorted(students,key=lambda x:int(x.id))#sorting operation
def convert(obj):#Json format specific to Student object
    if isinstance(obj, Student):
        return obj.toJSON()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")#throw error message to user

# Saving the json file
    #with open("DATABASE.json", "w") as dosya:
        #json.dump(sorted_students_byID, dosya, default=convert,indent=4)

flag=False #Flag that checks if select insert or delete has been done before exit is pressed   
while True:#a loop that continues until 'EXIT' input
    query = input('Enter a query or "exit" to quit: ')#info message
   
    query_parse=query.upper().split()#split input
    #SELECT PART
    if(query_parse[0] == "SELECT"):#if first word of the query is "SELECT"
        flag=True#Flag that checks if select insert or delete has been done before exit is pressed if query[0]==Select flag=true
        print("-------------SELECT OUTPUTS------------")
        requested=query_parse[1].split(",")#split to, like name,lastname,email etc.
        unsorted_list=[]
        sorted_list=[]             
        for a in range(len(students)):
            
            if evaluate_condition(query,a,"SELECT"):
                for i in range(len(requested)):
                    print(returnColumnOfStudent(requested[i], a), end=" " )
                    
                unsorted_list.append(students[a])#unsorted list the append selecting columns
                #print(students[a].id +" " +students[a].name +" "+ students[a].lastname +" " + students[a].email + " " +students[a].grade)
                print()    
        if "DSC" in query:#if descanding          
            sorted_list= sorted(unsorted_list,key=lambda x:int(x.grade))#sort students from their grades (descanding)
        elif "ASC" in query:#if ascending  
            sorted_list= sorted(unsorted_list,key=lambda x:int(x.grade),reverse=True)#sort students from their grades (ascending)
        print("---------------------------------------") 
    elif(query_parse[0] == "INSERT"):   #INSERT PART
        flag=True
        values_start_index = query.find('VALUES') + 7 #count 7 fro values
        values = query[values_start_index:].replace('(', '').replace(')', '').split(',')#split values like (15000,Ali,Veli,ali.veli@spacex.com,20)
        values = [value.strip() for value in values]
        insert_record(students, values)
     
    elif(query_parse[0]=="DELETE"):#DELETE PART
        deleting_students=[]#Taking the deleting rows
        flag=True
        for a in range(len(students)):
            if evaluate_condition(query,a,"DELETE"):
                deleting_students.append(students[a])               
            else:
                no_delete_students.append(students[a])
        
        print("You deleted these")
       
        for person in deleting_students:
            print(person.id +" " +person.name +" "+ person.lastname +" " + person.email + " " +person.grade)#print the deleted rows
    elif(query_parse[0]=="EXIT"):#if first word of the query is EXIT
        
        print("EXITING...")
        print("Json File is preparing")
        no_delete_students=sorted(no_delete_students,key=lambda x:int(x.id))#sort by the id
        students=sorted(students,key=lambda x:int(x.id))#sort by the id

        if flag==True:
            with open("result.json", "w") as dosya:
                json.dump(no_delete_students, dosya, default=convert, indent=4)#if delete or insert operation using write this json file
            break
        


        
        elif flag==False:
            with open("result.json", "w") as dosya:
                json.dump(students, dosya, default=convert, indent=4)#if no delete or insert operation write this json file
            break
    else:
        print("Wrong Format")#ERROR MESSAGE 




 
