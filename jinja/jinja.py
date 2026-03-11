from string import Template as Ts
from jinja2 import Template as Tj
# print("Hello World")

# name="Sunny"
# course="Btech"
# degree="Bachelors"

# values={"name":"Sunny","course":"Btech","degree":"Bachelors"}
# multi_string="""
# <h1>My name is $name</h1>
# <h2>My course is $course</h2>
# <h2>I am pursuing $degree</h2>
# """
# multi_jinja="""
# <h1>My name is {{name}}</h1>
# <h2>My course is {{course}}</h2>
# <h2>I am pursuing {{degree}}</h2>
# """
# temps=Ts(multi_string)
# tempj=Tj(multi_jinja)

# outputs=temps.substitute(values)
# outputj=tempj.render(values)

# print(outputs)
# print(outputj)

# data=[
#     {"id":1,"name":"Sunny","course":"Btech"},
#     {"id":2,"name":"Aniket","course":"RT Technician"},
#     {"id":3,"name":"Shubham","course":"Diploma"}    
# ]

# jtemp="""
# {% for item in data %}
#     {% if item!="a" %}
#         {{item["name"]}}
#         {{item["course"]}}
#     {%endif%}
# {%endfor%}
# """
# r=Tj(jtemp)
# out=r.render(data=data)
# print(out)

# jtemp="""
# {% for i in range(5)%}
#     {{i}}
# {%endfor%}    
# """
# r=Tj(jtemp)
# out=r.render()
# print(out)

raw="""
    <ul>
    {% for item in range(10) %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
"""
r=Tj(raw)
out=r.render()
print(out)