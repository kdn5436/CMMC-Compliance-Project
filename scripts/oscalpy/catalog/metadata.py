from dataclasses import dataclass, asdict
import re
from uuid import uuid4
from .properties import Prop, Link
from datetime import datetime

@dataclass
class Citation:
    text: str
    props: "list[Prop]" = None
    links: "list[Link]" = None
    
    def __init__(self, text) -> None:
        self.text = text

    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
    
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
 
@dataclass   
class Identifier:
    identifier: str
    scheme: str = None
    
    def __init__(self, identifier, scheme=None):
        self.identifier = identifier
        
        #scheme must follow pattern ^[a-zA-Z][a-zA-Z0-9+\\-.]+:.+$, then set it
        if scheme is not None:
            if re.match("^[a-zA-Z][a-zA-Z0-9+\\-.]+:.+$", scheme):
                self.scheme = scheme
    
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Hash:
    value: str
    algorithm: str
    
    def __init__(self, value, algorithm) -> None:
        self.value = value
        self.algorithm = algorithm

@dataclass
class ResourceLink:
    href: str
    media_type: str = None
    hashes: "list[Hash]" = None
    
    def __init__(self, href, media_type=None):
        self.href = href
        self.media_type = media_type
        
    def add_hash(self, value, algorithm):
        if self.hashes is None:
            self.hashes = []
        self.hashes.append(Hash(value, algorithm))
    
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
        

@dataclass
class Base64:
    value: str
    filename: str = None
    media_type: str = None
    
    def __init__(self, value, filename=None, media_type=None):
        self.value = value
        self.filename = filename
        self.media_type = media_type
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Resource:
    uuid: str
    title: str = None
    description: str = None
    props: "list[Prop]" = None
    document_ids: "list[Identifier]" = None
    citation: Citation = None
    rlinks: "list[ResourceLink]" = None
    base64: Base64 = None
    remarks: "list[str]" = None
    
    def __init__(self, uuid=str(uuid4()), title=None, description=None):
        self.uuid = uuid
        self.title = title
        self.description = description
    
    def base64(self, value, filename=None, media_type=None):
        self.base64 = Base64(value, filename, media_type)
    
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
    
    def citation(self, text):
        self.citation = Citation(text)
        
    def add_document_id(self, identifier, scheme=None):
        if self.document_ids is None:
            self.document_ids = []
        self.document_ids.append(Identifier(identifier, scheme))
        
    def add_rlink(self, href, media_type=None):
        if self.rlinks is None:
            self.rlinks = []
        self.rlinks.append(ResourceLink(href, media_type))
        
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class BackMatter:
    resources: "list[Resource]" = None
    
    def __init__(self) -> None:
        self.resources = []
    
    def add_resource(self, uuid=str(uuid4()), title=None, description=None):
        if self.resources is None:
            self.resources = []
        self.resources.append(Resource(uuid, title, description))
    
@dataclass
class Revision:
    version: str
    title: str = None
    published: str = None
    last_modified: str = None
    oscal_version: str = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    remarks: "list[str]" = None
    
    def __init__(self, version, title=None, published=datetime.now().isoformat(), last_modified=datetime.now().isoformat(), oscal_version=None) -> None:
        self.version = version
        self.title = title
        self.published = published
        self.last_modified = last_modified
        self.oscal_version = oscal_version
        
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
        self.last_modified = datetime.now().isoformat()
    
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
        self.last_modified = datetime.now().isoformat()
        
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        self.last_modified = datetime.now().isoformat()
        
    def update_time(self):
        self.last_modified = datetime.now().isoformat()
    
@dataclass
class Role:
    id: str
    title: str
    short_name: str = None
    description: str = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    remarks: "list[str]" = None
    
    def __init__(self, id, title, short_name=None, description= None) -> None:
        self.id = id
        self.title = title
        self.short_name = short_name
        self.description = description
        
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
        
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
        
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class TelephoneNumber:
    number: str
    type: str = None

    def __init__(self, number, type=None):
        self.number = number
        self.type = type
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
    
@dataclass
class Address:
    city: str
    state: str
    postal_code: str
    country: str
    type: str
    addr_lines: "list[str]"  # list of strings ^\\S(.*\\S)?$
    
    def __init__(self, address, city, state, postal_code, country, type, line2=None) -> None:
        self.addr_lines = []
        self.addr_lines.append(address)
        if line2 is not None:
            self.addr_lines.append(line2)
        self.type = type
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
    

@dataclass
class Party:
    uuid: str # ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
    type: str # "person" | "organization"
    name: str = None
    short_name: str = None
    external_ids: "list[Identifier]" = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    email_addresses: "list[str]" = None
    telephone_numbers: "list[TelephoneNumber]" = None
    addresses: "list[Address]" = None
    location_uuids: "list[str]" = None # list of strings ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
    members_of_organization: "list[str]" = None # list of strings ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
    remarks: "list[str]" = None
    
    def __init__(self, type, name=None, short_name=None, uuid=str(uuid4())) -> None:
        if not re.match("^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$", uuid):
            raise ValueError("Invalid UUID - must be UUIDv4")
        if type != "person" and type != "organization":
            raise ValueError("Party type must be 'person' or 'organization'")
        
        self.uuid = uuid
        self.type = type
        self.name = name
        self.short_name = short_name
        
    def add_external_id(self, scheme, identifier):
        if self.external_ids is None:
            self.external_ids = []
        self.external_ids.append(Identifier(scheme, identifier))
        
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
    
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
        
    def add_email_address(self, email_address):
        if self.email_addresses is None:
            self.email_addresses = []
            
        #email must match ^.+@.+$
        if not re.match("^.+@.+$", email_address):
            raise ValueError("Invalid email address")
        self.email_addresses.append(email_address) # ^.+@.+$
    
    def add_telephone_number(self, number, type=None):
        if self.telephone_numbers is None:
            self.telephone_numbers = []
        self.telephone_numbers.append(TelephoneNumber(number, type))
        
    def add_address(self, address, city, state, postal_code, country, type, line2=None):
        if self.addresses is None:
            self.addresses = []
        self.addresses.append(Address(address, city, state, postal_code, country, type, line2))
    
    def add_location_uuid(self, location_uuid):
        if self.location_uuids is None:
            self.location_uuids = []
        if not re.match("^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$", location_uuid):
            raise ValueError("Invalid UUID - must be UUIDv4")
        self.location_uuids.append(location_uuid)
    
    def add_member_of_organization(self, member_of_organization):
        if self.members_of_organization is None:
            self.members_of_organization = []
            
        #must match ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
        if not re.match("^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$", member_of_organization):
            raise ValueError("Invalid UUID - must be UUIDv4")
        self.members_of_organization.append(member_of_organization)
    
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        
    def __dict__(self):
        obj = asdict(self)
        return {k: v for k, v in asdict(self).items() if v is not None}
    

@dataclass
class ResponsibleParty:
    role_id: str
    party_uuids: "list[str]" = None 
    props: "list[Prop]" = None # list of Prop objects
    links: "list[Link]" = None
    remarks: "list[str]" = None # list of strings "^\\S(.*\\S)?$"]"
    
    def __init__(self, role_id, party_uuid):
        #role_id must match ^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$
        if not re.match("^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$", role_id):
            raise ValueError("Invalid role_id - must match ^(\\p{L}|_)(\\p{L}|\\p{N}|[.\\-_])*$")
        #party_uuid must match 	^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
        if not re.match("^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$", party_uuid):
            raise ValueError("Invalid UUID - must be UUIDv4")
        
        self.role_id = role_id
        self.party_uuids.append(party_uuid)
        
    def add_party_uuid(self, party_uuid):
        #must match ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
        if not re.match("^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$", party_uuid):
            raise ValueError("Invalid UUID - must be UUIDv4")
        self.party_uuids.append(party_uuid)
    
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
    
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
    
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
    
        
@dataclass
class Location:
    address: Address
    uuid: str
    title: str = None
    email_addresses: "list[str]" = None
    telephone_numbers: "list[TelephoneNumber]" = None
    urls: "list[str]" = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    remarks: "list[str]" = None
    
    def __init__(self, address, city, state, postal_code, country=None, line2=None, type=None, title=None, uuid=str(uuid4())):
        # uuid must match ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$
        if not re.match("^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$", uuid):
            raise ValueError("Invalid UUID - must be UUIDv4")
        
        self.address = Address(address, city, state, postal_code, country, type, line2)
        self.uuid = uuid
        self.title = title
        
    def add_email_address(self, email_address):
        if self.email_addresses is None:
            self.email_addresses = []
            
        #email must match ^.+@.+$
        if not re.match("^.+@.+$", email_address):
            raise ValueError("Invalid email address")
        self.email_addresses.append(email_address)
        
    def add_telephone_number(self, number, type=None):
        if self.telephone_numbers is None:
            self.telephone_numbers = []
        self.telephone_numbers.append(TelephoneNumber(number, type))
        
    def add_url(self, url):
        if self.urls is None:
            self.urls = []
        self.urls.append(url)
    
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
        
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
        
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
    

@dataclass
class Metadata:
    title: str
    last_modified: str # isoformat
    version: str
    oscal_version: str
    published: str = datetime.now().isoformat() # isoformat
    revisions: "list[Revision]" = None
    document_ids: "list[Identifier]" = None
    props: "list[Prop]" = None
    links: "list[Link]" = None
    roles: "list[Role]" = None
    locations: "list[Location]" = None
    parties: "list[Party]" = None
    responsible_parties: "list[ResponsibleParty]" = None
    remarks: "list[str]" = None
    
    def __init__(self, title, version, oscal_version, last_modified=datetime.now().isoformat(), published=datetime.now().isoformat(), parties=None, roles=None, locations=None, responsible_parties=None, revisions=None, document_ids=None, props=None, links=None, remarks=None):
        self.title = title
        self.last_modified = last_modified
        self.version = version
        self.oscal_version = oscal_version
        self.published = published
        self.parties = parties
        self.roles = roles
        self.locations = locations
        self.responsible_parties = responsible_parties
        self.revisions = revisions
        self.document_ids = document_ids
        self.props = props
        self.links = links
        self.remarks = remarks
    
    def set_publish_timestamp(self, published=datetime.now()):
        self.published = published.isoformat()
    
    def add_revision(self, version, title=None, published=datetime.now().isoformat(), last_modified=datetime.now().isoformat(), oscal_version=None):
        if self.revisions is None:
            self.revisions = []
        self.revisions.append(Revision(version, title, published, last_modified, oscal_version))
        
    def add_document_id(self, identifier, scheme=None):
        if self.document_ids is None:
            self.document_ids = []
        self.document_ids.append(Identifier(identifier, scheme))
    
    def add_prop(self, name, value, ns=None, property_class=None, uuid=str(uuid4())):
        if self.props is None:
            self.props = []
        self.props.append(Prop(name, value, ns, property_class, uuid))
        
    def add_link(self, href, rel=None, media_type=None, text=None):
        if self.links is None:
            self.links = []
        self.links.append(Link(href, rel, media_type, text))
        
    def add_role(self, id, title, short_name=None, description= None):
        if self.roles is None:
            self.roles = []
        self.roles.append(Role(id, title, short_name, description))
        
    def add_location(self, address, city, state, postal_code, country=None, line2=None, type=None, title=None, uuid=str(uuid4())):
        if self.locations is None:
            self.locations = []
        self.locations.append(Location(address, city, state, postal_code, country, line2, type, title, uuid))
        
    def add_party(self, name, type=None, short_name=None, uuid=str(uuid4())):
        if self.parties is None:
            self.parties = []
        self.parties.append(Party(name, type, short_name, uuid))
        
    def add_respone_party(self, role_id, party_uuid):
        if self.responsible_parties is None:
            self.responsible_parties = []
        self.responsible_parties.append(ResponsibleParty(role_id, party_uuid))  
        
    def add_remark(self, remark):
        if self.remarks is None:
            self.remarks = []
        self.remarks.append(remark)
        
    def __dict__(self):
        return {k: v for k, v in asdict(self).items() if v is not None}