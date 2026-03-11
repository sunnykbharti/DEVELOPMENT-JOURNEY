from jinja2 import Template as Tj
output="""
<!DOCTYPE html>
<body>
    <ul>
    {%for item in sl|sort%}
        <li>{{item}}</li>
    {%endfor%}
    </ul>
</body>
</html>
"""
l=[5,4,3,2,1]
t=Tj(output)
output=t.render(sl=l)
print(output)