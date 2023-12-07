from dataclasses import dataclass, asdict
import re
from uuid import uuid4
from .metadata import Metadata, BackMatter
from .properties import Prop, Link, Param, Part

#recursively remove None values from dict
def clean(d):
    if isinstance(d, dict):
        return {k: clean(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [clean(v) for v in d]
    else:
        return d

def recursively_change_key(obj: dict | list, old: str | list[str], new: str) -> dict | list:
    if isinstance(obj, dict):
        for k, v in obj.copy().items():
            if isinstance(old, list):
                for o in old:
                    if k == o:
                        obj[new] = obj.pop(o)
            elif k == old:
                obj[new] = obj.pop(old)
            recursively_change_key(v, old, new)
    elif isinstance(obj, list):
        for i in obj:
            recursively_change_key(i, old, new)
    return obj

def clean_dict(obj):
    clean_obj = clean(dict(obj))
    # change aliased class json key for objects to 'class'
    return recursively_change_key(clean_obj, ['ctrl_class', 'part_class', 'property_class', 'param_class'], 'class')

@dataclass
class Control:
    id: str
    title: str
    ctrl_class: str = None
    params: "list[Param]" = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    parts: "list[Part]" = None
    controls: "list[Control]" = None
    
    def __init__(self, id, title, ctrl_class=None):
        self.id = id
        self.title = title
        self.ctrl_class = ctrl_class
    
    def add_param(self, id, label=None, param_class=None, depends_on=None, usage=None):
        if self.params is None:
            self.params = []
        new = Param(id, label, param_class, depends_on, usage)
        self.params.append(new)
    
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
    
    def add_prop(self, name, value, ns=None, property_class=None, uuid=None):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
        
    def add_part(self, name, title=None, prose=None, ns=None, part_class=None, id=None):
        if self.parts is None:
            self.parts = []
        self.parts.append(Part(name, title, prose, ns, part_class, id))
        
    def add_control(self, id, title, ctrl_class=None):
        if self.controls is None:
            self.controls = []
        new = Control(id, title, ctrl_class)
        self.controls.append(new)
        
    def __dict__(self):
        return {"class" if k == 'ctrl_class' else k: v for k, v in asdict(self).items() if v is not None}
    

@dataclass
class Group:
    title: str
    id: str = None
    group_class: str = None
    params: "list[Param]" = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    parts: "list[Part]" = None
    groups: "list[Group]" = None
    controls: "list[Control]" = None
    
    def __init__(self, title, id=None, group_class=None):
        self.id = id
        self.title = title
        self.group_class = group_class            
        
    def add_param(self, id, label=None, param_class=None, depends_on=None, usage=None):
        if self.params is None:
            self.params = []
        new = Param(id, label, param_class, depends_on, usage)
        self.params.append(new)
        
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
        
    def add_link(self, href, rel, media_type, text):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
    
    def add_part(self, name, title, prose, ns, part_class, id):
        if self.parts is None:
            self.parts = []
        self.parts.append(Part(name, title, prose, ns, part_class, id))
        
    def add_group(self, title, id=None):
        if self.groups is None:
            self.groups = []
        new = Group(title, id)
        self.groups.append(new)
        
    def add_control(self, id, title, ctrl_class=None):
        if self.controls is None:
            self.controls = []
        new = Control(id, title, ctrl_class)
        self.controls.append(new)
         
    def __dict__(self):
        return {"class" if k == 'group_class' else k: v for k, v in asdict(self).items() if v is not None}
    
@dataclass
class Catalog:
    uuid: str
    metadata: Metadata
    params: "list[Param]" = None
    controls: "list[Control]" = None
    groups: "list[Group]" = None
    back_matter: BackMatter  = None      
    
    def __init__(self, title, version, oscal_version, uuid=str(uuid4())):
        self.uuid = uuid
        self.metadata = Metadata(title, version, oscal_version)

    def add_param(self, id, label=None, param_class=None, depends_on=None, usage=None):
        if self.params is None:
            self.params = []
        new = Param(id, label, param_class, depends_on, usage)
        self.params.append(new)
        
    def add_control(self, id, title, ctrl_class=None):
        if self.controls is None:
            self.controls = []
        new = Control(id, title, ctrl_class)
        self.controls.append(new)
    
    def add_group(self, title, id, group_class=None):
        if self.groups is None:
            self.groups = []
        new = Group(title, id, group_class)
        self.groups.append(new)
        
    def add_back_matter(self, resource_uuid, title=None, description=None):
        if self.back_matter is None:
            self.back_matter = BackMatter()
        self.back_matter.add_resource(resource_uuid, title, description)
        
    def as_dict(self):
        return asdict(self, dict_factory=clean_dict)
    
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}