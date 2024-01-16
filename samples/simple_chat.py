from autogen import UserProxyAgent, ConversableAgent, config_list_from_json,AssistantAgent,GroupChat,GroupChatManager

def socket_server(data):
    print(f'\n\n from tye callback{data}\n\n')
def main():
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample.
    # For example, if you have created a OAI_CONFIG_LIST file in the current working directory, that file will be used.
    # config_list = config_list_from_json(env_or_file="env.json")

    # Create the agent that uses the LLM.
    llm_config={'config_list': [{'model': 'gpt-4-1106-preview', 'api_key': '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','stream':True}]}
    user_proxy = UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
        human_input_mode="TERMINATE",
    )
    coder = AssistantAgent(
        name="Coder",
        llm_config=llm_config,
        use_socket=True,socket_server=socket_server
    )
    pm = AssistantAgent(
        name="Product_manager",
        system_message="Creative in software product ideas.",
        llm_config=llm_config,
        use_socket=True,socket_server=socket_server
    )
    groupchat = GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config,use_socket=True,socket_server=socket_server)

    user_proxy.initiate_chat(
    manager, message="givde me a graph of tesla stock"
)
    
if __name__ == "__main__":
    main()
