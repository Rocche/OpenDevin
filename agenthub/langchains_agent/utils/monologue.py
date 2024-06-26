
import agenthub.langchains_agent.utils.json as json
import agenthub.langchains_agent.utils.prompts as prompts

class Monologue:
    def __init__(self):
        self.thoughts = []

    def add_event(self, t: dict):
        if not isinstance(t, dict):
            raise ValueError("Event must be a dictionary")
        self.thoughts.append(t)

    def get_thoughts(self):
        return self.thoughts

    def get_total_length(self):
        total_length = 0
        for t in self.thoughts:
            try:
                total_length += len(json.dumps(t))
            except TypeError as e:
                print(f"Error serializing thought: {e}")
        return total_length

    def condense(self, llm):
        try:
            prompt = prompts.get_summarize_monologue_prompt(self.thoughts)
            response = llm.prompt(prompt)
            self.thoughts = prompts.parse_summary_response(response)
        except Exception as e:
            # Consider logging the error here instead of or in addition to raising an exception
            raise RuntimeError(f"Error condensing thoughts: {e}")
