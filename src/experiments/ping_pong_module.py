import dspy

lm = dspy.OpenAI(max_tokens=500)
dspy.settings.configure(lm=lm)


class PingPongModule(dspy.Module):
    """A module that simulates a game of ping pong."""

    def forward(self, player1, player2):
        pred = dspy.Predict("player1, player2 -> winner")

        result = pred(player1, player2).winner

        return result
