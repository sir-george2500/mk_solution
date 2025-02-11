from time import time

class TokenBucket:
  """
  Implements a token bucket algorithm for rate limiting.

  This class represents a virtual bucket that holds a limited number of tokens (capacity).
  Tokens are refilled at a constant rate (refill_rate). Requesters can consume tokens,
  but only if there are enough available.

  Attributes:
      capacity (int): The maximum number of tokens the bucket can hold.
      refill_rate (float): The rate at which tokens are refilled (tokens per second).
      last_refill_time (float): The timestamp of the last refill.
      current_tokens (int): The current number of tokens available in the bucket.

  Methods:
      get_tokens(self, now: float=None) -> int:
          Calculates and returns the number of available tokens based on refill rate and elapsed time.
      consume(self, amount: int, now: float=None) -> bool:
          Attempts to consume the specified amount of tokens. Returns True if successful, False otherwise.
  """

  def __init__(self, capacity, refill_rate):
    self.capacity = capacity
    self.refill_rate = refill_rate
    self.last_refill_time = time()
    self.current_tokens = self.capacity

  def get_tokens(self, now=None):
    """
    Calculates the number of available tokens based on current time and last refill.

    Args:
        now (float, optional): A timestamp to use for calculating elapsed time.
                                Defaults to the current time.

    Returns:
        int: The number of available tokens.
    """
    if now is None:
      now = time()
    elapsed_time = now - self.last_refill_time
    refill_amount = min(elapsed_time, 1) * self.refill_rate
    self.current_tokens = min(self.capacity, self.current_tokens + refill_amount)
    self.last_refill_time = now
    return self.current_tokens

  def consume(self, amount, now=None):
    """
    Attempts to consume the specified amount of tokens.

    Args:
        amount (int): The number of tokens to consume.
        now (float, optional): A timestamp to use for calculating available tokens.
                                Defaults to the current time.

    Returns:
        bool: True if successful, False otherwise.
    """
    if now is None:
      now = time()
    available_tokens = self.get_tokens(now)
    if available_tokens >= amount:
      self.current_tokens -= amount
      return True
    else:
      return False

