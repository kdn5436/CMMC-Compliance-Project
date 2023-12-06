from io import TextIOWrapper
import openai
from parse_cmmc_catalog import get_control_llm_system_message
import os, dotenv
import yaml

dotenv.load_dotenv()

L1_CONTROLS_SYSTEM_MSG = get_control_llm_system_message('../ref/cmmc_v2_L3.json')
CLIENT = openai.Client(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORG_ID"))

def classify_controls_in_task_win10(task_filepath: TextIOWrapper):
    sys_msg_content = f"""
    You are a component in a program that maps an ansible security implementation to a relevant security control in compliance with the CMMC Model V2 Security controls.
    You will be given an ansible task that implements a security control, and you will be respond with the ID of the security control that best represents the ansible task.
    Below is a list of CMMC Model V2 Level 1 Security Controls.  For each control, there is it's ID and Title, followed by a description of what the control requires.

    Controls:
    ```
    {L1_CONTROLS_SYSTEM_MSG}
    ```

    If the provided task is not relevant to any of the controls, respond with the word "NONE".
    """

    sys_msg = [{"role": "system", "content": sys_msg_content}]

    classifications = []
    used_tokens = 0
    with open(task_filepath, "r") as f:
        tasks = yaml.load(f.read())

        for task in tasks:
            #TODO PATCH tasks have changing actions, and thus can be classified based on the action (ansible.windows.win_regedit, ansible.windows.win_shell, etc...)
            # AUDIT tasks can either have a verification action, or a when conditional based on a previous action in the block
            # tasks are nested if they have a block key, which contains a list of more tasks

            task_name = task["name"].split(" ")[3]
            if "block" in task.keys():
                 task_name = "".join(task["name"][3:4]) 
            task_content = ""

            task_msg = [{"role": "user", "content": task_content}]

            response = CLIENT.chat.completions.create(
                model="gpt-4-1106-preview",
                temperature=0.0,
                messages=sys_msg + task_msg,
            )

            classifications.append(response.choices[0].message.content)
            used_tokens += response.usage.total_tokens

    return classifications, used_tokens
def main():
    
        classifications = classify_controls_in_task_win10("../src/lvl2/roles/Win10STIG/tasks/cat3.yml")

if __name__ == '__main__':
    main()