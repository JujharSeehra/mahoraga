class LearningTrigger:

    KEYWORDS = {
        "remember",
        "learn",
        "learned",
        "fixed",
        "fix",
        "solved",
        "solution",
        "working now",
        "works now",
        "failed",
        "failure",
        "problem",
        "issue",
        "discovered",
        "found out",
        "figured out",
        "important",
        "don't forget",
        "do not forget",
    }

    def should_evaluate(
        self,
        user_input
    ):

        text = user_input.lower()

        for keyword in self.KEYWORDS:

            if keyword in text:

                return True

        return False