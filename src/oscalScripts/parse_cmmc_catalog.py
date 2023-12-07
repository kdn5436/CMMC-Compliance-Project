import json

def get_control_llm_system_message(cmmc_catalog_filepath):
    with open(cmmc_catalog_filepath, 'r') as f:
        catalog = json.load(f)
        for group in catalog['groups']:
            for control in group['controls']:
                descriptions = "/n".join(["Description: " + prop["value"] for prop in control['props'] if prop['name'] == 'description'])
                # print(f"ID: {control['id']}\tTitle: {control['title']}\n{descriptions}\n")

if __name__ == '__main__':
    get_control_llm_system_message('../ref/cmmc_v2_L3.json')