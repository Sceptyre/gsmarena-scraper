from dataclasses import dataclass
from ..parser import parse_html, parse_xml

@dataclass
class GSMArenaPhoneBasic:
    id: str
    make: str
    model: str
    url: str

@dataclass
class GSMArenaPhonesList(list[GSMArenaPhoneBasic]):
    def from_sitemap_xml(xml_content: str) -> 'GSMArenaPhonesList':
        phones_list = GSMArenaPhonesList()
        sitemap_parsed = parse_xml(xml_content)
        for loc in sitemap_parsed.find_all('loc'):
            url = loc.text
            if "related" in url or "pictures" in url or len(url.split("-")) > 2: continue

            path = url.split("/")[-1]

            phones_list.append(GSMArenaPhoneBasic(
                id = path.split("-")[-1].split(".")[0],
                make = path.split("_")[0],
                model = "_".join(path.split("-")[0].split("_")[1:]),
                url=url
            ))

        return phones_list

@dataclass 
class GSMArenaPhoneSpec:
    label: str
    value: str


@dataclass
class GSMArenaPhoneSpecCategory:
    category: str
    definitions: list[GSMArenaPhoneSpec]

@dataclass
class GSMArenaPhone(GSMArenaPhoneBasic): 
    specs: dict[str,str]

    @staticmethod
    def from_html_response(html_content: str, basic_details: GSMArenaPhoneBasic) -> 'GSMArenaPhone':
        specs={}
        parsed = parse_html(html_content)
        specs_list_container = parsed.find("div", {"id": "specs-list"})
        
        if not specs_list_container: return GSMArenaPhone(
            **basic_details.__dict__,
            specs=specs
        )

        for category in specs_list_container.find_all("table"):
            cat_name = category.find_all("tr")[0].th.text.lower().replace(" ", "_")


            prev_spec_key = cat_name
            for spec_container in category.find_all("tr"):
                # skip empty row
                if not len(spec_container.find_all("td")): continue
                spec_category = spec_container.find_all("td")[0].text.lower().replace(" ", "_")

                spec_value = spec_container.find_all("td")[1].text.strip()

                spec_key = f"{cat_name}.{spec_category}"
                if spec_category == "\u00a0": 
                    spec_key = f"{prev_spec_key}.extended"

                specs[spec_key] = spec_value

                prev_spec_key = spec_key

        return GSMArenaPhone(
            **basic_details.__dict__,
            specs=specs
        )