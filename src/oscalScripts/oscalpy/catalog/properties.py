from dataclasses import dataclass, asdict
from uuid import uuid4

# Remark is a string
# 

@dataclass
class Prop:
    name: str # ^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$
    value: str # ^\\S(.*\\S)?$
    ns: str = None # ^[a-zA-Z][a-zA-Z0-9+\\-.]+:.+$
    property_class: str = None # ^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$
    remarks: "list[str]" = None
    uuid: str = str(uuid4()) # ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
    
    def __init__(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        self.name = name
        self.value = value
        self.uuid = uuid
        self.ns = ns
        self.property_class = property_class
        
    def value(self, value=None):
        if value is None:
            return self.value
        self.value = value
        
    def uuid(self, uuid=None):
        if uuid is None:
            return self.uuid
        self.uuid = uuid
        
    def ns(self, ns=None):
        if ns is None:
            return self.ns
        self.ns = ns
        
    def property_class(self, property_class=None):
        if property_class is None:
            return self.property_class
        self.property_class = property_class
        
    def add_remark(self, remark):
        self.remarks.append(remark)
         
    def __dict__(self):
        return {"class" if k == 'property_class' else k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Part:
    name: str
    title: str = None
    prose: str = None
    ns: str = None
    id: str = None
    part_class: str = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    
    def __init__(self, name, title=None, prose=None, ns=None, part_class=None, id=None):
        self.name = name
        self.id = id
        self.ns = ns
        self.part_class = part_class
        self.title = title
        self.prose = prose
        
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
    
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
        
    def id(self, id=None):
        if id is None:
            return self.id
        self.id = id
        
    def ns(self, ns=None):
        if ns is None:
            return self.ns
        self.ns = ns
        
    def part_class(self, part_class=None):
        if part_class is None:
            return self.part_class
        self.part_class = part_class    
    
    def title(self, title=None):
        if title is None:
            return self.title
        self.title = title
        
    def prose(self, prose=None):
        if prose is None:
            return self.prose
        self.prose = prose
        
    def __dict__(self):
        return {"class" if k == 'part_class' else k: v for k, v in asdict(self).items() if v is not None}
        
@dataclass
class Link:
    href: str # url like: ^https?://.+ 
    rel: str = None # ^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$
    media_type: str = None # ^\\S(.*\\S)?$
    text: str = None
    
    def __init__(self, href, rel=None, media_type=None, text=None):
        self.href = href
        self.rel = rel
        self.media_type = media_type
        self.text = text
        
    def rel(self, rel=None):
        if rel is None:
            return self.rel
        self.rel = rel
    
    def media_type(self, media_type=None):
        if media_type is None:
            return self.media_type
        self.media_type = media_type
        
    def text(self, text=None):
        if text is None:
            return self.text
        self.text = text 
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class ConstraintTest:
    expression: str
    remarks: list = None # list of strings
    
    def __init__(self, expression, remark=None):
        self.expression = expression
        if remark is not None:
            self.remarks = []
            self.remarks.append(remark)
    
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Constraint:
    tests: "list[ConstraintTest]"
    description: str = None
    
    def __init__(self, expression, test_remark=None, description=None):
        self.description = description
        self.tests = []
        self.add_test(expression, test_remark)
        
    def description(self, description=None):
        if description is None:
            return self.description
        self.description = description
        
    def add_test(self, expression, remark=None):
        self.tests.append(ConstraintTest(expression, remark))
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Selection:
    how_many: str
    choice: list
    
    def __init__(self, how_many, *choices) -> None:
        if how_many not in ["one", "one-or-more"]:
            raise ValueError("how_many must be either 'one' or 'one-or-more'")
        self.how_many = how_many
        self.choice = list(choices)
        
    def choose(self, *args):
        choices = list(args)
        if self.how_many == "one":
            if len(choices) > 1:
                raise ValueError("how_many is 'one' but multiple choices were provided")
        self.choice = choices
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Guideline:
    prose: str
    
    def __init__(self, prose) -> None:
        self.prose = prose

@dataclass
class Param:
    id: str
    param_class: str = None
    depends_on: str = None
    label: str = None
    usage: str = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    constraints: "list[Constraint]" = None
    guidelines: "list[Guideline]" = None
    values: "list[str]" = None
    select: Selection = None
    
    def __init__(self, id, label=None, param_class=None, depends_on=None, usage=None):
        self.id = id
        self.label = label
        self.param_class = param_class
        self.depends_on = depends_on
        self.usage = usage
        
    def add_constraint(self, expression, description=None, remark=None):
        if self.constraints is None:
            self.constraints = []
        self.constraints.append(Constraint(expression, remark, description))
        
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
    
    def add_link(self, href, rel, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel,media_type, text))
    
    def add_guideline(self, prose):
        if self.guidelines is None:
            self.guidelines = []
        self.guidelines.append(Guideline(prose))
        
    def add_value(self, value):
        if self.values is None:
            self.values = []
        self.values.append(value)
        
    def __dict__(self):
        return {"class" if k == 'param_class' else k: v for k, v in asdict(self).items() if v is not None}