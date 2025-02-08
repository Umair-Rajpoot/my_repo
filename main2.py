from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
from typing import Optional,List
import re

app=FastAPI()

class Student_registeration(BaseModel):
    name:str
    email:EmailStr
    age:int
    course:List[str]

def validate_student(student):
    if len(student.name) < 1 or len(student.name) > 50:
        return("Invalid name format")
    if student.age < 18 or student.age >30:
        return("Age must be between 18 and 30")
    if len(student.course) < 1 or len(student.course) > 5:
        return("Courses must be between 1 and 5")
    if len(set(student.course)) != len(student.course):
        return("The name of the courses cannot be same")
    for course in student.course:
        if len(course) <5 or len(course) > 30:
            return("Each course name must be 5-30 characters long")
    return None

class StudentEmailUpdate(BaseModel):
    email: EmailStr 

@app.get("/students/{student_id}")
def get_student(student_id:int , include_grade:bool =False , semester: Optional[str]=None):
    if student_id < 1001 or student_id > 9998:
        return {"error": "Student id must be between 1001 and 9998"}
    if semester and not re.match(r'^(Fall|Spring|Summer)\d{4}$',semester):
        return{"error": "Semester format is invalid"}
    return{"student_id":student_id,"include_grade":include_grade,"semester":semester}

@app.post("/students/register")
def register_student(student:Student_registeration):
    error=validate_student(student)
    if error:
        return{"error":error}
    return{"message":"Student registered successfully","student":student}

@app.put("/students/{student_id}/email")
def update_student_email(student_id :int,email_update:StudentEmailUpdate):
    if student_id < 1001 or student_id >9998:
        return{"error":"Student must be between 1001 and 9998"}
    return{"message":"Student email updated successfully","student_id":student_id,"email":email_update.email}
               




