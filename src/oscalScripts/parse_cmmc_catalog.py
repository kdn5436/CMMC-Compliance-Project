import json

def get_control_llm_system_message(cmmc_catalog_filepath):
    sys_msg = ""
    with open(cmmc_catalog_filepath, 'r') as f:
        catalog = json.load(f)
        for group in catalog['groups']:
            for control in group['controls']:
                descriptions = "/n".join(["Description: " + prop["value"] for prop in control['props'] if prop['name'] == 'description'])
                sys_msg += f"ID: {control['id']}\nTitle: {control['title']}\n{descriptions}\n\n"
                # sys_msg += f"Title: {control['title']}\n{descriptions}\n\n"
        f.close()
    return sys_msg[:-2]
if __name__ == '__main__':
    get_control_llm_system_message('../ref/cmmc_v2_L3.json')