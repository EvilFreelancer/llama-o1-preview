class ChatHistory:
    def __init__(self, system_prompt=None, history_limit=None):
        self.history_limit = history_limit
        self.system_prompt = system_prompt
        self.messages = []
        if system_prompt is not None:
            self.messages = [{
                "role": "system",
                "content": system_prompt
            }]

    def add_message(self, role, message):
        self.messages.append({
            "role": role,
            "content": message
        })
        self.trim_history()

    def add_user_message(self, message):
        self.add_message("user", message)

    def add_think_message(self, message):
        if len(self.messages) > 0 and self.messages[-1]["role"] == "assistant":
            # Если последнее сообщение было от модели, то мерджим think в assistant role
            self.messages[-1]["content"] = f"<think>{message}</think> {self.messages[-1]['content']}"
        else:
            self.add_message("assistant", f"<think>{message}</think> ")

    def add_assistant_message(self, message):
        self.add_message("assistant", message)

    def trim_history(self):
        appendix = 0
        if self.system_prompt is not None:
            appendix = 1
        if self.history_limit is not None and len(self.messages) > self.history_limit + appendix:
            overflow = len(self.messages) - (self.history_limit + appendix)
            self.messages = [self.messages[0]] + self.messages[overflow + appendix:]  # remove old messages except system

    def get_messages(self) -> list:
        return self.messages
