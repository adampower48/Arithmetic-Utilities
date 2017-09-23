# Generates primes up to and including given max. Sieve method.
def generate_primes(max_bound):
    primes = []
    nums = [True] * (max_bound + 1)

    for i in range(2, max_bound + 1):
        if nums[i]:
            primes.append(i)
            for k in range(i, max_bound + 1, i):
                nums[k] = False

    return primes


# Returns prime factors of a given number.
def prime_factors(num):
    primes = generate_primes(num)
    factors = []

    prime_index = 0
    while num > 1:
        if num % primes[prime_index] == 0:
            factors.append(primes[prime_index])
            num /= primes[prime_index]
        else:
            prime_index += 1

    return factors
